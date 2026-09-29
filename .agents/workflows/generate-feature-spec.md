---
description: Vòng lặp phối hợp giữa PM, BA và UX để biến ý tưởng thô thành Đặc tả Yêu cầu (SRS) chuẩn hóa, làm Single Source of Truth cho toàn bộ dự án. target_agents: ["senior-product-manager", "senior-ba-specialist", "senior-ux"]
---

# 🚀 Quy trình Khởi tạo Đặc tả Tính năng (Feature Spec Generation Loop)

Bạn là Orchestrator. Nhiệm vụ của bạn là nhận một [Ý tưởng tính năng thô] từ người dùng và điều phối 3 chuyên gia `@senior-product-manager`, `@senior-ba-specialist`, và `@senior-ux` để xuất ra một file Đặc tả Yêu cầu (SRS) hoàn chỉnh.

TUYỆT ĐỐI tuân thủ trình tự các bước (SOP) dưới đây và BẮT BUỘC sử dụng "Template SRS chuẩn" (gồm 9 mục: Context, User Story, Functional, Non-Functional, Flow of Events, Acceptance Criteria, Rules, UX Validation, Data Dictionary).

### Bước 1: Định hình Tầm nhìn & Phạm vi (Thực thi bởi `@senior-product-manager`)

- **Đầu vào:** Ý tưởng thô từ người dùng.
- **Hành động:**
  1. Xác định Tên tính năng, Tác nhân (Actor), và Mục tiêu cốt lõi (Goal).
  2. Viết các Yêu cầu Phi chức năng (Non-Functional Requirements) về Security, Performance.
  3. Định nghĩa các User Stories (Agile Standard).
- **Đầu ra:** Khung sườn của file SRS (Hoàn thành Mục 1, 2, 4).

### Bước 2: Phân tích Nghiệp vụ & Dữ liệu (Thực thi bởi `@senior-ba-specialist`)

- **Đầu vào:** Khung sườn từ Bước 1.
- **Hành động:** Đào sâu vào logic vận hành.
  1. Viết chi tiết Luồng sự kiện (Flow of Events) bao gồm Happy Path và Alternative Flows (Ngoại lệ).
  2. Vẽ Flowchart bằng cú pháp `Mermaid`.
  3. Viết Tiêu chí Nghiệm thu (Acceptance Criteria) theo chuẩn BDD (Given/When/Then).
  4. Lập Danh mục Dữ liệu (Data Dictionary) với các ràng buộc chặt chẽ.
- **Đầu ra:** Bản SRS chi tiết về nghiệp vụ (Hoàn thành Mục 3, 5, 6, 7, 9).

### Bước 3: Thiết kế Trải nghiệm & Trạng thái (Thực thi bởi `@senior-ux`)

- **Đầu vào:** Bản SRS từ Bước 2.
- **Hành động:** Bổ sung góc nhìn giao diện và trải nghiệm người dùng.
  1. Đảm bảo mọi bước trong Flow of Events đều có UI tương ứng.
  2. TUÂN THỦ quy tắc thiết kế trong `.agents/rules/design-system.md` (Border, Padding, No Gradients, Reusable Components).
  3. Định nghĩa chi tiết các trạng thái: `isLoading` (Skeleton/Spinner), `Empty` (Chưa có dữ liệu), và `Error` (Mất mạng, API lỗi).
- **Đầu ra:** Bản nháp SRS hoàn chỉnh (Hoàn thành Mục 8).

### Bước 4: Vòng lặp Kiểm duyệt Chéo (Cross-Check Loop)

- **Hành động:**
  - Yêu cầu `@senior-ba-specialist` kiểm tra lại xem `@senior-ux` có làm sai lệch logic nghiệp vụ không.
  - Dừng luồng (Human-in-the-loop). Hiển thị bản tóm tắt các điểm chính và sơ đồ Mermaid ra màn hình để Người dùng (Bạn) duyệt.
  - Đợi người dùng gõ `Approve` hoặc yêu cầu chỉnh sửa.

### Bước 5: Lưu trữ Artifact (Thực thi bởi Orchestrator)

- **Hành động:**
  1. Đảm bảo thư mục `.docs/specs/` tồn tại.
  2. Lưu toàn bộ tài liệu vào tệp `.docs/specs/[feature_name]/[feature_name]_srs.md`.
  3. Format tài liệu BẮT BUỘC phải khớp 100% với Template SRS chuẩn.
- **Đầu ra cuối cùng:** Hiển thị thông báo "🎉 File Đặc tả đã sẵn sàng làm Single Source of Truth" kèm đường dẫn file.
