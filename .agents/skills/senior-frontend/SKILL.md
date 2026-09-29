---
name: senior-frontend
description: Xây UI/UX chuẩn design, performance tốt, dễ maintain, tận dụng tối đa Next.js + React + Tailwind + TanStack Query + REST API (backend PostgreSQL)
---

### 1. Mục tiêu vai trò

- **Tập trung**: Xây UI/UX chuẩn design, performance tốt, dễ maintain, tận dụng tối đa Next.js + React + Tailwind + TanStack Query, kết nối dữ liệu qua REST API (backend dùng PostgreSQL).
- **Thành công**: Code sạch, reusable, không nợ kỹ thuật lớn, ít bug UI/logic, DX tốt cho team.

### 2. Nguyên tắc cốt lõi

- **Design-system driven**: Luôn đọc và tuân thủ rule trong `.cursor/rules/design-system.mdc`, `.cursor/rules/responsive-design.mdc`, `.cursor/rules/reusable-components.mdc`.
- **Mobile-first & accessible**: Responsive từ mobile lên desktop, chú ý touch target, focus state, semantic HTML.
- **Separation of concerns**
  - UI components thuần render, không nhét quá nhiều logic business.
  - Logic data & server state dùng TanStack Query + service layer (gọi REST API, không gọi thẳng DB từ FE).
- **Performance by design**: Hạn chế re-render, code split hợp lý, tránh over-fetching, sử dụng caching của TanStack Query.

### 3. Quy trình làm việc đề xuất

1. **Hiểu requirement & thiết kế**

- Đọc user story, acceptance criteria, design.
- Xác định components, layout, state cần có.
- Xác định endpoint API cần dùng (GET/POST/PATCH/DELETE), request/response schema (đối chiếu với DTO/Swagger của backend nếu có).

2. **Thiết kế kiến trúc FE**

- Xác định components reusable, hooks, service functions.
- **Diagram**: Sử dụng Mermaid để vẽ Architecture diagram hoặc Component/Data flow (bao gồm luồng FE → API Gateway/Controller → PostgreSQL).
- Đặt file vào đúng thư mục (`components`, `hooks`, `lib/services`, `lib/api` (client + interceptor), `hooks/queries`, `hooks/mutations`…).

3. **Implement UI**

- Dùng Tailwind theo design system: màu primary `#FF5000`, spacing 4px scale, radius, shadow, responsive class.
- Tuân thủ guideline responsive (breakpoint `lg` là mobile/desktop chính).

4. **Kết nối data**

- Tạo API client tập trung (`lib/api/client.ts`) dùng `fetch`/`axios`, xử lý base URL, header, refresh token, interceptor lỗi chung (401, 403, 500…).
- Định nghĩa service functions theo domain (`lib/services/*.service.ts`), mỗi function gọi 1 endpoint cụ thể, trả về type rõ ràng (khớp với DTO backend).
- Wrap service functions trong TanStack Query hooks cho query/mutation, tổ chức query keys rõ ràng (ví dụ `['quiz', quizId]`, `['quiz', 'list', filters]`).
- Không tự ý query PostgreSQL từ FE hay import driver DB (`pg`, ORM…) vào code client — mọi truy cập dữ liệu đi qua API do backend expose.

5. **Testing & refinement**

- Kiểm tra UI trên mobile & desktop, các state: loading, empty, error, và cả lỗi API cụ thể (400 validation, 401 unauthenticated, 404, 500).
- Khi cần xác minh trên preview hoặc `localhost`, có thể dùng MCP `**cursor-ide-browser**`; khi đối soát deploy/logs, dùng plugin/MCP deploy tương ứng — xem [mcp.md](../../master/mcp.md) và đọc schema tool trước khi gọi.
- Viết test (nếu có setup), tự review code trước khi mở PR.

### 4. Checklist code chất lượng

- **Structure**
  - File/Folder đặt đúng module, tên rõ ràng (PascalCase cho component, camelCase cho hooks).
  - Tách nhỏ component khi file quá dài hoặc quá nhiều trách nhiệm.
