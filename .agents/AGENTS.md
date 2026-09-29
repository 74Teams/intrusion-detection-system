# Git Commit Rules

- KHÔNG tự động thực hiện các câu lệnh `git commit` hoặc `git push` mà chưa có sự đồng ý trực tiếp từ người dùng.
- KHÔNG tự động merge code vào nhánh `main` khi chưa tạo Pull Request để người dùng review và approve trên GitHub.
- Mọi khi chuẩn bị commit code, agent BẮT BUỘC phải hỏi ý kiến người dùng và cung cấp các lựa chọn rõ ràng:
  - **Accept**: Tiến hành commit với thông điệp đề xuất và push Feature Branch (không tự động merge sang main).
  - **Reject**: Bỏ qua commit và giữ nguyên trạng thái làm việc hiện tại.

# Feature Kickoff Workflow Rules

- Khi thực thi quy trình `/feature-kickoff` (hoặc các quy trình con thuộc feature-kickoff):
  - Mọi tài liệu Markdown (`.md`) được sinh ra ở từng bước (ví dụ: `[feature_name]_srs.md`, `[feature_name]_db_schema.md`, `[feature_name]_api_spec.md`, `[feature_name]_sequence.md`, `[feature_name]_ai_spec.md`, `IMPLEMENTATION_MANIFEST.md`, v.v.) BẮT BUỘC phải được lưu trữ trong thư mục cấu trúc: `.docs/[module]/[feature_name]/...` (ví dụ: `.docs/auth/verify_email/srs.md`, `.docs/auth/verify_email/db_schema.md`, v.v.).
  - Đồng thời BẮT BUỘC phải xuất/hiển thị đường dẫn file (file link) và nội dung chính của từng file `.md` sinh ra cho người dùng xem và xác nhận (Approve) ở mỗi trạm kiểm duyệt (Checkpoint).
