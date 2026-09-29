---
trigger: always_on
---

# SYSTEM DESIGN RULES – NIDS BACKEND & DETECTION ENGINE

## 1. TỔNG QUAN HỆ THỐNG (SYSTEM OVERVIEW)

### 1.1. Định vị hệ thống

- **Tên dự án:** Hybrid NIDS (Rule-based & AI-driven Network Intrusion Detection System)
- **Mục tiêu:** Hệ thống phát hiện xâm nhập mạng theo thời gian thực kết hợp giữa kiểm tra luật tĩnh (Rule-based kiểu Snort) và phát hiện bất thường qua trí tuệ nhân tạo (AI/ML Traffic Worker).
- **Trọng tâm kỹ thuật:**
  - Bắt và giải mã gói tin thời gian thực với độ trễ thấp.
  - Phân tích sâu giao thức tầng ứng dụng (đặc biệt là HTTP).
  - So khớp quy tắc tốc độ cao (Aho-Corasick Multi-pattern matching).
  - Kết hợp mô hình AI phân loại bất thường mạng (DDoS, Scan, Anomalies).
  - Lưu trữ cảnh báo sự kiện và hỗ trợ Dashboard trực quan hóa.

### 1.2. Kiến trúc tổng thể (Dựa trên Architecture Diagram)

Hệ thống gồm 2 khối lớn:

1. **Traffic Ingestion (Thu nhận & Tiền xử lý lưu lượng)**:
   - `packet_decode.py`: Bắt gói tin (Live sniff hoặc đọc PCAP), bóc tách Ethernet -> IP -> TCP/UDP/ICMP.
   - `http_parser.py`: Trích xuất các vùng ứng dụng HTTP (Method, URI, Headers, Body, Status Code) để cung cấp cho Detection Engine.
   - Hàng đợi đệm bất đồng bộ (Queue): Tránh nghẽn I/O và rớt gói tin.
2. **Detection Analysis (Phân tích & Phát hiện)**:
   - `ids_realtime.py`: Bộ não so khớp luật theo thời gian thực (Fast Pattern Matching + Detailed Evaluation).
   - `manager_rules.py`: Nạp, phân tích cú pháp (parser), kiểm tra hợp lệ, quản lý tập luật (.rules).
   - `ai_worker.py`: Phân tích luồng lưu lượng (Flow Features) bằng mô hình học máy.
   - `event_database`: Lưu trữ sự kiện, cảnh báo (Alerts) và nhật ký lưu lượng.

### 1.3. Tech Stack cốt lõi

- **Ngôn ngữ:** Python 3.10+ (type hinting nghiêm ngặt)
- **Packet Ingestion:** `scapy` / `pypcap` / `dpkt` / `pcapy-ng`
- **Pattern Matching:** Thuật toán Aho-Corasick (`pyahocorasick`), Regular Expressions (`re`)
- **Database:** SQLite (giai đoạn dev) / PostgreSQL (giai đoạn production)
- **ORM / Database Access:** SQLAlchemy 2.0 hoặc Peewee / AsyncPG
- **AI / ML Worker:** `scikit-learn` / `xgboost` / `torch` (cho flow anomaly detection)
- **API & Dashboard Server:** FastAPI + WebSocket (phục vụ Real-time Alerts cho giao diện)

### 1.4. Nguyên tắc thiết kế

1. **Zero Packet Loss**: Ingestion module không được chạy logic nặng trực tiếp trong vòng lặp bắt gói. Phải ném vào Buffer/Queue.
2. **Phân tách rõ ràng (Decoupled Modules)**: Module bắt gói không phụ thuộc vào Database; Engine phát hiện giao tiếp qua Event Interface.
3. **Cú pháp Rule chuẩn hóa (Snort-compatible)**: Hỗ trợ cấu trúc Rule Header và Rule Options (đặc biệt các modifier HTTP).
4. **Structured Logging**: Mọi cảnh báo (Alert) phải có cấu trúc rõ ràng: Timestamp, SID, Severity, IP nguồn/đích, Port, Msg, Payload evidence.

---

## 2. CẤU TRÚC THƯ MỤC CHUẨN (FOLDER STRUCTURE)

```text
App/
├── rules/
│   ├── default.rules              # Các rule mặc định
│   ├── web_attacks.rules          # Rule SQLi, XSS, Path Traversal
│   └── dos_attacks.rules          # Rule phát hiện DoS/SYN Flood
│
├── services/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── packet_decode.py       # Bắt gói tin & giải mã tầng L2-L4
│   │   └── http_parser.py         # Bóc tách HTTP L7 regions
│   │
│   ├── detection/
│   │   ├── __init__.py
│   │   ├── ids_realtime.py        # Core Engine so khớp luật thời gian thực
│   │   ├── manager_rules.py       # Parser & Indexer cho tập luật .rules
│   │   └── pattern_matcher.py     # Cài đặt Aho-Corasick matcher
│   │
│   ├── ai_engine/
│   │   ├── __init__.py
│   │   ├── ai_worker.py           # Worker phân loại bất thường lưu lượng
│   │   ├── feature_extractor.py   # Trích xuất flow features (packet rate, size...)
│   │   └── models/                # File pre-trained model (.pkl / .onnx)
│   │
│   └── database/
│       ├── __init__.py            # Kết nối DB & Session Management
│       ├── models.py              # ORM Models (Event, Rule, TrafficLog)
│       └── repository.py          # Thao tác CRUD sự kiện & alert
│
├── api/                           # Backend API phục vụ Dashboard
│   ├── main.py                    # FastAPI server
│   ├── websocket.py               # Kênh bắn Alert thời gian thực
│   └── routes/                    # API xem alerts, quản lý rules
│
├── config/
│   ├── config.py                  # Load cấu hình (Interfaces, BPF, DB url)
│   └── settings.yaml              # File thiết lập hệ thống
│
├── main.py                        # Điểm khởi chạy toàn bộ tiến trình IDS
└── requirements.txt
```

---

## 3. QUY ƯỚC ĐẶC TẢ RULE (DETECTION RULE FORMAT)

Cú pháp tương thích Snort:

```text
[action] [proto] [src_ip] [src_port] [direction] [dst_ip] [dst_port] ( [options] )
```

### Các Option bắt buộc phải hỗ trợ:

1. `msg`: Thông điệp cảnh báo hiển thị trên giao diện.
2. `sid`: Mã định danh duy nhất của rule (Snort ID, ví dụ: `sid:1000001;`).
3. `rev`: Phiên bản cập nhật của rule (`rev:1;`).
4. `classtype`: Phân loại tấn công (ví dụ: `web-application-attack`, `attempted-recon`).
5. `priority` / `severity`: Mức độ nghiêm trọng (1: High, 2: Medium, 3: Low).
6. **Payload & HTTP Modifiers (Liên kết với `http_parser.py`)**:
   - `content`: Chuỗi hoặc hex cần tìm (`content:"SELECT";`).
   - `nocase`: Không phân biệt hoa/thường.
   - `http_uri`: Chỉ tìm kiếm bên trong URI path & query.
   - `http_client_body`: Chỉ tìm kiếm trong POST Body.
   - `http_header`: Chỉ tìm kiếm trong các header HTTP.
   - `http_method`: So khớp phương thức HTTP (`GET`, `POST`, `PUT`,...).
7. **Threshold & Detection Control**:
   - `threshold`: Giới hạn cảnh báo theo tần suất để chống bão alert.
