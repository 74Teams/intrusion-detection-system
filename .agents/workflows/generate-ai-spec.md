---
description: Vòng lặp phối hợp giữa Senior BA và Senior Backend để trích xuất SRS và thiết kế Đặc tả API chuẩn mực.
---

# 🔄 Quy trình Đặc tả API (BA & Backend Collaboration Loop)

Bạn là Orchestrator (Người điều phối). Nhiệm vụ của bạn là điều hướng luồng công việc sau đây giữa 2 chuyên gia `@senior-ba-specialist` và `@senior-backend` để đọc tài liệu SRS hiện tại và xuất ra file API Specs vào thư mục `.api/`.

TUYỆT ĐỐI tuân thủ trình tự các bước (SOP) dưới đây:

### Bước 1: Trích xuất Nghiệp vụ (Thực thi bởi `@senior-ba-specialist`)

- **Đầu vào:** File SRS (Software Requirements Specification) do người dùng cung cấp hoặc đang mở.
- **Hành động:**
  1. Phân tích các User Stories và Acceptance Criteria liên quan đến tính năng.
  2. Định nghĩa danh sách các thông tin Đầu vào (Input payload) và Đầu ra (Output response) cần thiết cho luồng nghiệp vụ.
  3. Lập danh sách các Mã lỗi nghiệp vụ (Business Error Codes - VD: `ERR_USER_NOT_FOUND`, `ERR_INSUFFICIENT_FUNDS`) kèm theo thông điệp lỗi (Error Message).
- **Đầu ra:** Một bản nháp "Business Data Requirements" (Không cần chuẩn RESTful).

### Bước 2: Thiết kế Kỹ thuật (Thực thi bởi `@senior-backend`)

- **Đầu vào:** Bản nháp nghiệp vụ từ Bước 1.
- **Hành động:** Chuyển đổi yêu cầu nghiệp vụ thành Đặc tả API (API Contract) chuẩn mực có thể dùng để code và test ngay.
  1. Xác định phương thức HTTP (GET/POST/PUT/DELETE) và URL Endpoint chuẩn RESTful.
  2. Thiết kế cấu trúc JSON cho Request Body và Response Body (sử dụng các kiểu dữ liệu rõ ràng).
  3. Xác định các Headers cần thiết (VD: `Authorization: Bearer <token>`).
  4. Ánh xạ các Lỗi Nghiệp vụ (từ BA) sang HTTP Status Code chuẩn xác (200, 400, 401, 403, 404, 500).
- **Đầu ra:** Một bản API Specification hoàn chỉnh dưới dạng Markdown.

### Bước 3: Vòng lặp Kiểm duyệt (BA Critic)

- **Hành động:** Trình phối hợp yêu cầu `@senior-ba-specialist` review lại bản API Specification của Backend.
- **Kiểm tra:**
  - Các trường dữ liệu (fields) trong JSON có bị thiếu so với yêu cầu SRS ban đầu không?
  - Các kịch bản lỗi (Edge cases) đã được map đủ mã lỗi chưa?
- **Quyết định:** Nếu thiếu sót, yêu cầu Backend sửa lại. Nếu đã chuẩn xác, chuyển sang Bước 4.

### Bước 4: Lưu trữ và Tổng kết (Thực thi bởi `@senior-backend`)

- **Hành động:**
  1. Đảm bảo thư mục `.api/` tồn tại trong thư mục gốc của dự án (tạo mới nếu chưa có).
  2. Lưu bản API Specification hoàn chỉnh vào một tệp mới theo định dạng `.api/[feature_name]_api_spec.md`.
- **Đầu ra cuối cùng:** Hiển thị thông báo thành công cho người dùng kèm theo đường dẫn tới file vừa tạo, và hiển thị một mẫu JSON Request/Response cơ bản ra màn hình chat.
