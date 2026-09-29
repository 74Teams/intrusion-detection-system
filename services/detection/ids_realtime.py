import re
from typing import List, Optional, Callable
from services.ingestion import DecodedPacket
from services.detection import SnortRule
from services.detection.manager_rules import RuleManager
from services.detection.pattern_matcher import MultiPatternMatcher

class DetectionEngine:
    """
    Core Engine so khớp luật thời gian thực (Real-time Rule Matcher).
    Bóc tách các trường trong DecodedPacket và đối chiếu với tập luật của RuleManager.
    """

    def __init__(self, rule_manager: RuleManager, alert_callback: Optional[Callable] = None):
        self.rule_manager = rule_manager
        self.alert_callback = alert_callback
        self.http_matcher = MultiPatternMatcher()
        self.raw_matcher = MultiPatternMatcher()
        self.prepare_fast_matchers()

    def prepare_fast_matchers(self) -> None:
        for rule in self.rule_manager.rules:
            if not rule.is_enabled:
                continue
            for c in rule.contents:
                pattern = c.lower() if rule.nocase else c
                if rule.http_uri or rule.http_client_body or rule.http_header:
                    self.http_matcher.add_pattern(pattern, rule)
                else:
                    self.raw_matcher.add_pattern(pattern, rule)

        self.http_matcher.build()
        self.raw_matcher.build()

    def evaluate_packet(self, packet: DecodedPacket) -> List[SnortRule]:
        matched_rules: List[SnortRule] = []

        for rule in self.rule_manager.rules:
            if not rule.is_enabled:
                continue

            if rule.protocol != "ip" and rule.protocol != packet.protocol.lower():
                continue

            if not self._match_port(packet.dst_port, rule.dst_port):
                continue
            if not self._match_port(packet.src_port, rule.src_port):
                continue

            if rule.flags and not self._match_flags(packet.tcp_flags, rule.flags):
                continue

            if rule.http_uri or rule.http_client_body or rule.http_header or rule.http_method:
                if not packet.http_data:
                    continue

                if rule.http_method and packet.http_data.method != rule.http_method:
                    continue

                target_text = ""
                if rule.http_uri:
                    target_text = packet.http_data.uri
                elif rule.http_client_body:
                    target_text = packet.http_data.body
                elif rule.http_header:
                    target_text = " ".join([f"{k}:{v}" for k, v in packet.http_data.headers.items()])

                if not self._match_contents(target_text, rule.contents, rule.nocase):
                    continue

                if rule.pcre and not self._match_pcre(target_text, rule.pcre):
                    continue

            else:
                if rule.contents:
                    raw_text = packet.raw_payload.decode("latin-1", errors="replace")
                    if not self._match_contents(raw_text, rule.contents, rule.nocase):
                        continue
                    if rule.pcre and not self._match_pcre(raw_text, rule.pcre):
                        continue

            matched_rules.append(rule)
            self._trigger_alert(packet, rule)

        return matched_rules

    def _match_port(self, packet_port: Optional[int], rule_port: str) -> bool:
        if rule_port == "any" or rule_port == "$HTTP_PORTS":
            if rule_port == "$HTTP_PORTS":
                return packet_port in {80, 8080, 8000, 3000, 5000}
            return True
        if packet_port is None:
            return False
        try:
            return packet_port == int(rule_port)
        except ValueError:
            return True

    def _match_flags(self, packet_flags: dict, rule_flags: str) -> bool:
        raw = packet_flags.get("raw_flags", "")
        if rule_flags == "0":
            return len(raw) == 0
        return all(f in raw for f in rule_flags)

    def _match_contents(self, text: str, contents: List[str], nocase: bool) -> bool:
        if not contents:
            return True
        target = text.lower() if nocase else text
        for c in contents:
            pattern = c.lower() if nocase else c
            if pattern not in target:
                return False
        return True

    def _match_pcre(self, text: str, pcre_str: str) -> bool:
        try:
            flags = 0
            pattern = pcre_str
            if pcre_str.startswith("/") and pcre_str.rfind("/") > 0:
                last_slash = pcre_str.rfind("/")
                pattern = pcre_str[1:last_slash]
                flag_str = pcre_str[last_slash + 1:]
                if "i" in flag_str:
                    flags |= re.IGNORECASE
            return bool(re.search(pattern, text, flags))
        except Exception:
            return False

    def _trigger_alert(self, packet: DecodedPacket, rule: SnortRule) -> None:
        alert_data = {
            "timestamp": packet.timestamp,
            "sid": rule.sid,
            "msg": rule.msg,
            "severity": rule.severity,
            "classtype": rule.classtype,
            "src_ip": packet.src_ip,
            "src_port": packet.src_port,
            "dst_ip": packet.dst_ip,
            "dst_port": packet.dst_port,
            "protocol": packet.protocol,
            "http_uri": packet.http_data.uri if packet.http_data else None,
            "http_method": packet.http_data.method if packet.http_data else None,
        }
        if self.alert_callback:
            self.alert_callback(alert_data)
        else:
            print(f"[ALERT sid:{rule.sid}] {rule.msg} | {packet.src_ip} -> {packet.dst_ip}")
