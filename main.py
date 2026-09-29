import sys
import time
import queue
import threading
from pathlib import Path

from config.config import SETTINGS
from services.database import init_db
from services.database.repository import EventRepository
from services.ingestion import DecodedPacket
from services.ingestion.packet_decoder import PacketDecoder
from services.ingestion.packet_capture import PacketCapture
from services.detection.manager_rules import RuleManager
from services.detection.ids_realtime import DetectionEngine
from services.ai_engine.ai_worker import AITrafficWorker

def handle_alert(alert_data: dict):
    """Callback luu canh bao vao database khi phat hien vi pham."""
    try:
        event = EventRepository.save_alert(alert_data)
        sid_str = f"SID:{alert_data.get('sid')}" if alert_data.get('sid') else "AI-ANOMALY"
        print(f"[ALERT #{event.id}] [{sid_str}] {alert_data.get('msg')} | {alert_data.get('src_ip')} -> {alert_data.get('dst_ip')}:{alert_data.get('dst_port')}")
    except Exception as e:
        print(f"[AlertError] Khong the luu alert: {e}")

def main():
    print("=" * 65)
    print("       HYBRID NIDS (Rule-based & AI-driven Engine)          ")
    print("=" * 65)

    # 1. Khoi tao Co so du lieu
    print("[1/4] Dang khoi tao CSDL...")
    init_db()

    # 2. Nap Rules tu thu muc rules/
    rules_dir = SETTINGS.get("detection", {}).get("rules_dir", "rules")
    print(f"[2/4] Dang nap cac tap luat tu '{rules_dir}'...")
    rule_manager = RuleManager(rules_dir)
    total_rules = rule_manager.load_all_rules()
    print(f"      -> Da nap thanh cong {total_rules} rules vao RAM.")

    # 3. Khoi tao Detection Engine & AI Worker
    print("[3/4] Khoi tao Detection Analysis Engine...")
    detection_engine = DetectionEngine(rule_manager, alert_callback=handle_alert)
    ai_worker = AITrafficWorker(alert_callback=handle_alert)

    # Hang doi dem bat dong bo (Packet Buffer Queue) chong rot goi
    packet_queue = queue.Queue(maxsize=SETTINGS.get("detection", {}).get("queue_max_size", 10000))

    def on_raw_packet(scapy_pkt):
        """Callback tu PacketCapture: Giai ma goi tin tho roi day vao Queue."""
        decoded = PacketDecoder.decode(scapy_pkt)
        if decoded is None:
            return  # Bo qua goi tin khong phai IP
        try:
            packet_queue.put_nowait(decoded)
        except queue.Full:
            print("[Canh bao] Queue day! Dang bi drop goi tin.")

    # Luong Worker xu ly phan tich
    def worker_loop():
        while True:
            try:
                packet = packet_queue.get(timeout=1.0)
                # Dua vao Rule Engine
                detection_engine.evaluate_packet(packet)
                # Dua vao AI Worker
                ai_worker.analyze_packet(packet)
                packet_queue.task_done()
            except queue.Empty:
                continue

    worker_thread = threading.Thread(target=worker_loop, daemon=True)
    worker_thread.start()

    # 4. Khoi chay Packet Ingestion (Sniffer)
    bpf = SETTINGS.get("network", {}).get("bpf_filter", "ip")
    iface = SETTINGS.get("network", {}).get("interface", None) or None
    capture_mode = SETTINGS.get("network", {}).get("capture_mode", "live")

    print(f"[4/4] Bat dau bat goi tin (Che do: {capture_mode}, BPF: '{bpf}')...")
    capturer = PacketCapture(raw_callback=on_raw_packet, bpf_filter=bpf)

    try:
        if capture_mode == "offline":
            pcap_file = SETTINGS.get("network", {}).get("pcap_file", "")
            print(f"      -> Dang phan tich file PCAP: {pcap_file}")
            capturer.start_offline(pcap_file)
            # Doi worker thread xu ly het cac goi tin trong queue
            packet_queue.join()
            time.sleep(0.5)  # Cho cac alert cuoi cung duoc ghi vao DB
            print(f"\n[*] Da phan tich xong file PCAP. Kiem tra alerts tai API: http://localhost:8000/api/alerts/")
        else:
            print("      -> Dang lang nghe truc tiep tren card mang (Nhan Ctrl+C de dung)...")
            capturer.start_live(iface)
    except KeyboardInterrupt:
        print("\n[!] Dung he thong NIDS.")
    except Exception as e:
        print(f"\n[Loi Capture] {e}")

if __name__ == "__main__":
    main()
