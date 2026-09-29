from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class RuleOption:
    """Đại diện cho một option bên trong dấu ngoặc (...) của Rule Snort."""
    name: str
    value: Optional[str] = None

@dataclass
class SnortRule:
    """Mô hình dữ liệu của một Rule đã được phân tích cú pháp."""
    action: str                  # alert, log, drop
    protocol: str                # tcp, udp, icmp, ip
    src_ip: str
    src_port: str
    direction: str               # -> hoặc <>
    dst_ip: str
    dst_port: str
    
    # Options phổ biến
    msg: str = ""
    sid: int = 0
    rev: int = 1
    classtype: str = ""
    severity: int = 2            # 1: High, 2: Med, 3: Low
    
    # Payload patterns
    contents: List[str] = field(default_factory=list)
    nocase: bool = False
    
    # HTTP Modifiers
    http_uri: bool = False
    http_client_body: bool = False
    http_header: bool = False
    http_method: Optional[str] = None
    
    # TCP Flags
    flags: Optional[str] = None
    
    # Regex
    pcre: Optional[str] = None
    
    raw_rule: str = ""
    is_enabled: bool = True
