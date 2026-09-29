---
description: Phân tích kịch bản và tạo Biểu đồ Tuần tự (Sequence Diagram) mô tả luồng giao tiếp giữa Client, Server và Third-party (OAuth, Cloud).
---

# 🔄 Quy trình Thiết kế Biểu đồ Tuần tự (Sequence Diagram Workflow)

Bạn là Orchestrator (Người điều phối). Nhiệm vụ của bạn là điều hướng luồng công việc sau đây giữa `@senior-ba-specialist` và `@senior-backend` để tạo ra một Biểu đồ Tuần tự bằng cú pháp Mermaid.js cho kịch bản được yêu cầu.

TUYỆT ĐỐI tuân thủ trình tự 4 bước (SOP) dưới đây:

### Bước 1: Phân tích Kịch bản & Xác định Tác nhân (Thực thi bởi `@senior-ba-specialist`)

- **Đầu vào:** User Story hoặc mô tả kịch bản từ người dùng (Ví dụ: Luồng đăng nhập Google OAuth).
- **Hành động:**
  1. Xác định TẤT CẢ các đối tượng tham gia (Participants/Actors) vào luồng: Client (Web/App), Server (Backend), Database (PostgreSQL), và Đối tác thứ 3 (Google, Stripe...).
  2. Viết ra một danh sách liệt kê tuần tự các bước trao đổi thông tin (Data exchange) giữa các hệ thống này.
  3. Bắt buộc phải xác định các rẽ nhánh logic (Happy path - Thành công, và Unhappy path - Lỗi/Từ chối).
- **Đầu ra:** Bản nháp mô tả luồng sự kiện (Event flow).

### Bước 2: Thiết kế Biểu đồ Mermaid (Thực thi bởi `@senior-ba-specialist`)

- **Đầu vào:** Bản nháp từ Bước 1.
- **Hành động:** Chuyển đổi mô tả thành mã `Mermaid.js` (loại `sequenceDiagram`).
  1. Sử dụng cú pháp chuẩn xác: `->>` (Gửi yêu cầu), `-->>` (Trả về kết quả).
  2. Bắt buộc sử dụng `activate` và `deactivate` để thể hiện thời gian xử lý của từng hệ thống.
  3. Bắt buộc sử dụng khối `alt`, `else`, `opt` cho các rẽ nhánh (Ví dụ: Kiểm tra Token hợp lệ / Không hợp lệ).
  4. Ghi rõ payload/dữ liệu truyền đi trên các mũi tên (Ví dụ: `Client->>Server: POST /api/auth (id_token)`).
- **Đầu ra:** Mã Mermaid hoàn chỉnh của Biểu đồ Tuần tự.

### Bước 3: Kiểm duyệt Khả thi Kỹ thuật (Thực thi bởi `@senior-backend`)

- **Hành động:** Trình phối hợp yêu cầu `@senior-backend` review lại mã Mermaid do BA vừa vẽ.
- **Kiểm tra các yếu tố rủi ro:**
  - Luồng giao tiếp có thiếu bước bảo mật nào không (Ví dụ: Thiếu bước Backend gọi lên Google để verify `id_token`, hoặc thiếu bước cấp phát JWT/Session cookie)?
  - Tương tác với Supabase đã hợp lý chưa (RLS, Insert/Update user)?
- **Quyết định:** Nếu phát hiện lỗ hổng kỹ thuật, yêu cầu BA sửa lại mã Mermaid. Nếu đã chính xác hoàn toàn, chuyển sang Bước 4.

### Bước 4: Xuất bản và Lưu trữ (Thực thi bởi Orchestrator)

- **Hành động:**
  1. Đảm bảo thư mục `.docs/sequence-diagrams/` tồn tại trong dự án.
  2. Lưu mã Mermaid kèm một đoạn giải thích ngắn gọn vào tệp `.docs/sequence-diagrams/[scenario_name].md`.
- **Đầu ra cuối cùng:**
  - Render (hiển thị) trực tiếp biểu đồ Mermaid ra màn hình chat.
  - Hiển thị thông báo hoàn thành kèm đường dẫn tới tệp vừa lưu để Developer sẵn sàng viết code.
