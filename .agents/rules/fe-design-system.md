---
trigger: always_on
---

# SYSTEM DESIGN RULES – REACTJS FRONTEND AGENT

(Đồng bộ với NestJS Feature-based Backend)

## 1. SYSTEM OVERVIEW

### 1.1. Định vị hệ thống

Tên dự án: Quizio
Backend cho nền tảng quiz thời gian thực (Kahoot-style).  
Tập trung vào:

- Tốc độ cao
- Real-time ổn định
- Phân quyền rõ ràng
- Dễ mở rộng theo feature

### 1.2. Kiến trúc

- **Feature-based Architecture** (không dùng Clean Architecture)
- Mỗi domain nghiệp vụ là một module độc lập
- Controller mỏng – Service chứa business logic
- Real-time sử dụng **Socket.IO** (NestJS Gateway)
- Redis dùng cho: cache, rate limiting, lưu trạng thái phòng live, ranking tạm thời, pub/sub
- BullMQ dùng cho các tác vụ bất đồng bộ (gửi email, generate report, cleanup phòng…)

### 1.3. Tech Stack bắt buộc

- React 18+ với TypeScript (strict mode)
- Build tool: Vite
- Routing: React Router DOM v6+
- Server State: **TanStack Query (React Query)**
- Client State: Zustand
- HTTP Client: Axios (có interceptor)
- Form: React Hook Form + Zod
- UI Library: [Ant Design / Shadcn UI / MUI] (chọn 1 và giữ nhất quán)
- Notification: react-hot-toast hoặc sonner
- Linting: ESLint + Prettier

### 1.4. Nguyên tắc chính

1. Tổ chức theo **Feature-based** (mỗi domain nghiệp vụ là một feature).
2. Component UI không được gọi API trực tiếp.
3. Tất cả API call phải đi qua Axios instance có interceptor.
4. Phân quyền frontend phải đồng bộ với backend (Role + Permission).
5. Frontend chỉ ẩn/hiện UI theo quyền, backend vẫn là nơi kiểm tra quyền cuối cùng.
6. Xử lý lỗi 401, 403, 429 một cách rõ ràng và thân thiện.
7. Hạn chế dùng `any`, ưu tiên type an toàn.

---

## 2. CẤU TRÚC THƯ MỤC (FEATURE-BASED)

src/
├── main.tsx
├── App.tsx
├── vite-env.d.ts
│
├── assets/
├── styles/
│
├── config/
│ ├── env.ts
│ └── constants.ts
│
├── lib/
│ ├── axios.ts # Axios instance + interceptor
│ ├── react-query.ts # QueryClient configuration
│ └── utils.ts
│
├── shared/
│ ├── components/ # Button, Modal, Table, Spinner, Empty...
│ ├── hooks/ # useAuth, usePermission, useDebounce...
│ ├── layouts/ # MainLayout, AuthLayout...
│ ├── types/
│ ├── constants/
│ ├── enums/ # Role, Permission (đồng bộ backend)
│ └── utils/
│
├── features/
│ ├── auth/
│ │ ├── components/
│ │ ├── hooks/
│ │ ├── pages/
│ │ ├── services/ # auth.api.ts
│ │ ├── stores/ # auth.store.ts
│ │ ├── types/
│ │ └── index.ts
│ │
│ ├── users/
│ │ ├── components/
│ │ ├── hooks/
│ │ ├── pages/
│ │ ├── services/ # users.api.ts
│ │ ├── types/
│ │ └── index.ts
│ │
│ ├── orders/
│ │ └── ...
│ │
│ └── notifications/
│ └── ...
│
├── routes/
│ ├── index.tsx
│ ├── PrivateRoute.tsx
│ ├── RoleRoute.tsx
│ └── paths.ts
│
└── types/
**Quy tắc cấu trúc:**

- Mỗi feature tương ứng với một module ở backend.
- Không để logic gọi API nằm trong component.
- `shared/` chỉ chứa những thứ thực sự dùng chung toàn ứng dụng.

---

## 3. NAMING CONVENTIONS

### 3.1. File & Folder

| Loại           | Quy tắc                      | Ví dụ                       |
| -------------- | ---------------------------- | --------------------------- |
| Feature folder | kebab-case                   | `users`, `order-management` |
| Component      | PascalCase                   | `UserTable.tsx`             |
| Page           | PascalCase + `Page`          | `UserListPage.tsx`          |
| Hook           | camelCase + `use`            | `useUsers.ts`               |
| Service / API  | kebab-case + `.api.ts`       | `users.api.ts`              |
| Store          | kebab-case + `.store.ts`     | `auth.store.ts`             |
| Types          | kebab-case + `.types.ts`     | `user.types.ts`             |
| Constants      | kebab-case + `.constants.ts` | `user.constants.ts`         |

### 3.2. Biến, Hàm, Component

