# Hybrid NIDS – Rule-based & AI-driven Network Intrusion Detection System

Hệ thống phát hiện xâm nhập mạng thời gian thực kết hợp giữa kiểm tra luật tĩnh (Rule-based kiểu Snort) và phát hiện bất thường qua trí tuệ nhân tạo (AI Flow Worker).

> **PBL4 – Project-Based Learning 4**  
> Hệ thống phát hiện xâm nhập mạng thời gian thực kết hợp kiểm tra luật tĩnh (Snort-compatible) và phát hiện bất thường qua trí tuệ nhân tạo (AI Flow Worker).

---

## 1. Cấu trúc thư mục dự án

## Mục lục

1. [Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
2. [Kiến trúc kỹ thuật](#2-kiến-trúc-kỹ-thuật)
3. [Cấu trúc thư mục](#3-cấu-trúc-thư-mục)
4. [Cài đặt & Chạy hệ thống](#4-cài-đặt--chạy-hệ-thống)
5. [Demo Offline (Khuyến nghị)](#5-demo-offline-khuyến-nghị)
6. [Tập luật phát hiện (Detection Rules)](#6-tập-luật-phát-hiện-detection-rules)
7. [REST API](#7-rest-api)
8. [Trạng thái phát triển](#8-trạng-thái-phát-triển)

---

## 1. Tổng quan hệ thống

Hybrid NIDS là hệ thống phát hiện xâm nhập mạng theo thời gian thực, hoạt động theo pipeline 4 tầng:

```
Gói tin mạng
     │
     ▼
┌─────────────────────┐
│  Traffic Ingestion  │  ← Scapy sniff (Live / Offline PCAP)
│  packet_capture.py  │
└────────┬────────────┘
         │ raw packet
         ▼
┌─────────────────────┐
│  Packet Decoder     │  ← Bóc tách L2–L7 (IP, TCP Flags, HTTP URI/Body)
│  packet_decoder.py  │
│  http_parser.py     │
└────────┬────────────┘
         │ DecodedPacket → Async Queue
         ▼
┌─────────────────────┐     ┌──────────────────┐
│  Detection Engine   │     │   AI Worker       │
│  ids_realtime.py    │     │   ai_worker.py    │  ← (stub, giai đoạn 2)
│  Aho-Corasick       │     └──────────────────┘
│  + PCRE Regex       │
└────────┬────────────┘
         │ Alert
         ▼
┌─────────────────────┐     ┌──────────────────┐
│  SQLite / MySQL DB  │────▶│  FastAPI REST API │
│  (SQLAlchemy ORM)   │     │  /api/alerts/     │
└─────────────────────┘     └──────────────────┘
```

**Kết quả thực nghiệm (Demo PCAP):**

- Phân tích 18 gói tin tấn công giả lập → phát hiện **16 cảnh báo**
- Bao phủ: SQLi, XSS, Path Traversal, Command Injection, Nmap Xmas/Null/FIN Scan
- **Zero False Positive** trên 4 gói traffic hợp lệ (HTTP, DNS, ICMP, TCP SYN)

---

## 2. Kiến trúc kỹ thuật

| Tầng             | Module                       | Công nghệ                             |
| ---------------- | ---------------------------- | ------------------------------------- |
| Thu nhận gói tin | `packet_capture.py`          | Scapy `sniff()` – Live & Offline PCAP |
| Giải mã L2–L4    | `packet_decoder.py`          | Scapy layers (IP, TCP, UDP, ICMP)     |
| Bóc tách HTTP L7 | `http_parser.py`             | Python HTTP parser thủ công           |
| So khớp luật     | `ids_realtime.py`            | Aho-Corasick + PCRE Regex             |
| Quản lý luật     | `manager_rules.py`           | Parser cú pháp Snort-compatible       |
| Lưu trữ sự kiện  | `models.py`, `repository.py` | SQLAlchemy 2.0 + SQLite/MySQL         |
| REST API         | `api/main.py`                | FastAPI + Uvicorn                     |
| Cấu hình         | `config/settings.yaml`       | PyYAML                                |

**Thuật toán so khớp: Aho-Corasick**  
Cho phép tìm kiếm đồng thời tất cả chuỗi nội dung (`content`) trong tập luật với độ phức tạp O(N) – không phụ thuộc vào số lượng rule, đảm bảo hiệu năng cao ngay cả khi tập luật mở rộng hàng nghìn entries.

---

## 3. Cấu trúc thư mục

```text
App/
├── config/
│   ├── config.py                 # Nạp cấu hình từ settings.yaml
│   └── settings.yaml             # Thiết lập Card mạng, BPF filter, CSDL, thư mục rules
│   ├── config.py                  # Nạp cấu hình từ settings.yaml
│   └── settings.yaml              # Cấu hình interface, capture mode, DB, rules dir
│
├── rules/                        # Tập quy tắc phát hiện xâm nhập (.rules)
│   ├── web_attacks.rules         # Rule SQLi, XSS, Path Traversal, Command Injection
│   └── network_scans.rules       # Rule Nmap Xmas, Null, FIN, Ping Flood
├── rules/                         # Tập quy tắc phát hiện (.rules)
│   ├── web_attacks.rules          # 10 rules: SQLi, XSS, Path Traversal, CMD Injection
│   └── network_scans.rules        # 4 rules: Nmap Xmas, Null, FIN, SYN-FIN Scan
│
├── services/
│   ├── ingestion/
│   │   ├── __init__.py           # Data structures: DecodedPacket, ParsedHTTPRequest
│   │   ├── packet_decode.py      # Bắt gói tin (Live/Offline PCAP) & giải mã L2-L4
│   │   └── http_parser.py        # Bóc tách tầng ứng dụng HTTP L7 (Method, URI, Body)
│   │   ├── __init__.py            # DataClass: DecodedPacket, ParsedHTTPRequest
│   │   ├── packet_capture.py      # Thu nhận gói tin (Live / Offline PCAP)
│   │   ├── packet_decoder.py      # Giải mã tầng L3–L4 + phân nhánh L7
│   │   └── http_parser.py         # Bóc tách HTTP: Method, URI, Headers, Body
│   │
│   ├── detection/
│   │   ├── __init__.py           # Data structure: SnortRule
│   │   ├── ids_realtime.py       # Core Engine so khớp luật thời gian thực
│   │   ├── manager_rules.py      # Parser đọc & quản lý tập luật (.rules)
│   │   └── pattern_matcher.py    # Aho-Corasick Multi-pattern Matcher
│   │   ├── __init__.py            # DataClass: SnortRule, RuleOption
│   │   ├── ids_realtime.py        # Core Detection Engine (so khớp theo thời gian thực)
│   │   ├── manager_rules.py       # Parser & loader tập luật .rules
│   │   └── pattern_matcher.py     # Aho-Corasick Multi-pattern Matcher
│   │
│   ├── ai_engine/
│   │   ├── __init__.py
│   │   ├── feature_extractor.py  # Trích xuất đặc trưng luồng (Packet rate, SYN ratio)
│   │   └── ai_worker.py          # Worker AI phát hiện bất thường (DDoS, Scan)
│   │   └── ai_worker.py           # AI Worker (stub – giai đoạn 2)
│   │
│   └── database/
│       ├── __init__.py           # Kết nối Database (SQLite/PostgreSQL) & Session
│       ├── models.py             # SQLAlchemy ORM Models (Rule, Event, Payload)
│       └── repository.py         # CRUD thao tác lưu và truy vấn cảnh báo
│       ├── __init__.py            # Kết nối DB & Session factory
│       ├── models.py              # ORM Models: RuleModel, EventModel, EventPayloadModel
│       └── repository.py          # CRUD: save_alert(), get_recent_events()
│
├── api/                          # Backend API & WebSocket phục vụ Dashboard
│   ├── main.py                   # FastAPI server
├── api/
│   ├── main.py                    # FastAPI app + CORS
│   └── routes/
│       └── alerts.py             # API danh sách Alerts
│       └── alerts.py              # GET /api/alerts/?limit=50
│
├── main.py                       # Điểm khởi chạy toàn bộ tiến trình NIDS
├── requirements.txt              # Danh sách thư viện phụ thuộc
├── pcap_samples/
│   └── demo_attacks.pcap          # File PCAP mẫu 18 gói tấn công giả lập
│
├── main.py                        # Entry point khởi chạy toàn bộ NIDS
├── create_demo_pcap.py            # Script tạo file PCAP giả lập để demo
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 2. Hướng dẫn cài đặt & Chạy hệ thống

## 4. Cài đặt & Chạy hệ thống

### 2.1. Yêu cầu tiên quyết

### 4.1. Yêu cầu

1. **Python 3.10+**.
2. **Npcap Driver** (trên Windows): Tải tại [npcap.com](https://npcap.com/#download) và chọn _"Install Npcap in WinPcap API-compatible Mode"_. (Trên Linux chỉ cần cài `sudo apt install libpcap-dev`).

- **Python 3.10+**
- **Npcap** (Windows – chỉ cần khi dùng Live Capture):
  Tải tại [npcap.com](https://npcap.com/#download), chọn _"Install Npcap in WinPcap API-compatible Mode"_.
- **Linux:** `sudo apt install libpcap-dev`

### 2.2. Cài đặt thư viện

### 4.2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 2.3. Khởi chạy NIDS Engine

### 4.3. Cấu hình `settings.yaml`

> **Lưu ý**: Trên Windows, cần mở Command Prompt / PowerShell bằng quyền **Run as Administrator** để bắt gói tin mạng.

```yaml
network:
  capture_mode: "offline" # "offline" hoặc "live"
  pcap_file: "pcap_samples/demo_attacks.pcap"

database:
  type: "sqlite"
  db_url: "sqlite:///nids_events.db" # Không cần MySQL khi dev/demo
```

---

## 5. Demo Offline (Khuyến nghị)

Cách demo nhanh nhất, **không cần quyền Admin và không cần Npcap**:

**Bước 1 – Tạo file PCAP mẫu:**

```bash
python create_demo_pcap.py
```

> Output: `pcap_samples/demo_attacks.pcap` (18 gói tin: 10 web attack + 4 network scan + 4 normal traffic)

**Bước 2 – Chạy NIDS Engine:**

```bash
python main.py
```

### 2.4. Khởi chạy API Dashboard (Tùy chọn)

**Kết quả mong đợi trên terminal:**

```
=================================================================
       HYBRID NIDS (Rule-based & AI-driven Engine)
=================================================================
[1/4] Dang khoi tao CSDL...
[2/4] Dang nap cac tap luat tu 'rules'...
      -> Da nap thanh cong 14 rules vao RAM.
[3/4] Khoi tao Detection Analysis Engine...
[4/4] Bat dau bat goi tin (Che do: offline, BPF: 'ip')...
[ALERT #1] [SID:1000001] WEB-ATTACK SQL Injection - UNION SELECT detected | 192.168.1.100 -> 10.0.0.5:80
[ALERT #2] [SID:1000003] WEB-ATTACK SQL Injection - SQL comment execution | 192.168.1.100 -> 10.0.0.5:80
[ALERT #3] [SID:1000010] WEB-ATTACK Cross-Site Scripting - SCRIPT tag attempt | 192.168.1.101 -> 10.0.0.5:80
...
[ALERT #14] [SID:1000103] SCAN Suspicious SYN-FIN packet detected | 192.168.1.200 -> 10.0.0.5:8080

[*] Da phan tich xong file PCAP. Kiem tra alerts tai API: http://localhost:8000/api/alerts/
```

**Bước 3 – Khởi động API Dashboard (terminal mới):**

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

- Swagger UI: http://localhost:8000/docs
- Danh sách alerts: http://localhost:8000/api/alerts/?limit=50

## Truy cập Swagger API docs tại: `http://localhost:8000/docs`.

## 6. Tập luật phát hiện (Detection Rules)

Cú pháp tương thích Snort:

```
alert tcp any any -> any $HTTP_PORTS (msg:"..."; http_uri; content:"union"; nocase; sid:1000001; severity:1;)
```

### `rules/web_attacks.rules` – 10 Rules

| SID     | Loại tấn công                      | Cơ chế phát hiện                     |
| ------- | ---------------------------------- | ------------------------------------ |
| 1000001 | SQL Injection – UNION SELECT       | `content` match trên `http_uri`      |
| 1000002 | SQL Injection – OR boolean bypass  | `pcre` regex trên `http_uri`         |
| 1000003 | SQL Injection – SQL comment (`--`) | `content` match trên `http_uri`      |
| 1000010 | XSS – `<script>` tag               | `content` match trên `http_uri`      |
| 1000011 | XSS – `javascript:` URI            | `content` match trên `http_uri`      |
| 1000012 | XSS – Event handler (`onerror=`)   | `pcre` regex trên `http_client_body` |
| 1000020 | Path Traversal – `../`             | `content` match trên `http_uri`      |
| 1000021 | LFI – `/etc/passwd`                | `content` match trên `http_uri`      |
| 1000022 | LFI – `win.ini`                    | `content` match trên `http_uri`      |
| 1000030 | Command Injection – chained cmds   | `pcre` regex trên `http_uri`         |

### `rules/network_scans.rules` – 4 Rules

| SID     | Loại scan       | Cơ chế phát hiện                                     |
| ------- | --------------- | ---------------------------------------------------- |
| 1000100 | Nmap Xmas Scan  | TCP flags `FUP` (FIN+URG+PSH đồng thời)              |
| 1000101 | Nmap Null Scan  | TCP flags `0` (không có cờ nào)                      |
| 1000102 | Nmap FIN Scan   | TCP flag `F` (chỉ FIN)                               |
| 1000103 | SYN-FIN Anomaly | TCP flags `SF` (SYN+FIN – bất hợp pháp theo RFC 793) |

---

## 7. REST API

Base URL: `http://localhost:8000`

| Method | Endpoint                | Mô tả                           |
| ------ | ----------------------- | ------------------------------- |
| `GET`  | `/health`               | Kiểm tra trạng thái server      |
| `GET`  | `/api/alerts/?limit=50` | Lấy danh sách cảnh báo gần nhất |

**Ví dụ response `/api/alerts/`:**

```json
[
  {
    "id": 1,
    "timestamp": "2026-09-29T13:24:02",
    "sid": 1000001,
    "source_type": "RULE_ENGINE",
    "attack_type": "web-application-attack",
    "severity": 1,
    "src_ip": "192.168.1.100",
    "src_port": 54321,
    "dst_ip": "10.0.0.5",
    "dst_port": 80,
    "protocol": "TCP",
    "http_method": "GET",
    "http_uri": "/search?q=1'+UNION+SELECT+username,password+FROM+users--",
    "summary": "WEB-ATTACK SQL Injection - UNION SELECT detected",
    "status": "NEW"
  }
]
```

---

## 8. Trạng thái phát triển

| Tính năng                                           | Trạng thái     |
| --------------------------------------------------- | -------------- |
| Live packet capture (Scapy)                         | ✅ Hoàn thành  |
| Offline PCAP analysis                               | ✅ Hoàn thành  |
| L3/L4 packet decoder (IP, TCP, UDP, ICMP)           | ✅ Hoàn thành  |
| L7 HTTP parser (Method, URI, Headers, Body)         | ✅ Hoàn thành  |
| Snort-compatible rule parser                        | ✅ Hoàn thành  |
| Aho-Corasick multi-pattern matcher                  | ✅ Hoàn thành  |
| TCP flag-based detection (Nmap scans)               | ✅ Hoàn thành  |
| HTTP modifier matching (http_uri, http_client_body) | ✅ Hoàn thành  |
| PCRE regex matching                                 | ✅ Hoàn thành  |
| SQLAlchemy ORM + SQLite persistence                 | ✅ Hoàn thành  |
| FastAPI REST endpoint (`/api/alerts/`)              | ✅ Hoàn thành  |
| Demo PCAP script (`create_demo_pcap.py`)            | ✅ Hoàn thành  |
| AI anomaly detection (ML model)                     | 🔄 Giai đoạn 2 |
| Flow feature extractor                              | 🔄 Giai đoạn 2 |
| WebSocket real-time alert push                      | 🔄 Giai đoạn 2 |
| Frontend Dashboard                                  | 🔄 Giai đoạn 2 |
| Rule Management API (CRUD)                          | 🔄 Giai đoạn 2 |

---

_PBL4 – Trường Đại học Bách Khoa Đà Nẵng_
