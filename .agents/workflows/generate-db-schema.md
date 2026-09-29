---
description: Vòng lặp phối hợp giữa Senior BA và Senior Backend để thiết kế Cơ sở dữ liệu từ mức khái niệm (Logical ERD) đến mức vật lý (Physical Schema).
---

# 🔄 Quy trình Thiết kế Cơ sở Dữ liệu (BA & Backend Database Loop)

Bạn là Orchestrator (Người điều phối). Nhiệm vụ của bạn là điều hướng luồng công việc sau đây giữa 2 chuyên gia `@senior-ba-specialist` và `@senior-backend` để đọc tài liệu yêu cầu (SRS/PRD) và xuất ra bản thiết kế Database hoàn chỉnh vào thư mục `.db/`.

TUYỆT ĐỐI tuân thủ trình tự 4 bước (SOP) dưới đây:

### Bước 1: Thiết kế Mức Khái niệm/Logic (Thực thi bởi `@senior-ba-specialist`)

- **Đầu vào:** Tệp PRD/SRS hoặc mô tả yêu cầu tính năng từ người dùng.
- **Hành động:**
  1. Phân tích nghiệp vụ để tìm ra TẤT CẢ các thực thể (Entities) cần thiết (Ví dụ: User, Order, Session...).
  2. Xác định các thuộc tính nghiệp vụ cốt lõi của từng thực thể (Không cần quan tâm kiểu dữ liệu kỹ thuật, chỉ cần biết nó lưu thông tin gì).
  3. Xác định mối quan hệ giữa các thực thể: 1-1 (One-to-One), 1-N (One-to-Many), N-N (Many-to-Many).
  4. Vẽ một sơ đồ Logical ERD sử dụng cú pháp `Mermaid.js`.
- **Đầu ra:** Bản nháp "Logical Entity-Relationship Document".

### Bước 2: Thiết kế Mức Vật lý (Thực thi bởi `@senior-backend`)

- **Đầu vào:** Bản nháp Logical ERD từ Bước 1.
- **Hành động:** Chuyển đổi mô hình khái niệm thành Physical Database Schema chuẩn mực cho kỹ thuật.
  1. Chuẩn hóa tên bảng và tên cột (Sử dụng `snake_case` hoặc `camelCase` tùy chuẩn dự án).
  2. Quyết định kiểu dữ liệu cụ thể (Ví dụ: `VARCHAR(255)`, `UUID`, `JSONB`, `TIMESTAMP WITH TIME ZONE`).
  3. Thiết lập Khóa chính (Primary Key - PK) và Khóa ngoại (Foreign Key - FK) để tạo ràng buộc toàn vẹn.
  4. Đề xuất các Index (Chỉ mục) cần thiết dựa trên các trường thường xuyên được truy vấn.
  5. Viết mã DDL (Data Definition Language) bằng SQL hoặc định dạng ORM (như Prisma schema / Supabase schema).
- **Đầu ra:** Một bản "Physical Database Schema" kèm theo mã nguồn khởi tạo bảng.

### Bước 3: Vòng lặp Đối chiếu (BA Critic)

- **Hành động:** Trình phối hợp yêu cầu `@senior-ba-specialist` rà soát lại bản thiết kế vật lý của Backend.
- **Kiểm tra:**
  - Các bảng vật lý đã đủ để lưu trữ tất cả thông tin mà User Story yêu cầu chưa?
  - Mối quan hệ Khóa ngoại (FK) có đúng với logic nghiệp vụ (Ví dụ: Xóa User thì có xóa Order không - CASCADE)?
- **Quyết định:** Nếu thiếu sót, yêu cầu Backend sửa lại mã DDL. Nếu đã chuẩn xác, chuyển sang Bước 4.

### Bước 4: Lưu trữ và Tổng kết (Thực thi bởi `@senior-backend`)

- **Hành động:**
  1. Đảm bảo thư mục `.db/` tồn tại trong gốc dự án.
  2. Lưu toàn bộ thiết kế (bao gồm Sơ đồ Mermaid ERD và mã SQL/Schema) vào một tệp mới theo định dạng `.db/[feature_name]_schema.md` (hoặc `.sql`).
- **Đầu ra cuối cùng:** Hiển thị thông báo hoàn thành cho người dùng, đính kèm đường dẫn tệp vừa tạo và render sơ đồ Mermaid ERD ra màn hình chat để người dùng duyệt nhanh.
