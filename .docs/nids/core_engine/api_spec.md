# ĐẶC TẢ GIAO DIỆN LẬP TRÌNH ỨNG DỤNG (API SPECIFICATION) – HYBRID NIDS

- **Module:** `nids`
- **Feature:** `core_engine`
- **Giao thức:** HTTP/1.1 RESTful + WebSocket (Real-time Stream)
- **Base URL:** `http://localhost:8000/api`
- **Định dạng dữ liệu:** `application/json` (UTF-8)

---

## 1. TỔNG QUAN DANH SÁCH ENDPOINTS

| Nhóm        | Method | Endpoint         | Mô tả                                                   |
| :---------- | :----- | :--------------- | :------------------------------------------------------ |
| **System**  | `GET`  | `/health`        | Kiểm tra tình trạng hoạt động của NIDS Engine           |
| **Alerts**  | `GET`  | `/alerts`        | Lấy danh sách sự kiện cảnh báo (hỗ trợ phân trang, lọc) |
| **Alerts**  | `GET`  | `/alerts/{id}`   | Lấy chi tiết một cảnh báo kèm payload forensic evidence |
| **Rules**   | `GET`  | `/rules`         | Lấy danh sách các rule đang kích hoạt trong hệ thống    |
| **Rules**   | `POST` | `/rules/reload`  | Nạp lại (reload) các file `.rules` từ đĩa vào RAM       |
| **Metrics** | `GET`  | `/stats/summary` | Thống kê số lượng alerts theo severity, top attacker IP |
| **Stream**  | `WS`   | `/ws/alerts`     | Kênh WebSocket đẩy cảnh báo thời gian thực tới UI       |

---

## 2. CHI TIẾT CÁC ENDPOINT REST API

### 2.1. Kiểm tra trạng thái hệ thống

- **Endpoint:** `GET /api/health`
- **Response (200 OK):**

```json
{
  "status": "HEALTHY",
  "engine": "Hybrid NIDS Core",
  "version": "1.0.0",
  "uptime_seconds": 12450,
  "loaded_rules": 14,
  "queue_size": 12,
  "db_connected": true
}
```

---

### 2.2. Danh sách cảnh báo tấn công (Alerts List)

- **Endpoint:** `GET /api/alerts`
- **Query Parameters:**
  - `limit` (int, default: 50, max: 200): Số lượng bản ghi lấy về.
  - `offset` (int, default: 0): Bản ghi bắt đầu (phân trang).
  - `severity` (int, optional): Lọc theo độ nghiêm trọng (1, 2, 3).
  - `src_ip` (string, optional): Lọc theo địa chỉ IP nguồn.
  - `status` (string, optional): Lọc theo trạng thái (`NEW`, `RESOLVED`).

- **Response (200 OK):**

```json
{
  "total": 128,
  "limit": 50,
  "offset": 0,
  "data": [
    {
      "id": 1052,
      "timestamp": "2026-09-28T20:30:15Z",
      "sid": 1000001,
      "source_type": "RULE_ENGINE",
      "attack_type": "web-application-attack",
      "severity": 1,
      "src_ip": "192.168.1.45",
      "src_port": 54210,
      "dst_ip": "192.168.1.10",
      "dst_port": 80,
      "protocol": "TCP",
      "http_method": "GET",
      "http_uri": "/search?q=1+union+select+1,2,3",
      "summary": "WEB-ATTACK SQL Injection - UNION SELECT detected",
      "status": "NEW"
    }
  ]
}
```

---

### 2.3. Chi tiết cảnh báo & Bằng chứng Forensic

- **Endpoint:** `GET /api/alerts/{id}`
- **Response (200 OK):**

```json
{
  "id": 1052,
  "timestamp": "2026-09-28T20:30:15Z",
  "sid": 1000001,
  "severity": 1,
  "src_ip": "192.168.1.45",
  "src_port": 54210,
  "dst_ip": "192.168.1.10",
  "dst_port": 80,
  "protocol": "TCP",
  "summary": "WEB-ATTACK SQL Injection - UNION SELECT detected",
  "payload_evidence": {
    "matched_content": "union select",
    "http_headers": "host: 192.168.1.10\r\nuser-agent: sqlmap/1.7\r\naccept: */*",
    "http_body": "",
    "packet_raw_hex": "4500003c1c4640004006..."
  }
}
```

- **Response (404 Not Found):**

```json
{
  "detail": "Alert with ID 1052 not found"
}
```

---

### 2.4. Quản lý tập luật (Rule Management)

- **Endpoint:** `GET /api/rules`
- **Response (200 OK):**

```json
{
  "total_rules": 14,
  "rules": [
    {
      "sid": 1000001,
      "msg": "WEB-ATTACK SQL Injection - UNION SELECT detected",
      "protocol": "tcp",
      "dst_port": "$HTTP_PORTS",
      "severity": 1,
      "classtype": "web-application-attack",
      "is_enabled": true
    }
  ]
}
```

- **Endpoint:** `POST /api/rules/reload`
- **Response (200 OK):**

```json
{
  "success": true,
  "message": "Reloaded rules successfully",
  "reloaded_rules_count": 14
}
```

---

## 3. WEBSOCKET REAL-TIME ALERTS CONTRACT

Kênh kết nối hai chiều đẩy cảnh báo trực tiếp từ Detection Engine ra giao diện Dashboard:

- **URL:** `ws://localhost:8000/api/ws/alerts`
- **Format Frame (Server $\rightarrow$ Client JSON):**

```json
{
  "event": "NEW_ALERT",
  "data": {
    "id": 1053,
    "timestamp": "2026-09-28T20:35:00Z",
    "sid": 1000100,
    "msg": "SCAN Nmap Xmas Scan detected (FUP flags)",
    "severity": 2,
    "src_ip": "10.0.0.99",
    "src_port": 44444,
    "dst_ip": "192.168.1.10",
    "dst_port": 22
  }
}
```
