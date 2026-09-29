"""
Script tạo file PCAP mẫu chứa các gói tin tấn công giả lập.
Dùng cho demo NIDS ở chế độ offline.

Chạy: python create_demo_pcap.py
Output: pcap_samples/demo_attacks.pcap
"""
from scapy.all import IP, TCP, UDP, ICMP, Raw, wrpcap, Ether
import os

OUTPUT_DIR = "pcap_samples"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "demo_attacks.pcap")

os.makedirs(OUTPUT_DIR, exist_ok=True)

packets = []

# 1. SQL INJECTION ATTACKS

# SID:1000001 - UNION SELECT
sqli_union = (
    IP(src="192.168.1.100", dst="10.0.0.5")
    / TCP(sport=54321, dport=80, flags="PA", seq=1000, ack=1)
    / Raw(load=b"GET /search?q=1'+UNION+SELECT+username,password+FROM+users-- HTTP/1.1\r\nHost: victim.com\r\nUser-Agent: Mozilla/5.0\r\n\r\n")
)
packets.append(sqli_union)

# SID:1000002 - OR boolean bypass
sqli_or = (
    IP(src="192.168.1.100", dst="10.0.0.5")
    / TCP(sport=54322, dport=80, flags="PA", seq=2000, ack=1)
    / Raw(load=b"GET /login?user=admin'+or+'1'%3D'1 HTTP/1.1\r\nHost: victim.com\r\nUser-Agent: Mozilla/5.0\r\n\r\n")
)
packets.append(sqli_or)

# SID:1000003 - SQL comment (--)
sqli_comment = (
    IP(src="192.168.1.100", dst="10.0.0.5")
    / TCP(sport=54323, dport=80, flags="PA", seq=3000, ack=1)
    / Raw(load=b"GET /page?id=1-- HTTP/1.1\r\nHost: victim.com\r\n\r\n")
)
packets.append(sqli_comment)

# 2. CROSS-SITE SCRIPTING (XSS)

# SID:1000010 - <script> tag
xss_script = (
    IP(src="192.168.1.101", dst="10.0.0.5")
    / TCP(sport=54330, dport=80, flags="PA", seq=4000, ack=1)
    / Raw(load=b"GET /comment?text=<script>alert('XSS')</script> HTTP/1.1\r\nHost: victim.com\r\n\r\n")
)
packets.append(xss_script)

# SID:1000011 - javascript: URI
xss_js = (
    IP(src="192.168.1.101", dst="10.0.0.5")
    / TCP(sport=54331, dport=80, flags="PA", seq=5000, ack=1)
    / Raw(load=b"GET /redirect?url=javascript:alert(document.cookie) HTTP/1.1\r\nHost: victim.com\r\n\r\n")
)
packets.append(xss_js)

# SID:1000012 - Event handler (POST body)
xss_event = (
    IP(src="192.168.1.101", dst="10.0.0.5")
    / TCP(sport=54332, dport=80, flags="PA", seq=6000, ack=1)
    / Raw(load=b"POST /api/comment HTTP/1.1\r\nHost: victim.com\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 35\r\n\r\nbody=<img src=x onerror=alert(1)>")
)
packets.append(xss_event)

# 3. PATH TRAVERSAL / LFI

# SID:1000020 - ../
path_traversal = (
    IP(src="192.168.1.102", dst="10.0.0.5")
    / TCP(sport=54340, dport=80, flags="PA", seq=7000, ack=1)
    / Raw(load=b"GET /file?path=../../../../etc/passwd HTTP/1.1\r\nHost: victim.com\r\n\r\n")
)
packets.append(path_traversal)

# SID:1000021 - /etc/passwd
lfi_passwd = (
    IP(src="192.168.1.102", dst="10.0.0.5")
    / TCP(sport=54341, dport=80, flags="PA", seq=8000, ack=1)
    / Raw(load=b"GET /download?file=/etc/passwd HTTP/1.1\r\nHost: victim.com\r\n\r\n")
)
packets.append(lfi_passwd)

# SID:1000022 - win.ini
lfi_winini = (
    IP(src="192.168.1.102", dst="10.0.0.5")
    / TCP(sport=54342, dport=8080, flags="PA", seq=9000, ack=1)
    / Raw(load=b"GET /download?file=C:\\windows\\win.ini HTTP/1.1\r\nHost: victim.com\r\n\r\n")
)
packets.append(lfi_winini)

# 4. COMMAND INJECTION (RCE)

# SID:1000030 - Chained commands
cmd_inject = (
    IP(src="192.168.1.103", dst="10.0.0.5")
    / TCP(sport=54350, dport=80, flags="PA", seq=10000, ack=1)
    / Raw(load=b"GET /ping?host=127.0.0.1;cat+/etc/shadow HTTP/1.1\r\nHost: victim.com\r\n\r\n")
)
packets.append(cmd_inject)

# 5. NETWORK SCANS (NMAP)

# SID:1000100 - Nmap Xmas Scan (FIN + URG + PSH)
xmas_scan = (
    IP(src="192.168.1.200", dst="10.0.0.5")
    / TCP(sport=12345, dport=80, flags="FPU", seq=0)
)
packets.append(xmas_scan)

# SID:1000101 - Nmap Null Scan (no flags)
null_scan = (
    IP(src="192.168.1.200", dst="10.0.0.5")
    / TCP(sport=12346, dport=443, flags="", seq=0)
)
packets.append(null_scan)

# SID:1000102 - Nmap FIN Scan
fin_scan = (
    IP(src="192.168.1.200", dst="10.0.0.5")
    / TCP(sport=12347, dport=22, flags="F", seq=0)
)
packets.append(fin_scan)

# SID:1000103 - SYN-FIN anomaly
synfin = (
    IP(src="192.168.1.200", dst="10.0.0.5")
    / TCP(sport=12348, dport=8080, flags="SF", seq=0)
)
packets.append(synfin)

# 6. NORMAL TRAFFIC 

# HTTP GET bình thường
normal_http = (
    IP(src="192.168.1.50", dst="10.0.0.5")
    / TCP(sport=60000, dport=80, flags="PA", seq=100, ack=1)
    / Raw(load=b"GET /index.html HTTP/1.1\r\nHost: victim.com\r\nUser-Agent: Mozilla/5.0\r\n\r\n")
)
packets.append(normal_http)

# DNS query (UDP)
dns_query = (
    IP(src="192.168.1.50", dst="8.8.8.8")
    / UDP(sport=55555, dport=53)
    / Raw(load=b"\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01")
)
packets.append(dns_query)

# ICMP Ping bình thường
ping = (
    IP(src="192.168.1.50", dst="10.0.0.5")
    / ICMP(type=8, code=0)
    / Raw(load=b"PingPingPingPing")
)
packets.append(ping)

# Normal TCP SYN (kết nối bình thường)
normal_syn = (
    IP(src="192.168.1.50", dst="10.0.0.5")
    / TCP(sport=60001, dport=443, flags="S", seq=500)
)
packets.append(normal_syn)

# GHI RA FILE PCAP
wrpcap(OUTPUT_FILE, packets)
print(f"[OK] Da tao {len(packets)} goi tin vao {OUTPUT_FILE}")
print(f"   - 10 goi tan cong web (SQLi, XSS, Path Traversal, CMD Injection)")
print(f"   -  4 goi network scan (Xmas, Null, FIN, SYN-FIN)")
print(f"   -  4 goi traffic binh thuong (HTTP, DNS, ICMP, SYN)")
print(f"\n[INFO] De chay NIDS phan tich file nay:")
print(f"   python main.py")
