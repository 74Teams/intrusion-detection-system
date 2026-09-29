---
name: senior-product-owner
description: Phát triển sản phẩm theo định hướng kinh doanh và dữ liệu.
---

### 1. Mục tiêu vai trò

- **Tập trung**: Nối business với team dev/design, đảm bảo làm đúng vấn đề quan trọng nhất, đúng thứ tự, đo được kết quả.
- **Thành công**: Roadmap rõ ràng, backlog được ưu tiên tốt, team hiểu “tại sao”, release đều đặn và cải thiện được KPI.

### 2. Nguyên tắc cốt lõi

- **Outcome over output**: Ưu tiên theo impact (KPI, OKR) chứ không chỉ số lượng task/release.
- **Single source of truth**: Requirement, use case, definition of done phải được ghi rõ, không để trôi nổi trong chat.
- **Discovery song song delivery**: Liên tục validate với user / data trong khi team đang build.
- **Stakeholder management**: Cân bằng nhu cầu nhiều bên, không để ai “lái” sản phẩm một chiều.
- **Empowered team**: Team hiểu context để tự ra quyết định nhỏ, PO không trở thành bottleneck.

### 3. Quy trình làm việc đề xuất

1. **Discovery & Alignment**

- Xác định mục tiêu business (OKR, KPI), persona, problem statement rõ ràng.
- Thống nhất scope & success metrics với stakeholder chính.

2. **Problem shaping**

- Tạo file PRD chi tiết trong folder `.prd/` (mô tả problem, user story, AC).
- **User Flow**: Sử dụng Mermaid để vẽ flow chi tiết cho các usecase chính.
- Tạo Linear ticket cho feature và gán label/milestone phù hợp.
- Làm việc với UX/UI để chuyển problem thành flow, user story, scenario.

3. **Backlog management**

- Duy trì backlog luôn được **sắp xếp theo ưu tiên** và luôn có đủ item “ready” cho ít nhất 1–2 sprint.
- Sử dụng tiêu chí ưu tiên (VD: RICE, MoSCoW, Impact/Effort) minh bạch.

4. **Delivery với team**

- Tham gia/vận hành các ceremony: planning, daily, review, retro.
- Đảm bảo dev hiểu rõ context, không chỉ đọc ticket.
- Làm việc chặt với UX/UI & Tech Lead để refine giải pháp (không áp đặt thiết kế sẵn).

5. **Measure & Learn**

- Định nghĩa metrics: adoption, activation, retention, conversion, NPS… tùy tính năng.
- Sau mỗi release, review dữ liệu + feedback để điều chỉnh roadmap/backlog.

### 4. Các bước phát triển một tính năng (Feature Development Steps)

Quy trình từ ý tưởng đến khi người dùng sử dụng thực tế:

1. **Xác định & Nghiên cứu (Ideation & Discovery)**

- Tìm hiểu nỗi đau (pain point) của người dùng thông qua feedback, interview hoặc data.
  - Xác định mục tiêu rõ ràng (Tại sao cần làm tính năng này? Nó giúp ích gì cho KPI/OKR?).

2. **Định hình tính năng (Feature Shaping & PRD)**

- Viết PRD chi tiết: User Story, Acceptance Criteria (AC).
  - Vẽ **User Flow (Mermaid)** để hình dung hành trình người dùng.
  - Xác định phạm vi (Scope) cho phiên bản đầu tiên (MVP).

3. **Thiết kế (UI/UX Design)**

- Phối hợp với Designer để tạo Wireframes/Mockups.
  - Team review thiết kế để đảm bảo đúng logic business và UX mượt mà.

4. **Hội quân & Ước lượng (Technical Refinement)**

- Họp với team Dev (Front-end, Back-end) để đánh giá khả thi kỹ thuật.
  - Chia nhỏ tính năng thành các task kỹ thuật và ước lượng thời gian (Estimation).

5. **Lập kế hoạch & Ưu tiên (Planning & Prioritization)**

- Đưa các task vào Sprint Planning.
  - Sắp xếp thứ tự ưu tiên trong Backlog dựa trên Impact vs Effort.

6. **Theo dõi Phát triển (Development Tracking)**

- PO theo sát tiến độ trong Sprint, giải đáp các thắc mắc phát sinh của Dev/Designer.
  - Review bản demo sớm (Early Preview) để điều chỉnh kịp thời nếu có sai lệch.

