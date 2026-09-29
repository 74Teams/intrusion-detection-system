# SƠ ĐỒ TUẦN TỰ HỆ THỐNG (SEQUENCE DIAGRAM) – HYBRID NIDS CORE ENGINE

- **Module:** `nids`
- **Feature:** `core_engine`

---

## 1. LUỒNG XỬ LÝ GÓI TIN THỜI GIAN THỰC (REAL-TIME DETECTION PIPELINE)

Sơ đồ mô tả hành trình từ lúc gói tin chạm Card mạng qua hai tầng phân tích (Rule Engine & AI) đến khi lưu MySQL và bắn WebSocket Alert ra Dashboard:

```mermaid
sequenceDiagram
    autonumber
    actor Attacker as Kẻ tấn công / Mạng ngoài
    participant NIC as Card mạng (Npcap Driver)
    participant Capture as packet_capture.py
    participant Queue as packet_queue (Buffer)
    participant Decoder as packet_decoder.py
    participant HTTP as http_parser.py
    participant Engine as ids_realtime.py (Rule Engine)
    participant AI as ai_worker.py (AI Engine)
    participant DB as MySQL Database
    participant WS as WebSocket Clients (Dashboard)

    Note over NIC,Capture: Giai đoạn 1: Bắt gói tin không khóa (Non-blocking Ingestion)
    Attacker->>NIC: Gửi gói tin TCP độc hại (SQLi / Xmas Scan)
    NIC->>Capture: Bắt gói tin thô (Promiscuous Mode)
    Capture->>Queue: put_nowait(raw_packet)
    Note right of Capture: Không xử lý nặng, tránh nghẽn NIC (Zero Packet Loss)

    Note over Queue,Engine: Giai đoạn 2: Bóc tách & Phân tích bất đồng bộ
    Queue->>Decoder: worker_thread lấy packet ra
    Decoder->>Decoder: Trích xuất L3 (IP) và L4 (TCP/UDP, Flags)

    alt Nếu là cổng Web ($HTTP_PORTS: 80, 8080...)
        Decoder->>HTTP: Gửi raw_payload
        HTTP-->>Decoder: Trả về ParsedHTTPRequest (Method, URI, Headers, Body)
    end

    Decoder->>Engine: evaluate_packet(DecodedPacket)

    par So khớp luật tĩnh
        Engine->>Engine: Kiểm tra Protocol & Port Filter
        Engine->>Engine: So khớp TCP Flags (FUP, SF...)
        Engine->>Engine: Quét chuỗi vùng HTTP (URI/Body) hoặc Raw
        alt Phát hiện vi phạm luật (Signature Matched)
            Engine->>DB: EventRepository.save_alert(alert_data)
            DB-->>Engine: Xác nhận lưu thành công (Event ID)
            Engine->>WS: Broadcast NEW_ALERT event
        end
    and Phân tích hành vi động (AI Flow)
        Decoder->>AI: analyze_packet(DecodedPacket)
        AI->>AI: Cập nhật Flow Feature (Packet rate, SYN ratio)
        opt Nếu vượt ngưỡng bất thường (Anomaly Detected)
            AI->>DB: save_alert(AI-ANOMALY)
            AI->>WS: Broadcast AI Anomaly Alert
        end
    end
```

---

## 2. LUỒNG KHỞI ĐỘNG HỆ THỐNG (SYSTEM BOOTSTRAP SEQUENCE)

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Người vận hành
    participant Main as main.py
    participant Settings as config/settings.yaml
    participant DB as MySQL (Docker)
    participant RuleMgr as manager_rules.py
    participant Engine as ids_realtime.py
    participant Capture as packet_capture.py

    Admin->>Main: Chạy `python main.py`
    Main->>Settings: Nạp cấu hình (DB, BPF, Ports)
    Main->>DB: init_db() & ensure_database_exists()
    DB-->>Main: CSDL và các bảng đã sẵn sàng

    Main->>RuleMgr: load_all_rules("rules/")
    RuleMgr->>RuleMgr: Đọc và parse *.rules
    RuleMgr-->>Main: Đã nạp 14 rules vào RAM

    Main->>Engine: Khởi tạo DetectionEngine(rule_manager)
    Engine->>Engine: Xây dựng bộ so khớp nhanh (Automaton)

    Main->>Capture: start_live(interface)
    Note over Capture: Lắng nghe liên tục trên card mạng
```