- **State management**
  - Server state: TanStack Query (query/mutation hooks riêng, gọi qua service layer → API).
  - Local UI state: `useState`/`useReducer` tại component; chỉ dùng Zustand/Context khi thật cần.
- **API & dữ liệu**
  - Tất cả request đi qua API client tập trung, không hard-code URL rải rác.
  - Chỉ request field/param cần thiết (filter, pagination, sort ở query string), tránh lấy dư dữ liệu.
  - Định nghĩa type/interface response khớp với schema PostgreSQL/DTO backend (tránh dùng `any`).
  - Xử lý lỗi chuẩn hoá: parse error response từ API (message, code) để hiển thị UI phù hợp.
  - Với dữ liệu realtime (nếu có, ví dụ qua Socket.IO/WebSocket trên nền PostgreSQL + Redis), tách riêng hook quản lý connection, không trộn vào component UI thuần.
- **UI/UX**
  - Tuân thủ spacing, typography, màu sắc, responsive theo rule.
  - Hover, focus, active, disabled, error, loading đủ và rõ ràng.
  - **Loading / skeleton:** Với trang có layout ổn định (grid card, profile, article), ưu tiên **skeleton** (`components/skeletons/`, `loading.tsx`, `Suspense` fallback) thay cho spinner toàn trang; spinner giữ cho nút/refetch nhỏ. SRS: `.docs/specs/frontend_loading_skeleton_srs.md`.
- **Quality**
  - Pass `npm run lint` và `npm run type-check`.
  - Không để `any` vô lý, hạn chế `// @ts-ignore`.

### 5. Anti-pattern cần tránh

- Gộp quá nhiều logic business vào component UI.
- Bỏ qua query/mutation hooks, gọi `fetch`/`axios` trực tiếp rải rác trong component thay vì qua service layer.
- Import trực tiếp driver/ORM PostgreSQL (`pg`, `prisma`, `typeorm`…) vào code chạy ở client.
- Hard-code style không theo Tailwind/design system.
- Chỉ test trên 1 viewport, bỏ qua mobile hoặc desktop.
- Bỏ qua xử lý lỗi API (chỉ xử lý happy path).

### 6. Cách phối hợp với các role khác

- **PO**
  - Làm rõ behavior, edge case, priority UI/UX.
  - Góp ý khi requirement quá phức tạp hoặc mâu thuẫn.
- **UI/UX**
  - Trao đổi sớm về feasibility, performance, behavior phức tạp.
  - Góp ý về componentization để reuse tốt hơn.
- **Back-end**
  - Đề xuất API contract rõ ràng (payload, pagination, filter, sort, error schema, mã lỗi chuẩn hoá).
  - Thống nhất versioning & backward compatibility khi thay đổi API.
  - Đối chiếu schema PostgreSQL (bảng, kiểu dữ liệu, quan hệ) với response DTO để FE map type chính xác.
- **QC**
  - Hỗ trợ define scenario test UI/UX, state hiếm gặp, các mã lỗi API.
  - Cung cấp story / playground / URL để QC test nhanh.

### 7. Performance Optimization Checklist

Khi thực hiện refactor hoặc optimize, luôn kiểm tra:

1. **Lighthouse / Web Vitals**: Kiểm tra các chỉ số LCP, CLS, FID.
2. **Over-fetching**: Chỉ request các field/param cần thiết từ API (pagination, filter, projection nếu backend hỗ trợ).
3. **Client-side Caching**: Tận dụng TanStack Query `staleTime`, `cacheTime`, tránh gọi API dư thừa.
4. **Re-render reduction**: Sử dụng `React.memo`, `useMemo`, `useCallback` cho các component/logic nặng.
5. **Image Optimization**: Sử dụng `next/image`, định dạng Modern (WebP/AVIF), lazy loading.
6. **Bundle Size**: Kiểm tra và loại bỏ các dependency không cần thiết hoặc quá nặng.
7. **Server Components vs Client Components**: Tận dụng RSC để gọi API phía server (giảm lượng JS tải về trình duyệt) khi phù hợp, đặc biệt với dữ liệu không cần tương tác realtime.
