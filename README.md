# Hybrid NIDS (Rule-based & AI-driven Network Intrusion Detection System)

Hệ thống phát hiện xâm nhập mạng thời gian thực kết hợp giữa kiểm tra luật tĩnh (Rule-based kiểu Snort) và phát hiện bất thường qua trí tuệ nhân tạo (AI Flow Worker).

---

## 1. Cấu trúc thư mục dự án

```text
App/
├── config/
│   ├── config.py                 # Nạp cấu hình từ settings.yaml
│   └── settings.yaml             # Thiết lập Card mạng, BPF filter, CSDL, thư mục rules
│
├── rules/                        # Tập quy tắc phát hiện xâm nhập (.rules)
│   ├── web_attacks.rules         # Rule SQLi, XSS, Path Traversal, Command Injection
│   └── network_scans.rules       # Rule Nmap Xmas, Null, FIN, Ping Flood
│
├── services/
│   ├── ingestion/
│   │   ├── __init__.py           # Data structures: DecodedPacket, ParsedHTTPRequest
│   │   ├── packet_decode.py      # Bắt gói tin (Live/Offline PCAP) & giải mã L2-L4
│   │   └── http_parser.py        # Bóc tách tầng ứng dụng HTTP L7 (Method, URI, Body)
│   │
│   ├── detection/
│   │   ├── __init__.py           # Data structure: SnortRule
│   │   ├── ids_realtime.py       # Core Engine so khớp luật thời gian thực
│   │   ├── manager_rules.py      # Parser đọc & quản lý tập luật (.rules)
│   │   └── pattern_matcher.py    # Aho-Corasick Multi-pattern Matcher
│   │
│   ├── ai_engine/
│   │   ├── __init__.py
│   │   ├── feature_extractor.py  # Trích xuất đặc trưng luồng (Packet rate, SYN ratio)
│   │   └── ai_worker.py          # Worker AI phát hiện bất thường (DDoS, Scan)
│   │
│   └── database/
│       ├── __init__.py           # Kết nối Database (SQLite/PostgreSQL) & Session
│       ├── models.py             # SQLAlchemy ORM Models (Rule, Event, Payload)
│       └── repository.py         # CRUD thao tác lưu và truy vấn cảnh báo
│
├── api/                          # Backend API & WebSocket phục vụ Dashboard
│   ├── main.py                   # FastAPI server
│   └── routes/
│       └── alerts.py             # API danh sách Alerts
│
├── main.py                       # Điểm khởi chạy toàn bộ tiến trình NIDS
├── requirements.txt              # Danh sách thư viện phụ thuộc
└── README.md
```

---

## 2. Hướng dẫn cài đặt & Chạy hệ thống

### 2.1. Yêu cầu tiên quyết

1. **Python 3.10+**.
2. **Npcap Driver** (trên Windows): Tải tại [npcap.com](https://npcap.com/#download) và chọn _"Install Npcap in WinPcap API-compatible Mode"_. (Trên Linux chỉ cần cài `sudo apt install libpcap-dev`).

### 2.2. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 2.3. Khởi chạy NIDS Engine

> **Lưu ý**: Trên Windows, cần mở Command Prompt / PowerShell bằng quyền **Run as Administrator** để bắt gói tin mạng.

```bash
python main.py
```

### 2.4. Khởi chạy API Dashboard (Tùy chọn)

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Truy cập Swagger API docs tại: `http://localhost:8000/docs`.
