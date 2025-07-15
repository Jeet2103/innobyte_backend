# RESTful API Design – Blog Application

## ✅ User Authentication
| Method | Endpoint         | Auth | Description          |
|--------|------------------|------|----------------------|
| POST   | /auth/register   | ❌   | Register new user    |
| POST   | /auth/login      | ❌   | Login and get token  |

## 📝 Blog Post Management
| Method | Endpoint         | Auth | Description              |
|--------|------------------|------|--------------------------|
| POST   | /posts           | ✅   | Create a new post        |
| GET    | /posts           | ❌   | Get all posts            |
| GET    | /posts/<id>      | ❌   | Get single post by ID    |
| PUT    | /posts/<id>      | ✅   | Update post (owner only) |
| DELETE | /posts/<id>      | ✅   | Delete post (owner only) |

## 💬 Comment Management
| Method | Endpoint               | Auth | Description                |
|--------|------------------------|------|----------------------------|
| POST   | /comments              | ✅   | Add comment to post        |
| GET    | /comments?post_id=<id> | ❌   | List comments for a post   |
| GET    | /comments/<id>         | ❌   | Get single comment by ID   |
| PUT    | /comments/<id>         | ✅   | Update comment (owner only)|
| DELETE | /comments/<id>         | ✅   | Delete comment (owner only)|
