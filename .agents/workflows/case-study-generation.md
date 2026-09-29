---
description: Pipeline AI Multi-Agent tạo Case Study thực chiến (PM Battle).
---

# Case Study Generation Workflow

Workflow này mô tả quy trình AI Multi-Agent tự động chuyển đổi các ý tưởng thô (Seed Notes) thành các bài Case Study thực chiến chất lượng cao, bám sát thị trường Việt Nam và có bộ tiêu chí đánh giá khắt khe.

## Tổng quan Pipeline

Quy trình được điều phối bởi `lib/services/caseStudyAiService.ts`, sử dụng Gemini qua các giai đoạn dưới đây. API `POST /api/admin/case-studies/generate` sau khi trả **202** vẫn **giữ runtime** bằng `waitUntil()` (package `@vercel/functions`) để pipeline chạy xong trên Vercel; kèm `maxDuration = 300` trên route.

**Seed Notes (Context user):** Researcher nhận `seedNotes` + bắt web search; prompt yêu cầu không chỉ dựa seed nhưng **phải phản ánh** chi tiết bài toán user trong `situation_raw` / `complication_raw`. Case Writer nhận thêm khối **USER SEED** (nguyên văn `seedNotes`) để đề bài bám ý user, bổ sung từ SCQ/RAG.

---

## Phase 1: Tri thức tham chiếu (RAG Context)

**Mục tiêu**: Tìm kiếm các Case Study có sẵn để AI học hỏi cấu trúc và độ khó.

- **Action**: Sử dụng model `gemini-embedding-001` để vector hóa `seedNotes`.
- **Logic**: Gọi RPC `match_case_studies` trong Supabase để lấy 5 nguồn tham khảo gần nhất.

## Phase 2: Phân tích vấn đề (Researcher Agent)

**Mục tiêu**: Bóc tách bối cảnh thô thành "nguyên liệu" sắc bén và mang tính đánh đố.

- **Agent Roles**: [Researcher Agent](file:///Users/truongtritin/Github/tuhocproductv2/lib/ai/case-study-generation/researcherPrompts.ts)
- **Luật sinh tồn**:
  - **No Textbook**: Không tạo bài toán hoàn hảo, môi trường phải hỗn loạn.
  - **Trade-offs**: Bắt buộc có các mục tiêu kinh doanh triệt tiêu lẫn nhau.
  - **Data Blindspots**: Tạo ra sự đa dạng ngẫu nhiên về lỗi dữ liệu (không dùng con số dập khuôn).
- **Output**: JSON chứa `situation_raw`, `complication_raw`, `business_goals`, `audience_profile`.

## Phase 3: Bản địa hóa & SCQ (Localizer Agent)

**Mục tiêu**: Chuyển đổi dữ liệu thô sang khung SCQ và áp dụng sắc thái thị trường Việt Nam.

- **Agent Roles**: [Localizer Agent](file:///Users/truongtritin/Github/tuhocproductv2/lib/ai/case-study-generation/localizerPrompts.ts)
- **Đặc thù Việt Nam**: Lồng ghép thói quen COD, tâm lý săn khuyến mãi, Nghị định 13 (bảo vệ dữ liệu), và văn hóa dùng Zalo/MoMo.
- **Output**: JSON chứa `scq_situation`, `scq_complication`, `scq_question`, `localized_constraints`.

## Phase 4: Thiết kế nội dung (Case Writer Agent)

**Mục tiêu**: Lắp ghép dữ liệu thành một đề bài Case Study chuẩn MECE sắc bén.

- **Agent Roles**: [Case Writer Agent](file:///Users/truongtritin/Github/tuhocproductv2/lib/ai/case-study-generation/caseWriterPrompts.ts)
- **Cấu trúc đề bài (5 phần)**:
  1. 🏢 Company Context
  2. 🌪️ The Challenge (Trade-offs)
  3. 🚧 The Constraints (Nguồn lực, Dữ liệu, Văn hóa, Pháp lý)
  4. 🎯 Expected Output (PRD, GTM, MVP, North Star & Counter-metrics)
  5. 🕵️ Unknowns & Assumptions
- **Output**: JSON chứa `title`, `description`, `content_markdown`, `impact_metrics`.

## Phase 5: Thiết lập đánh giá (Rubric Master Agent)

**Mục tiêu**: Tạo bộ tiêu chí chấm điểm khắt khe cho bài giải của ứng viên.

- **Agent Roles**: [Rubric Master Agent]
- **Tiêu chí (5-6 items)**: Phân loại theo MARKET, PRODUCT_DESIGN, GROWTH, DATA_ANALYTICS, EXECUTION, MEASUREMENT_RISK.
- **Triết lý**: Chống sáo rỗng (Anti-Fluff), ưu tiên năng lực thực thi MVP và tư duy đánh đổi.

## Phase 6: Visual Agent (Cover image)

**Mục tiêu**: Sinh ảnh bìa qua model Gemini image (`generateCoverImage`), upload bucket `profile-images` / prefix `case-study-covers/`, gán `cover_image` (và `cover_image_prompt` từ Case Writer).

- **Regenerate thủ công**: Admin mở `/admin/case-studies/[id]` → **Regenerate cover** gọi `POST /api/admin/case-studies/:id/regenerate-cover` với `prompt` hiện tại trên form.

---

## Hậu xử lý (Post-Processing)

- **SEO Optimization**: Tự động tạo slug chuẩn SEO từ tiêu đề.
- **Database Update**: Lưu trữ kết quả và trạng thái `PENDING_EXPERT_REVIEW`.
- **Vector Embedding**: Nếu case được publish, tự động tạo embedding cho nội dung để phục vụ RAG tương lai.

## Tham chiếu kỹ thuật

- **Service**: `lib/services/caseStudyAiService.ts`
- **API generate**: `app/api/admin/case-studies/generate/route.ts` (`waitUntil`, `maxDuration`)
- **API regenerate cover**: `app/api/admin/case-studies/[id]/regenerate-cover/route.ts`
- **Prompts**: `lib/ai/case-study-generation/`
- **Tracing**: Theo dõi qua bảng `case_study_agent_traces`.
