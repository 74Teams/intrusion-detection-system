# ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS) – HYBRID NIDS CORE ENGINE

- **Tên dự án:** Hybrid NIDS (Rule-based & AI-driven Network Intrusion Detection System)
- **Module:** `nids`
- **Feature:** `core_engine`
- **Phiên bản tài liệu:** 1.0.0
- **Trạng thái:** Chờ phê duyệt (Pending Approval)

---

## 1. TỔNG QUAN HỆ THỐNG & MỤC TIÊU NGHIỆP VỤ

### 1.1. Mục tiêu

Xây dựng một hệ thống phát hiện xâm nhập mạng (NIDS) thời gian thực theo kiến trúc lai (Hybrid):

1. **Rule-based Engine (Tĩnh)**: Tương thích cú pháp Snort, phân tích sâu gói tin L3–L4 và bóc tách L7 (HTTP) với độ trễ tối thiểu, không làm nghẽn luồng mạng.
2. **AI Engine (Động - Mở rộng)**: Phân loại luồng lưu lượng (Flow Anomaly) nhằm phát hiện các hành vi bất thường, tấn công DoS/DDoS và rà quét (Reconnaissance).
3. **Event Persistence & Visualization**: Lưu vết cảnh báo chi tiết vào MySQL và hỗ trợ API/WebSocket phục vụ giám sát.

### 1.2. Đối tượng sử dụng (Stakeholders / Personas)

- **Giảng viên / Hội đồng đánh giá PBL4**: Đánh giá kiến trúc kỹ thuật, độ phức tạp thuật toán, khả năng so khớp luật chính xác và khả năng tự giải thích/vận hành hệ thống.
- **Quản trị viên mạng (SOC Analyst / Network Admin)**: Theo dõi cảnh báo theo thời gian thực, điều chỉnh tập luật (.rules), tra cứu lịch sử sự cố an ninh mạng.

---

## 2. PHẠM VI CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

### FR-01: Thu nhận lưu lượng mạng (Packet Ingestion)

- **FR-01.1 (Live Mode)**: Lắng nghe liên tục trên card mạng vật lý/ảo ở chế độ Promiscuous thông qua Npcap/Scapy.
- **FR-01.2 (Offline Mode)**: Đọc và phát lại file định dạng `.pcap` để phục vụ kiểm thử, tái hiện tấn công hoặc đánh giá benchmark.
- **FR-01.3 (BPF Filter)**: Cho phép cấu hình bộ lọc Berkeley Packet Filter (mặc định: `ip`) từ file thiết lập.
- **FR-01.4 (Asynchronous Buffer)**: Thu nhận raw packet và ném ngay vào hàng đợi bất đồng bộ (`queue.Queue`) với dung lượng đệm cấu hình được (mặc định: 10,000 packets) để đạt tiêu chí _Zero Packet Loss_.

### FR-02: Phân tích & Giải mã giao thức (Packet Decoding)

- **FR-02.1 (L3/L4 Parsing)**: Trích xuất IP nguồn, IP đích, giao thức (TCP, UDP, ICMP), cổng nguồn, cổng đích.
- **FR-02.2 (TCP Flags Inspection)**: Giải mã trạng thái các cờ điều khiển TCP: SYN, ACK, FIN, RST, PSH, URG và chuỗi cờ thô (raw flags) để nhận diện các dạng scan (Xmas, Null, FIN, SYN-FIN).
- **FR-02.3 (HTTP L7 Deep Packet Inspection)**: Khi gói tin đi qua các cổng dịch vụ Web (80, 8080, 8000, 3000, 5000), hệ thống tự động bóc tách các vùng:
  - `Method`: GET, POST, PUT, DELETE, OPTIONS, HEAD...
  - `URI & Query`: Path và các tham số truy vấn URL đã URL-decode.
  - `Headers`: Danh sách headers dạng Key-Value chuẩn hóa lowercase.
  - `Body`: Payload thân tin nhắn HTTP (phục vụ bắt POST XSS/SQLi).

### FR-03: Quản lý tập luật (Rule Management)

- **FR-03.1 (Snort-compatible Syntax)**: Hỗ trợ cấu trúc Rule chuẩn:
  `[action] [proto] [src_ip] [src_port] -> [dst_ip] [dst_port] ( [options] )`
- **FR-03.2 (Options Parser)**: Phân tích các trường bắt buộc:
  - Meta: `msg`, `sid`, `rev`, `classtype`, `severity`/`priority`.
  - Detection: `content`, `nocase`, `flags`, `pcre`.
  - HTTP Modifiers: `http_uri`, `http_client_body`, `http_header`, `http_method`.
