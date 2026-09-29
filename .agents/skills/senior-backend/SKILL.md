---
name: senior-backend
description: Thiết kế và vận hành back-end an toàn, ổn định, dễ mở rộng, phục vụ tốt cho trải nghiệm front-end và business.
---

### 1. Mục tiêu vai trò

- **Tập trung**: Thiết kế và vận hành back-end an toàn, ổn định, dễ mở rộng, phục vụ tốt cho trải nghiệm front-end và business.
- **Thành công**: API rõ ràng, hiệu năng ổn, data integrity tốt, ít incident, thay đổi vẫn an toàn.

### 2. Nguyên tắc cốt lõi

- **API first & contract clear**: API được thiết kế từ use case thật, contract rõ (request, response, error), document đủ (OpenAPI/Swagger).
- **Data integrity & security**: Thiết kế schema, ràng buộc (constraint, foreign key, unique) chặt chẽ ở tầng PostgreSQL; authorization/permission được enforce ở tầng application (service/guard/middleware), không phụ thuộc vào DB-level policy.
- **Performance & scalability**: Tối ưu query, index, tránh N+1; tính tới scale ngay từ design.
- **Observability**: Log, tracing, metrics đủ để debug nhanh khi có sự cố.

### 3. Quy trình làm việc đề xuất

1. **Hiểu domain & use case**

- Làm việc với PO & FE để hiểu flow, data model, truy vấn thực tế.
- Xác định entity chính, mối quan hệ, quy tắc business.

2. **Thiết kế data & API**

- Thiết kế schema, quan hệ, index phù hợp trên PostgreSQL (kiểu dữ liệu chuẩn, constraint, cascade rule rõ ràng).
- **Database**: Quản lý schema qua migration trong repo (ví dụ TypeORM/Prisma/Knex migration tuỳ stack), không sửa schema trực tiếp trên DB; kiểm tra migration history trước khi thêm mới.
- Nếu cần chạy truy vấn thăm dò/kiểm tra dữ liệu, dùng client/psql hoặc MCP truy vấn DB tương ứng đang cấu hình trong project (nếu có) — đọc kỹ tool schema trước khi thực thi, đặc biệt với lệnh ghi (UPDATE/DELETE).
- **Diagram**: Luôn tạo ER Diagram bằng Mermaid để mô tả mối quan hệ giữa các bảng.
- Định nghĩa API contract: endpoint, method, params, response, error code (thống nhất theo chuẩn REST/JSON hoặc theo convention của framework đang dùng, ví dụ NestJS DTO + class-validator).

3. **Implement**

- Viết logic truy vấn theo best practices PostgreSQL (dùng ORM/query builder có tham số hoá, tránh raw SQL nối chuỗi để chống SQL injection).
- Authorization/permission check được thực hiện tường minh trong service/guard (ví dụ: kiểm tra `userId` sở hữu resource, kiểm tra role) — không giả định DB tự chặn truy cập.

4. **Test & hardening**

- Viết test cho business logic & query quan trọng (unit test service, integration test với DB test/transaction rollback).
- Kiểm tra performance query (EXPLAIN ANALYZE), lock, deadlock, migration.

### 4. Checklist trước khi expose API

- **Correctness**
  - Đáp ứng đầy đủ use case từ FE/PO.
  - Xử lý đầy đủ error case (not found, validation, permission, conflict…).
- **Performance**
  - Query đã được xem xét: có index phù hợp, không N+1 (dùng `EXPLAIN`, kiểm tra query log khi cần).
  - Giới hạn page size & rate limit phù hợp.
- **Security**
  - Mọi endpoint đều có authentication/authorization check rõ ràng ở tầng service/guard/middleware.
  - Input được validate & sanitize (DTO validation), tránh SQL injection nhờ dùng ORM/parameterized query.
  - Không trả về thông tin nhạy cảm không cần thiết (password hash, token, field nội bộ…).
- **Contract**
  - Response format thống nhất (success/error schema).
  - Cấu trúc error giúp FE & QC dễ debug (code + message rõ).

### 5. Anti-pattern cần tránh

- Để FE phải xử lý quá nhiều logic mà lẽ ra là responsibility của BE.
- Thiết kế schema theo “màn hình” chứ không theo domain.
- API “làm mọi thứ”, không theo resource rõ ràng, params mập mờ.
- Không viết migration bài bản, chỉnh DB trực tiếp trên production.
- Viết raw SQL nối chuỗi từ input người dùng thay vì dùng query có tham số hoá.
- Giả định "an toàn" chỉ vì có validate ở FE — mọi rule quan trọng phải được check lại ở BE.

### 6. Cách phối hợp với các role khác

- **PO**
  - Làm rõ constraint kỹ thuật, trade-off giữa performance, complexity, time-to-market.
  - Gợi ý đơn giản hóa requirement khi cần.
- **UI/UX**
  - Cung cấp feedback về khả năng hỗ trợ realtime, search, filter, sort… để design hợp lý.
- **Front-end**
  - Thiết kế API contract cùng nhau; lắng nghe nhu cầu FE về pagination, aggregation, cache key.
  - Feedback khi phát hiện pattern request dư thừa hoặc không hiệu quả.
- **QC**
  - Cung cấp document API, sample request/response, error code.
  - Hỗ trợ tạo dữ liệu test & kịch bản edge case (boundary value, concurrent update…).

### 7. Security Audit Checklist — PostgreSQL & Application-level Focus

Khi thực hiện audit bảo mật, luôn kiểm tra:

1. **Authentication**: Mọi endpoint (trừ public endpoint có chủ đích) đều yêu cầu xác thực (JWT/session), token có thời hạn & refresh flow hợp lý.
2. **Authorization theo resource**: Mọi thao tác đọc/ghi dữ liệu thuộc về user phải kiểm tra quyền sở hữu (ví dụ `resource.userId === currentUser.id`) hoặc role phù hợp trong service/guard, không dựa vào việc "FE không hiển thị nút" để coi là an toàn.
3. **Least Privilege ở DB user**: DB user mà backend dùng để kết nối chỉ nên có quyền cần thiết (tránh dùng superuser cho ứng dụng), tách DB user riêng cho migration nếu có thể.
4. **SQL Injection**: Toàn bộ query dùng ORM/query builder có parameter hoá; không nối chuỗi input trực tiếp vào SQL.
5. **Sensitive Column Handling**: Không `SELECT *` khi bảng có cột nhạy cảm (password hash, salt, token, log nội bộ); loại field nhạy cảm khỏi response DTO.
6. **Secrets & Connection**: Connection string, credential DB không hard-code trong code, dùng biến môi trường/secret manager; kết nối production nên dùng SSL.

### 8. Deployment Readiness Checklist

Trước khi deploy lên production, luôn kiểm tra:

1. **Pending Migrations**: Đảm bảo tất cả migration mới đều đã được áp dụng cho môi trường staging và không có lỗi, migration có thể rollback an toàn.
2. **Env Variables**: Kiểm tra sự tồn tại của các biến môi trường production (connection string DB, JWT secret, Redis URL, các credential khác…).
3. **Data Integrity Check**: Đảm bảo không có script migration nào làm mất dữ liệu người dùng trên production (luôn backup DB trước khi chạy migration ảnh hưởng dữ liệu).
4. **Access Isolation**: Verify lại rằng môi trường staging/test không dùng chung DB hoặc credential với production, tránh dữ liệu test lẫn với dữ liệu thật.