| Loại             | Quy tắc                      | Ví dụ                         |
| ---------------- | ---------------------------- | ----------------------------- |
| Component        | PascalCase                   | `UserForm`                    |
| Hook             | camelCase bắt đầu bằng `use` | `useAuth`, `useUserDetail`    |
| Hàm thường       | camelCase                    | `formatDate`, `mapUserToForm` |
| Constant         | UPPER_SNAKE_CASE             | `MAX_PAGE_SIZE`               |
| Enum             | PascalCase                   | `Role`, `Permission`          |
| Type / Interface | PascalCase                   | `User`, `CreateUserDto`       |
| Boolean          | is / has / can / should      | `isLoading`, `canEdit`        |

### 3.3. Đồng bộ với Backend

- Tên type/DTO phía frontend nên gần giống backend (`CreateUserDto`, `UserResponse`...).
- Enum `Role` và `Permission` phải **giống hệt** backend.

---

## 4. GỌI API & ĐỒNG BỘ VỚI BACKEND

### 4.1. Axios Instance

- Chỉ sử dụng 1 Axios instance duy nhất (`lib/axios.ts`).
- Request interceptor: tự động gắn `Authorization: Bearer <token>`.
- Response interceptor xử lý:
  - `401` → logout hoặc refresh token.
  - `403` → thông báo “Bạn không có quyền thực hiện hành động này”.
  - `429` → thông báo “Bạn thao tác quá nhanh, vui lòng thử lại sau”.
  - `500` → thông báo lỗi hệ thống chung.

### 4.2. TanStack Query

- GET → `useQuery`
- POST/PUT/PATCH/DELETE → `useMutation`
- Query key phải có cấu trúc rõ ràng:
  ```ts
  ["users", filters][("users", userId)][("orders", { page, status })];
  ```

Sau mutation thành công phải invalidateQueries đúng key.

4.3. Service Layer
Mỗi feature có file \*.api.ts:
TypeScript// features/users/services/users.api.ts
export const usersApi = {
getList: (params: UserQuery) => axios.get('/users', { params }),
getById: (id: string) => axios.get(`/users/${id}`),
create: (data: CreateUserDto) => axios.post('/users', data),
update: (id: string, data: UpdateUserDto) => axios.patch(`/users/${id}`, data),
remove: (id: string) => axios.delete(`/users/${id}`),
};

5. AUTHENTICATION & AUTHORIZATION
   5.1. Authentication

Quản lý trạng thái đăng nhập bằng Zustand (auth.store.ts).
Token được gắn tự động qua Axios interceptor.
PrivateRoute: chưa đăng nhập → redirect về trang login.

5.2. Authorization (RBAC)
Enum phải đồng bộ với backend:
TypeScriptexport enum Role {
  Admin = 'ADMIN',
  User = 'USER',
}

export enum Permission {
USER_CREATE = 'user:create',
USER_READ = 'user:read',
USER_UPDATE = 'user:update',
USER_DELETE = 'user:delete',
ORDER_CREATE = 'order:create',
ORDER_READ = 'order:read',
ORDER_UPDATE = 'order:update',
ORDER_DELETE = 'order:delete',
}
Tạo hook usePermission():
TypeScriptconst { hasPermission, hasRole, can } = usePermission();
Cách sử dụng:
tsx{hasPermission(Permission.USER_CREATE) && <Button>Thêm người dùng</Button>}

{hasRole([Role.Admin, Role.Manager]) && <AdminPanel />}
Route phân quyền dùng RoleRoute.
5.3. Nguyên tắc bảo mật

Frontend chỉ dùng quyền để ẩn/hiện UI.
Mọi hành động quan trọng vẫn phải được backend kiểm tra và trả về 403 nếu không đủ quyền.

6. XỬ LÝ RATE LIMITING (429)

Interceptor bắt lỗi 429.
Hiển thị thông báo rõ ràng cho người dùng.
Nếu backend trả header Retry-After thì sử dụng giá trị đó để disable nút hoặc hiển thị đếm ngược.
Không tự động retry liên tục.

7. QUẢN LÝ STATE

Loại StateCông nghệVí dụServer State (dữ liệu API)TanStack QueryDanh sách user, chi tiết orderClient State toàn cụcZustandAuth user, theme, sidebarForm StateReact Hook FormForm tạo / chỉnh sửaUI State cục bộuseStateMở/đóng modal, tab đang chọn
Quy tắc: Không đưa dữ liệu từ API vào Zustand trừ khi thực sự cần chia sẻ lâu dài giữa nhiều nơi.

8. ROUTING

Định nghĩa tất cả đường dẫn trong routes/paths.ts.
Sử dụng createBrowserRouter.
Có PrivateRoute và RoleRoute.
Bắt buộc có trang 404.

9. FORM & VALIDATION

Sử dụng React Hook Form + Zod.
Schema Zod nên tương thích với validation của backend để giảm lỗi 400.
Hiển thị lỗi trả về từ backend một cách rõ ràng trên từng field nếu có thể.