- **FR-03.3 (Memory Indexing)**: Nạp toàn bộ tập luật từ thư mục `rules/` vào RAM khi khởi động, quản lý theo SID duy nhất.

### FR-04: So khớp luật thời gian thực (Real-time Detection Engine)

- **FR-04.1 (Multi-stage Filtering)**: Lọc phân tầng: Protocol $\rightarrow$ Port $\rightarrow$ TCP Flags $\rightarrow$ Content/PCRE.
- **FR-04.2 (Region-targeted Matching)**: Nếu rule chỉ định modifier (ví dụ: `http_uri`), engine chỉ tìm kiếm chuỗi trong vùng dữ liệu đó, loại bỏ việc tìm kiếm vô nghĩa trên toàn bộ payload.
- **FR-04.3 (Regex/PCRE Support)**: Hỗ trợ so khớp mẫu phức tạp bằng biểu thức chính quy (Regular Expressions).

### FR-05: Cảnh báo & Lưu trữ sự kiện (Alerting & Database Persistence)

- **FR-05.1 (Console Logging)**: In cảnh báo có cấu trúc ra màn hình terminal ngay khi phát hiện vi phạm: `[ALERT #ID] [SID:xxx] msg | src -> dst`.
- **FR-05.2 (Database Ingestion)**: Lưu trữ cảnh báo vào MySQL database (bảng `events`), lưu vết đầy đủ timestamp, IP, Port, loại tấn công, mức độ nghiêm trọng.
- **FR-05.3 (Data Integrity)**: Tự động khởi tạo database và schema (`ensure_database_exists`) nếu chưa tồn tại.

---

## 3. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS)

### NFR-01: Hiệu năng & Khả năng chịu tải (Performance)

- Hệ thống xử lý được tối thiểu 500-1000 packets/giây trên môi trường kiểm thử mà không bị đầy hàng đợi đệm.
- Độ trễ phát hiện (Detection Latency) từ lúc gói tin chạm card mạng đến khi xuất Alert < 50ms.

### NFR-02: Tính sẵn sàng & Chống Crash (Reliability)

- Xử lý ngoại lệ toàn diện: Gói tin lỗi cấu trúc (malformed packet) hoặc payload mã hóa không được làm dừng tiến trình bắt gói chính.
- Quản lý kết nối CSDL có Connection Pool (tự phục hồi khi mất kết nối MySQL).

### NFR-03: Tính tương thích & Cấu hình (Portability)

- Chạy trên hệ điều hành Windows 10/11 (với Npcap) và Linux (với libpcap).
- Tập trung mọi tham số nhạy cảm và thông số hệ thống vào file `config/settings.yaml`.

---

## 4. MA TRẬN PHÁT HIỆN TẤN CÔNG (ATTACK MATRIX)

| SID         | Loại tấn công         | Mẫu nhận diện (Signature)                                     | Mức độ     |
| :---------- | :-------------------- | :------------------------------------------------------------ | :--------- |
| **1000001** | SQL Injection         | `content:"union"; content:"select"; nocase; http_uri;`        | High (1)   |
| **1000002** | SQL Injection         | `content:"or"; pcre:"/or\s+['"]?\d+['"]?\s*=\s*['"]?\d+/i";`  | High (1)   |
| **1000003** | SQL Injection         | `content:"--"; http_uri;`                                     | Medium (2) |
| **1000010** | Stored/Reflected XSS  | `content:"<script"; nocase; http_uri;`                        | High (1)   |
| **1000012** | Event Handler XSS     | `pcre:"/on(error\|load\|mouseover)\s*=/i"; http_client_body;` | High (1)   |
| **1000020** | Path Traversal / LFI  | `content:"../"; http_uri;`                                    | High (1)   |
| **1000021** | Sensitive File Access | `content:"/etc/passwd"; http_uri;`                            | High (1)   |
| **1000030** | Command Injection     | `pcre:"/(\|\s*id\|;\s*cat\s+\|&\s*whoami)/i"; http_uri;`      | High (1)   |
| **1000100** | Nmap Xmas Scan        | `flags:FUP;` (Cờ FIN, URG, PSH bật đồng thời)                 | Medium (2) |
| **1000101** | Nmap Null Scan        | `flags:0;` (Không bật bất kỳ cờ TCP nào)                      | Medium (2) |
| **1000102** | Nmap FIN Scan         | `flags:F;` (Chỉ bật duy nhất cờ FIN)                          | Medium (2) |
| **1000103** | SYN-FIN Anomaly       | `flags:SF;` (Bật đồng thời cả SYN và FIN)                     | High (1)   |
