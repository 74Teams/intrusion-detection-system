---
trigger: always_on
---

# DATABASE SCHEMA – Real-time Quiz Platform

(Updated: Refresh Token lưu trên Redis)

## 1. Tổng quan

- Database: PostgreSQL
- ORM: TypeOrm
- Refresh Token: **lưu trên Redis** (không còn bảng trong PostgreSQL)
- Phong cách đặt tên: `snake_case`
- Primary Key: UUID
- Mọi bảng đều có `created_at` và `updated_at`

---

## 2. Sơ đồ quan hệ

users
├── quizzes (1 - n) # creator
├── rooms (1 - n) # host
└── participants (1 - n) # nếu user đã login
quizzes
├── questions (1 - n)
└── rooms (1 - n)
questions
└── choices (1 - n)
rooms
├── participants (1 - n)
└── participant_answers (1 - n)
participants
└── participant_answers (1 - n)

## 3. Chi tiết các bảng

### 3.1. users

| Cột        | Kiểu dữ liệu | Ràng buộc                  | Mô tả               |
| ---------- | ------------ | -------------------------- | ------------------- |
| id         | UUID         | PK                         | -                   |
| email      | VARCHAR(255) | UNIQUE, NOT NULL           | -                   |
| password   | TEXT         | NOT NULL                   | password hash       |
| username   | VARCHAR(50)  | NOT NULL                   | display name        |
| avatar_url | TEXT         | NULL                       | -                   |
| role       | ENUM         | NOT NULL, DEFAULT 'PLAYER' | PLAYER, HOST, ADMIN |
| is_active  | BOOLEAN      | DEFAULT true               | -                   |
| created_at | TIMESTAMP    | DEFAULT now()              | -                   |
| updated_at | TIMESTAMP    | DEFAULT now()              | -                   |

**Index:** `email`, `role`

---

### 3.2. quizzes

| Cột          | Kiểu dữ liệu | Ràng buộc         | Mô tả           |
| ------------ | ------------ | ----------------- | --------------- |
| id           | UUID         | PK                | -               |
| title        | VARCHAR(255) | NOT NULL          | -               |
| description  | TEXT         | NULL              | -               |
| cover_url    | TEXT         | NULL              | -               |
| visibility   | ENUM         | DEFAULT 'PRIVATE' | PRIVATE, PUBLIC |
| is_published | BOOLEAN      | DEFAULT false     | -               |
| play_count   | INTEGER      | DEFAULT 0         | -               |
| creator_id   | UUID         | FK → users.id     | -               |
| created_at   | TIMESTAMP    | DEFAULT now()     | -               |
| updated_at   | TIMESTAMP    | DEFAULT now()     | -               |

**Index:** `creator_id`, `(visibility, is_published)`

---

### 3.3. questions

| Cột            | Kiểu dữ liệu | Ràng buộc       | Mô tả               |
| -------------- | ------------ | --------------- | ------------------- |
| id             | UUID         | PK              | -                   |
| quizz_id       | UUID         | FK → quizzes.id | -                   |
| content        | TEXT         | NOT NULL        | Nội dung câu hỏi    |
| background_url | TEXT         | NULL            | Ảnh nền câu hỏi     |
| time_limit     | INTEGER      | DEFAULT 20      | Giây                |
| points         | INTEGER      | DEFAULT 1000    | Điểm cơ bản của câu |
| index          | INTEGER      | NOT NULL        | Thứ tự câu hỏi      |
| created_at     | TIMESTAMP    | DEFAULT now()   | -                   |
| updated_at     | TIMESTAMP    | DEFAULT now()   | -                   |

**Index:** `quizz_id`

---

### 3.4. choices