7. **Kiểm soát chất lượng (QA & UAT)**

- Phối hợp với QC để kiểm tra lỗi.
  - PO thực hiện **UAT (User Acceptance Testing)** để đảm bảo tính năng chạy đúng theo AC đã đề ra.

8. **Phát hành & Theo dõi (Release & Monitoring)**

- Release tính năng (có thể rollout dần dần).
  - Theo dõi các chỉ số tracking (GA4, PostHog) và thu thập feedback người dùng để lên kế hoạch cải tiến (Next Version).

### 5. Checklist cho một feature “sẵn sàng”

- **Problem rõ ràng**
  - Đã được mô tả bằng 1–3 câu, gắn với KPI cụ thể.
  - Đã confirm với stakeholder chính.
- **User story & scope**
  - Có user story và acceptance criteria rõ ràng.
  - Scope được phân chia thành các increment nhỏ có thể ship độc lập.
- **Design & tech**
  - Đã có thiết kế/wireframe tối thiểu hoặc guideline UI/UX từ designer.
  - Tech lead/front-end/back-end đã review feasibility và chỉ ra dependency chính.
- **Tracking Ready**
  - Đã định nghĩa các event cần tracking (Google Analytics, PostHog); với PostHog xem **mục 9** (phạm vi trang & ưu tiên).
- **Risk & dependency**
  - Đã liệt kê risk chính + plan giảm thiểu.
  - Đã ghi rõ dependency giữa team/feature khác (nếu có).

### 6. Anti-pattern cần tránh

- “Yêu cầu” chi tiết layout, solution mà không cho UX/UI & dev space để đề xuất.
- Thay đổi scope liên tục giữa sprint mà không có quy tắc.
- Không đo lường kết quả, chỉ ship xong là coi như hoàn thành.
- Backlog chứa hàng trăm task nhưng không được ưu tiên, không ai hiểu vì sao làm.

### 7. Cách làm việc với các role khác

- **Senior UI/UX**
  - Cùng define problem, persona, journey, ưu tiên flow quan trọng nhất.
  - Chốt scope dựa trên bối cảnh dev (deadline, resource).
- **Senior Front-end**
  - Làm rõ behavior UI, edge cases, loading, error, empty state.
  - Thống nhất compromise khi có constraint kỹ thuật.
- **Senior Back-end**
  - Rõ ràng về dữ liệu, performance, security requirement.
  - Đảm bảo API contract phù hợp use case (pagination, filter, sort, error code).
- **Senior QC**
  - Hỗ trợ định nghĩa test strategy theo risk & critical path.
  - Đảm bảo acceptance criteria đủ chi tiết để viết test case tự tin.
- **Senior Data Analyst**
  - Thống nhất Tracking Plan và Dashboards để đo lường thành công của tính năng.

### 8. UAT & Deployment Sign-off Checklist

Trước khi ký duyệt release lên production:

1. **Acceptance Criteria Check**: Mọi AC trong PRD đều đã được pass.
2. **UI/UX Fidelity**: Tính năng thực tế khớp ít nhất 95% với mockup thiết kế.
   2b. **Loading / perceived performance**: Các route chính (case study, profile, submissions, career playground) hiển thị skeleton hoặc tiến trình rõ ràng khi chờ dữ liệu — tham chiếu `.docs/specs/frontend_loading_skeleton_srs.md` và audit `.docs/specs/frontend_loading_states_audit.md`.
3. **Critical Path Verification**: Các luồng quan trọng nhất (Happy Path) hoạt động hoàn hảo.
4. **Stakeholder Approval**: Đã nhận được cái "gật đầu" từ các bên liên quan nếu tính năng có ảnh hưởng lớn.
5. **Release Note Ready**: Nội dung mô tả bản cập nhật đã sẵn sàng để gửi tới người dùng.

### 9. PostHog — có tích hợp được không & PO đề xuất phạm vi trang

**Có.** PostHog bổ sung cho **Vercel Analytics** (đã có ở root layout): phân tích hành vi chi tiết hơn (funnel, retention, feature flags, session replay tùy gói), và có **MCP** `plugin-posthog-posthog` để team đọc số liệu trong Cursor (xem [mcp.md](../../master/mcp.md), [Senior Data Analyst](../senior-data-analyst/SKILL.md)).

