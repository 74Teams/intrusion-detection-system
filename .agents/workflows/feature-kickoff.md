---
description: feature-kickoff Master Workflow V2. Điều phối toàn diện từ Ý tưởng thô -> Đặc tả SRS -> DB Schema -> API Specs -> Sequence Diagram -> Test Prep. Write your command content here.
---

# 🚀 Quy trình Khởi tạo Dự án Toàn diện (End-to-End Feature Pipeline)

Bạn là Tác nhân Điều phối trưởng (Chief Orchestrator). Nhiệm vụ của bạn là nhận một [Ý tưởng tính năng thô] từ người dùng, sau đó tự động kích hoạt tuần tự và song song các workflows con để biến ý tưởng đó thành một bộ tài liệu và môi trường kỹ thuật hoàn chỉnh sẵn sàng cho việc lập trình.

TUYỆT ĐỐI tuân thủ luồng thực thi 5 bước sau. BẮT BUỘC:

1. Sử dụng đầu ra (Output Artifact) của bước trước làm đầu vào (Input Context) cho bước sau.
2. TUÂN THỦ 100% quy tắc trong `@/rules/design-system.md` cho toàn bộ các thiết kế giao diện và component phát sinh.
3. VỚI MỖI QUY TRÌNH / BƯỚC: Mọi tài liệu Markdown (`.md`) được sinh ra (ví dụ: `srs.md`, `db_schema.md`, `api_spec.md`, `sequence.md`, `ai_spec.md`, `IMPLEMENTATION_MANIFEST.md`,...) BẮT BUỘC phải được lưu vào thư mục `.docs/[module]/[feature_name]/...` (ví dụ: `.docs/auth/verify_email/srs.md`, `.docs/auth/login/srs.md`, `.docs/users/users/users_srs.md`) và xuất/hiển thị đường dẫn (file link) kèm nội dung chính cho người dùng duyệt ở từng trạm kiểm duyệt (Checkpoint).


### Bước 1: Khởi tạo Đặc tả & Nghiệp vụ (Single Source of Truth)

- **Hành động:** Kích hoạt workflow `/generate-feature-spec` dựa trên ý tưởng thô của người dùng.
- **Mục tiêu:** Để bộ ba PM, BA, UX phối hợp cùng [Senior AI Engineer](.agents/skills/senior-ai-engineering/SKILL.md) (nếu tính năng có AI) sinh ra file Đặc tả Yêu cầu (SRS) chuẩn mực, bao gồm các yêu cầu về RAG Context, AI Persona và Guardrails.
- **Trạm kiểm duyệt (Checkpoint 1):** Dừng luồng. Hiển thị file `[feature_name]_srs.md` cho người dùng duyệt. Đợi người dùng gõ `Approve` mới đi tiếp.

### Bước 2: Khởi tạo Kiến trúc Dữ liệu (Database Foundation)

- **Đầu vào:** File SRS vừa được duyệt ở Bước 1.
- **Hành động:** Kích hoạt workflow `/generate-db-schema`.
- **Mục tiêu:** Chốt cấu trúc bảng, các trường dữ liệu và sơ đồ quan hệ (ERD).
- **Trạm kiểm duyệt (Checkpoint 2):** Dừng và hiển thị sơ đồ Mermaid ERD. Yêu cầu người dùng gõ `Approve` hoặc comment chỉnh sửa trước khi đi tiếp.

### Bước 3: Thiết kế Giao tiếp Hệ thống (Parallel Fan-Out)

- **Đầu vào:** File SRS (từ Bước 1) và Database Schema (từ Bước 2).
- **Hành động:** KHỞI CHẠY ĐỒNG THỜI 3 workflow sau để tiết kiệm thời gian:
  1. **Luồng 3A:** Kích hoạt `/generate-api-spec` để chốt API Contract (JSON, Status Code).
  2. **Luồng 3B:** Kích hoạt `/generate-sequence-diagram` để vẽ luồng tương tác giữa Client - Server - DB - 3rd Party.
  3. **Luồng 3C (AI & Agents):** Phối hợp với [Senior AI Engineer](.agents/skills/senior-ai-engineering/SKILL.md) thiết kế AI Architecture (RAG Data Sources, Agentic Tools, Prompt Templates). Xuất bản file `[feature_name]_ai_spec.md`.
- **Trạm kiểm duyệt (Checkpoint 3):** Tổng hợp API Spec, Sequence Diagram và AI Spec ra màn hình. Yêu cầu người dùng gõ `Approve`.

### Bước 4: Đảm bảo Chất lượng & Chuẩn bị Môi trường (QA Prep)

- **Đầu vào:** Toàn bộ kết quả từ Bước 1, Bước 2 và Bước 3 (SRS, DB, API, Sequence, AI Spec).
- **Hành động:** Kích hoạt workflow `/prepare-test-environment`.
- **Mục tiêu:**
  1. QA và Backend tạo dữ liệu mẫu (Seed Data/Mocks).
  2. Senior AI Engineer thiết kế bộ Test Cases cho AI (Accuracy Scoring, Backtesting prompts).
  3. Viết các script kiểm thử tự động (Automation Scripts) dọn đường cho Dev.

### Bước 5: Tối ưu hóa Hiệu năng & Chi phí (Optimization Loop)

- **Đầu vào:** Bản thảo thiết kế từ Bước 3 và Bước 4.
- **Hành động:** Kích hoạt workflow `/optimized-feature-performance`.
- **Mục tiêu:** Đảm bảo tính năng không chỉ chạy đúng mà còn chạy nhanh, rẻ và ổn định. Phối hợp giữa [Senior AI Engineer](.agents/skills/senior-ai-engineering/SKILL.md) và [Senior BA](.agents/skills/seniore-ba/SKILL.md).

### Bước 6: Hợp nhất & Đóng gói (Gather & Wrap-up)

- **Hành động:**
  1. Kiểm tra lại sự tồn tại của toàn bộ các file được sinh ra ở 5 bước trên (SRS, DB Schema, API Spec, Sequence, AI Spec, Performance Benchmarks).
  2. Tạo một file `IMPLEMENTATION_MANIFEST.md` tại thư mục gốc, chứa link liên kết tới toàn bộ các file kỹ thuật.
- **Đầu ra cuối cùng:** Thông báo "🎉 Giai đoạn Planning & Design đã hoàn tất 100%. Mọi thứ đã sẵn sàng để đội ngũ Dev tiến hành Vibe Coding!".