| Cột         | Kiểu dữ liệu | Ràng buộc         | Mô tả              |
| ----------- | ------------ | ----------------- | ------------------ |
| id          | UUID         | PK                | -                  |
| question_id | UUID         | FK → questions.id | -                  |
| content     | TEXT         | NOT NULL          | Nội dung đáp án    |
| is_correct  | BOOLEAN      | DEFAULT false     | -                  |
| index       | INTEGER      | NOT NULL          | 0=A, 1=B, 2=C, 3=D |
| created_at  | TIMESTAMP    | DEFAULT now()     | -                  |
| updated_at  | TIMESTAMP    | DEFAULT now()     | -                  |

**Index:** `question_id`

---

### 3.5. rooms

| Cột                    | Kiểu dữ liệu | Ràng buộc         | Mô tả                                 |
| ---------------------- | ------------ | ----------------- | ------------------------------------- |
| id                     | UUID         | PK                | -                                     |
| room_pin               | VARCHAR(6)   | UNIQUE, NOT NULL  | Mã PIN 6 số                           |
| quizz_id               | UUID         | FK → quizzes.id   | -                                     |
| host_id                | UUID         | FK → users.id     | -                                     |
| title                  | VARCHAR(255) | NULL              | Tên phòng (optional)                  |
| status                 | ENUM         | DEFAULT 'WAITING' | WAITING, PLAYING, FINISHED, CANCELLED |
| max_players            | INTEGER      | DEFAULT 50        | -                                     |
| current_question_index | INTEGER      | NULL              | Câu đang chơi                         |
| start_time             | TIMESTAMP    | NULL              | -                                     |
| end_time               | TIMESTAMP    | NULL              | -                                     |
| created_at             | TIMESTAMP    | DEFAULT now()     | -                                     |
| updated_at             | TIMESTAMP    | DEFAULT now()     | -                                     |

**Index:** `room_pin`, `host_id`, `status`

---

### 3.6. participants

| Cột           | Kiểu dữ liệu | Ràng buộc                | Mô tả                |
| ------------- | ------------ | ------------------------ | -------------------- |
| id            | UUID         | PK                       | -                    |
| room_id       | UUID         | FK → rooms.id            | -                    |
| user_id       | UUID         | FK → users.id (nullable) | `null` = Guest       |
| username      | VARCHAR(50)  | NOT NULL                 | Nickname trong phòng |
| avatar_url    | TEXT         | NULL                     | -                    |
| total_score   | BIGINT       | DEFAULT 0                | -                    |
| correct_count | INTEGER      | DEFAULT 0                | -                    |
| is_connected  | BOOLEAN      | DEFAULT true             | -                    |
| joined_at     | TIMESTAMP    | DEFAULT now()            | -                    |
| left_at       | TIMESTAMP    | NULL                     | -                    |
| created_at    | TIMESTAMP    | DEFAULT now()            | -                    |
| updated_at    | TIMESTAMP    | DEFAULT now()            | -                    |

**Ràng buộc:** `UNIQUE(room_id, username)`  
**Index:** `room_id`, `user_id`

---

### 3.7. participant_answers

| Cột            | Kiểu dữ liệu | Ràng buộc                  | Mô tả                  |
| -------------- | ------------ | -------------------------- | ---------------------- |
| id             | UUID         | PK                         | -                      |
| participant_id | UUID         | FK → participants.id       | -                      |
| question_id    | UUID         | FK → questions.id          | -                      |
| choice_id      | UUID         | FK → choices.id (nullable) | `null` = không trả lời |
| is_correct     | BOOLEAN      | DEFAULT false              | -                      |
| point_earned   | BIGINT       | DEFAULT 0                  | -                      |
| time_taken_ms  | INTEGER      | NULL                       | Thời gian trả lời (ms) |
| created_at     | TIMESTAMP    | DEFAULT now()              | -                      |
| updated_at     | TIMESTAMP    | DEFAULT now()              | -                      |

**Ràng buộc:** `UNIQUE(participant_id, question_id)`  
**Index:** `participant_id`, `question_id`

---

## 4. Enums

```ts
enum Role {
  USER
  ADMIN
}

enum QuizVisibility {
  PRIVATE
  PUBLIC
}

enum RoomStatus {
  WAITING
  PLAYING
  FINISHED
  CANCELLED
}
```