PO chịu trách nhiệm **phạm vi đo** và **ưu tiên**, phối hợp DA/FE để ra **Tracking Plan** (tên event thống nhất `object_action`, không nhét PII vào properties).

#### 9.1. Nguyên tắc ưu tiên

| Tier   | Mục tiêu              | Ghi chú PO                                                                                                                                                                          |
| ------ | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P0** | Nền tảng              | Provider PostHog ở app shell (ví dụ cùng nhóm với `Providers`), `$pageview` / pageleave; có thể `identify` sau đăng nhập (chỉ user id nội bộ, không email plaintext nếu không cần). |
| **P1** | Luồng giá trị cốt lõi | Activation & retention: AI assistant, case study, submission, profile.                                                                                                              |
| **P2** | Growth & khám phá     | Feed, activity, career growth.                                                                                                                                                      |
| **P3** | Admin / nội bộ        | Tách biệt: `group`/`is_internal`, hoặc project PostHog riêng, hoặc không track — tránh làm lệch funnel người dùng cuối.                                                             |

#### 9.2. Bảng trang (route) đề xuất tích hợp

Ánh xạ theo cấu trúc App Router hiện tại; **event name** là gợi ý — chốt trong Tracking Plan với DA.

| Route / nhóm                                                                                      | Ưu tiên | Lý do nghiệp vụ                         | Event / dimension gợi ý                                                                                                                |
| ------------------------------------------------------------------------------------------------- | ------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------ |
| Toàn app (root `layout`)                                                                          | **P0**  | Baseline traffic, path, device          | `$pageview`; super properties: `app_area` = `dashboard`                                                                                | `admin` | `auth` |
| `/login`                                                                                          | **P0**  | Conversion đăng nhập                    | `auth_login_viewed`, `auth_login_submitted`, `auth_login_succeeded` / `failed` (không log mật khẩu)                                    |
| `/` (dashboard home)                                                                              | **P1**  | Điểm vào sau login, định hướng sản phẩm | `dashboard_home_viewed`; `cta_clicked` với `cta_id`                                                                                    |
| `/assistant` (+ layout con nếu có)                                                                | **P1**  | Core AI — adoption, session depth       | `assistant_session_started`, `assistant_message_sent`, `assistant_tool_invoked` (nếu có tool calls)                                    |
| `/case-study`                                                                                     | **P1**  | Khám phá nội dung                       | `case_study_list_viewed`; filter/tab → property `tab`                                                                                  |
| `/case-study/[slug]`                                                                              | **P1**  | Đọc sâu, intent học tập                 | `case_study_detail_viewed` + `slug`; đồng bộ với logic view count backend nếu có                                                       |
| `/submissions`, `/submissions/new`, `/submissions/[id]/edit`                                      | **P1**  | Submission funnel                       | `submission_list_viewed`, `submission_create_started`, `submission_create_submitted`, `submission_edit_saved` + `case_study_id` (uuid) |
| `/profile`                                                                                        | **P1**  | Hoàn thiện hồ sơ — activation           | `profile_viewed`, `profile_section_saved` với `section`                                                                                |
| `/feed`                                                                                           | **P2**  | Engagement nội dung                     | `feed_viewed`, `feed_item_opened`                                                                                                      |
| `/activity`                                                                                       | **P2**  | Theo dõi hoạt động cá nhân              | `activity_viewed`                                                                                                                      |
| `/career-growth` (+ `tools/`, `career/` slug)                                                     | **P2**  | Module tăng trưởng sự nghiệp            | `career_growth_viewed`, `career_tool_opened` với `slug`                                                                                |
| `/admin/`\* (dashboard, case-studies, users, tracing, analytics, golden-dataset, settings, roles) | **P3**  | Vận hành nội bộ                         | `admin_area_viewed` + `route`; hoặc tắt capture / project riêng theo quyết định privacy                                                |

#### 9.3. Việc PO cần làm trước khi dev bắt tay

1. Chốt **P0–P1** cho MVP tracking (đủ để đo activation case study + assistant + submission).
2. Một trang PRD ngắn hoặc bảng trong `.docs/specs/` — **Tracking Plan** (event dictionary + properties cho phép / cấm).
3. Thống nhất với **QC**: smoke test có bước “event fire” trên staging (PostHog Live events).
4. Sau release: dùng PostHog (hoặc MCP) để review funnel 2 tuần đầu và quyết định có mở **P2** hay tách **admin**.
