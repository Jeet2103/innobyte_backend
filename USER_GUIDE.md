# 📝 USER GUIDE – Blog API

Welcome to the **Blog API**! This guide explains how to authenticate users, interact with blog posts and comments, and use tools like Swagger UI, Postman, and `curl`.

---

## 📌 Base URL

```
http://localhost:5000/api
```

---

## 🔐 Authentication – JWT Based

### ✅ Register a New User

**Endpoint:**

```
POST /auth/register
```

**Request Body:**

```json
{
  "username": "yourusername",
  "email": "your@email.com",
  "password": "YourPassword123"
}
```

---

### ✅ Login and Get Token

**Endpoint:**

```
POST /auth/login
```

**Request Body:**

```json
{
  "username": "yourusername",
  "password": "YourPassword123"
}
```

**Sample Response:**

```json
{
  "access_token": "<your_token>",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "yourusername"
  }
}
```

> Use the `access_token` in the `Authorization` header like this:

```
Authorization: Bearer <your_token>
```

---

## 🧾 Blog Posts Endpoints

### ▶ Create a Post

```
POST /posts
Authorization: Bearer <your_token>
```

**Request Body:**

```json
{
  "title": "My First Post",
  "content": "Hello world!"
}
```

---

### ▶ Get All Posts

```
GET /posts
```

---

### ▶ Get a Specific Post

```
GET /posts/<post_id>
```

---

### ▶ Update a Post

```
PUT /posts/<post_id>
Authorization: Bearer <your_token>
```

**Request Body:**

```json
{
  "title": "Updated Title",
  "content": "Updated Content"
}
```

---

### ▶ Delete a Post

```
DELETE /posts/<post_id>
Authorization: Bearer <your_token>
```

---

## 💬 Comment Endpoints

### ▶ Create a Comment

```
POST /comments
Authorization: Bearer <your_token>
```

**Request Body:**

```json
{
  "content": "Great post!",
  "post_id": 1
}
```

---

### ▶ Get All Comments (Optional filter by post)

```
GET /comments
GET /comments?post_id=1
```

---

### ▶ Get a Specific Comment

```
GET /comments/<comment_id>
```

---

### ▶ Update a Comment

```
PUT /comments/<comment_id>
Authorization: Bearer <your_token>
```

**Request Body:**

```json
{
  "content": "Updated comment"
}
```

---

### ▶ Delete a Comment

```
DELETE /comments/<comment_id>
Authorization: Bearer <your_token>
```

---

## 🧪 Using Swagger UI

Swagger UI is available for interactive API documentation and testing.

### 📍 URL

```
http://localhost:5000/apidocs
```

### 🛡 Authorize with JWT

1. Click the `Authorize` button at the top of Swagger UI.
2. Enter the token as:

   ```
   Bearer <your_token>
   ```

3. Now, all authenticated endpoints are usable from the UI.

---

## 🛠 Example `curl` Commands

### 🔐 Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{"username":"jeet2103","password":"Jeet1234"}'
```

### 📝 Create a Post

```bash
curl -X POST http://localhost:5000/api/posts \
-H "Authorization: Bearer <your_token>" \
-H "Content-Type: application/json" \
-d '{"title":"New Post","content":"Post content goes here"}'
```

---

## 🧪 Tools Recommended

- **Swagger UI**: For interactive API documentation
- **Postman**: For token-based testing
- **curl**: For command-line testing
- **pytest**: For unit testing

---

## 📘 Important Notes

- All POST/PUT requests must have `Content-Type: application/json`.
- Only authenticated users can create, update, or delete posts/comments.
- Only authors of posts/comments can modify or delete their content.
