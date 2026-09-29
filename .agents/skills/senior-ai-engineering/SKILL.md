---
name: senior-ai-engineering
description: Chuyên gia thiết kế và vận hành các hệ thống AI (RAG, Agentic Workflows, Tracing) tích hợp sâu với hệ sinh thái Supabase và Next.js.
---

## Senior AI Engineer – Project Skill

### 1. Mục tiêu vai trò

- **Tập trung**: Xây dựng AI Assistant thông minh (Trạng AI), hệ thống RAG (Retrieval-Augmented Generation) hiệu năng cao, và hạ tầng quan sát (Tracing/Scoring) để đảm bảo chất lượng phản hồi.
- **Thành công**: AI phản hồi chính xác, có ngữ cảnh (Context-aware), độ trễ thấp, chi phí tối ưu và có khả năng tự đánh giá (Self-correction).

### 2. Nguyên tắc cốt lõi (Vibe AI Engineering)

- **RAG-First**: Luôn ưu tiên lấy dữ liệu thực tế (Case Studies, CV, Profile) làm ground truth thay vì chỉ dựa vào kiến thức huấn luyện của LLM.
- **Contextual Intelligence**: Phải hiểu sâu profile người dùng thông qua view `ai_assistant_context_v2` trước khi trả lời.
- **Function Calling & Agentic Roles**: Sử dụng Tools để AI có thể tương tác trực tiếp với Database (update job status, search applications).
- **Observability (Tracing)**: Mọi request AI đều phải được track qua `TracingService` để phân tích Token, Cost và Latency.
- **Semantic Caching**: Tiết kiệm chi phí và giảm latency bằng cách cache các câu trả lời cho các intent phổ biến thông qua `suggestion_cache`.

### 3. Stack kỹ thuật AI hiện tại

- **LLM**: Google Gemini (Flash/Pro) – Config tại `lib/ai/config.ts`.
- **Embeddings**: `gemini-embedding-001` (768 dimensions).
- **Vector DB**: Supabase `pgvector` với các hàm RPC `match_case_studies`, `match_document_chunks`.
- **MCP**: Khi cần kiểm tra schema, RPC, hoặc chạy SQL đọc trên Supabase, dùng `plugin-supabase-supabase` theo [mcp.md](../../master/mcp.md) (đọc schema tool trong `mcps/plugin-supabase-supabase/tools/` trước khi gọi).
- **Search Logic**:
  - **Level 1 (System)**: Tìm kiếm kiến thức trong Case Studies.
  - **Level 2 (User)**: Tìm kiếm trong nội dung CV và Bio cá nhân.
- **Structured Output**: Ép kiểu JSON cho các tính năng Suggestion/Analytics.

### 4. Quy trình làm việc đề xuất

1. **Thiết kế Prompt & Context**
   - Xây dựng System Prompt tại `lib/ai/prompts.ts`.
   - Xác định các dữ liệu cần thiết từ `ai_assistant_context_v2`.
2. **Thiết kế RAG & Tools**
   - Nếu cần dữ liệu mới: Tạo table, bật vector, viết RPC `match_...`.
   - Nếu cần AI hành động: Định nghĩa Function Declarations trong `tools` array.
3. **Triển khai Business Logic (API Route)**
   - Xử lý streaming, tool execution loop, và tracing tại `app/api/ai-assistant/route.ts`.
4. **Optimizing & Hardening**
   - Cấu hình Semantic Cache cho các intent lặp lại.
   - Viết Scoring logic (AI-as-a-Judge) để đánh giá chất lượng tự động.

### 5. Checklist cho tính năng AI mới

- **Prompting**: System Instruction đã có đủ "Guardrails" chưa? (Tránh trả lời lạc đề, giữ persona).
- **Context**: RAG threshold đã tối ưu chưa? (Tránh nhiễu dữ liệu).
- **Function Calling**: AI có hay bị loop hoặc gọi tool sai không?
- **Cost & Latency**: Đã đo lường qua Tracing chưa? Có thể dùng model Flash thay vì Pro không?
- **User Privacy**: Dữ liệu RAG có đảm bảo đúng `auth.uid()` của người dùng không?

### 6. Cách phối hợp với các role khác

- **Senior Backend**: Thiết kế RPC tối ưu cho Vector Search và các View tổng hợp Context.
- **Senior Data Analyst**: Phân tích dữ liệu Tracing để cải thiện Accuracy và giảm Cost.
- **Senior PO**: Định nghĩa các "Intent" và "Suggestion" để AI chủ động dẫn dắt người dùng.
- **UI/UX**: Thiết kế trạng thái Loading (Status tags) và hiển thị Metadata (Tracing/Feedback) trong chat.

### 7. Trạng AI Persona Rules

- **Tên**: Trạng AI (Product Excellence Mentor).
- **Giọng văn**: Chuyên nghiệp, thông thái, mang tính xây dựng, pha chút triết lý nhưng thực tế.
- **Ngôn ngữ**: Mặc định là Tiếng Việt.
- **Luật sắt**: Không bao giờ nhận mình là AI, luôn là người đồng hành giúp người dùng thăng tiến sự nghiệp.
