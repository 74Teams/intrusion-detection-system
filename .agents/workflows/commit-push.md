---
description: Quy trình kiểm thử, commit chuẩn Conventional Commits, tạo Feature Branch, push remote, tạo Pull Request (PR), hỏi duyệt Accept/Reject và Merge.
---

# 🚀 Quy trình Git Commit & Remote PR Workflow (Standard Git & PR Workflow)

Bạn là Orchestrator phụ trách quản lý mã nguồn Git. Khi người dùng yêu cầu commit hoặc khi hoàn thành một tính năng, bạn BẮT BUỘC thực thi tuần tự 5 bước theo tiêu chuẩn dưới đây:

---

## 📋 Phase 1: Kiểm thử & Đảm bảo Chất lượng Code (Pre-commit Check)

**Mục tiêu:** Không bao giờ commit code hỏng hoặc lỗi syntax.

1. **Build Verification:** Chạy `npm run build` (hoặc build từng folder `quizio-backend` / `quizio-frontend` tương ứng) để đảm bảo 0 lỗi TypeScript compilation.
2. **Linting & Formatting:** Chạy `npm run lint` hoặc `npm run format` nếu cần.
3. **Automated Testing:** Đảm bảo các unit tests/integration tests đều pass.

---

## 🌿 Phase 2: Quản lý Branch theo Tính năng (Feature Branching)

**Mục tiêu:** Cách ly mã nguồn tính năng mới với nhánh chính (`main`).

1. **Định dạng Tên Branch (Branch Naming Convention):**
   - Tính năng mới: `feature/<tên-tính-năng>` (VD: `feature/user-profile`, `feature/quiz-crud`)
   - Sửa lỗi: `bugfix/<tên-lỗi>` hoặc `hotfix/<tên-lỗi>` (VD: `bugfix/auth-token-expired`)
   - Refactor/Tối ưu: `refactor/<tên-chức-năng>` (VD: `refactor/rbac-guard`)
2. **Tạo Branch từ `main` mới nhất:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/<tên-tính-năng>
   ```

---

## 📝 Phase 3: Đặt thông điệp Commit chuẩn Conventional Commits

**Mục tiêu:** Lịch sử Git sạch sẽ, dễ tra cứu và tạo Release Notes tự động.

Định dạng bắt buộc: `<type>(<scope>): <short summary>`

### 📌 Các Type chuẩn:

- `feat`: Tính năng mới cho người dùng.
- `fix`: Sửa lỗi (bug fix).
- `docs`: Thêm hoặc cập nhật tài liệu (SRS, API Spec, README).
- `style`: Định dạng code (spaces, semicolons, format), không làm thay đổi logic.
- `refactor`: Tái cấu trúc code mà không sửa bug hay thêm feature.
- `perf`: Cải thiện hiệu năng (performance).
- `test`: Thêm hoặc sửa test cases.
- `chore`: Thay đổi build tools, dependencies, config (`package.json`, `.gitignore`).

---

## 🛑 Phase 4: Trạm Kiểm Duyệt Người Dùng (User Confirmation Checkpoint)

**Mục tiêu:** Tuân thủ 100% quy tắc trong `@/AGENTS.md` - KHÔNG tự động commit/push khi chưa được người dùng duyệt.

Agent BẮT BUỘC hiển thị thông tin và dừng luồng để hỏi ý kiến:

```text
📋 Đề xuất Git Commit, Push & Pull Request:
- Feature Branch: feature/<tên-tính-năng>
- Commit Message: <type>(<scope>): <message>
- Target Branch: main (origin/main)
- Các file thay đổi:
  - [NEW] quizio-backend/src/modules/...
  - [MODIFY] quizio-frontend/src/...

Vui lòng chọn:
- [Accept]: Đồng ý tạo branch, commit, push remote, tạo Pull Request và merge vào main.
- [Reject]: Bỏ qua commit và giữ nguyên trạng thái làm việc.
```

---

## 🔀 Phase 5: Push Remote, Pull Request & Merge (Hoàn tất)

Khi người dùng chọn **Accept**:

1. **Stage và commit thay đổi trên Feature Branch:**

   ```bash
   git add .
   git commit -m "<type>(<scope>): <message>"
   ```

2. **Push Feature Branch lên Remote Origin:**

   ```bash
   git push -u origin feature/<tên-tính-năng>
   ```

3. **Tạo Pull Request tự động bằng GitHub CLI (`gh`):**
   - Chạy lệnh:
     ```bash
     gh pr create --title "<type>(<scope>): <message>" --body "Automated Pull Request for feature/<tên-tính-năng>. Please review before merging." --base main --head feature/<tên-tính-năng>
     ```
   - Nếu chưa đăng nhập `gh` (`gh auth login`), hiển thị link tạo PR trên web: `https://github.com/nmchien1106/Quizio/pull/new/feature/<tên-tính-năng>`
   - **LƯU Ý:** KHÔNG tự động merge PR hoặc merge local sang `main`. Việc merge bắt buộc thực hiện sau khi PR được review và approve trên GitHub.

4. Thông báo hoàn tất thành công cho người dùng kèm link PR!
