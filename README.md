# Blog RESTful API 🚀

A fully featured **RESTful Blog API** built using Flask, SQLAlchemy, Marshmallow, and JWT. This project supports creating, updating, and deleting blog posts and comments with full user authentication and role-based access control.

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Tools & Technologies Used](#tools--technologies-used)
3. [Project Methodology](#project-methodology)
4. [Codebase Structure](#codebase-structure)
5. [Environment Setup](#environment-setup)
    - [Using Conda](#using-conda)
    - [Using Python venv](#using-python-venv)
6. [Cloning the Repository](#cloning-the-repository)
7. [Installing Dependencies](#installing-dependencies)
8. [Setting up Environment Variables](#setting-up-environment-variables)
9. [Database Setup](#database-setup)
10. [Running the Application](#running-the-application)
11. [Using the API](#using-the-api)
12. [API User Guide](#api-user-guide)

---

## 📖 Overview

This API allows users to:
- Register and authenticate using JWT.
- Create, read, update, and delete blog posts.
- Add and manage comments on posts.
- Secure access using role-based control.
- Use Swagger UI to test and explore the API.

---

## ⚙️ Tools & Technologies Used

- **Python 3.10**
- **Flask** — Web framework
- **Flask-JWT-Extended** — Authentication
- **SQLAlchemy** — ORM for PostgreSQL
- **Marshmallow** — Data serialization
- **Flask-Migrate** — Database migrations
- **PostgreSQL** — Relational database
- **Swagger UI** — API documentation
- **Pytest** — Automated testing

---

## 🧭 Project Methodology

This project was developed using a modular, scalable, and test-driven approach:

1. **Requirement Analysis** — Define essential routes and functionality.
2. **Database Design** — Normalize schemas and set up relationships.
3. **API Development** — Build routes for users, posts, and comments.
4. **Authentication** — Secure endpoints using JWT.
5. **Testing** — Write unit and integration tests using Pytest.
6. **Documentation** — Use Swagger UI and markdown for developer usability.
7. **Logging & Error Handling** — Robust logging for maintainability.
8. **Deployment Ready** — Portable with environment configuration support.

---

## 📁 Codebase Structure

```
flask-blog-api/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── logger.py
│   ├── swagger_config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   ├── post_schema.py
│   │   └── comment_schema.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── post_routes.py
│   │   └── comment_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth_service.py
│   └── utils/
│       ├── __init__.py
│       └── decorators.py
│
├── migrations/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_posts.py
│   └── test_comments.py
|
├── db/
│   ├── create_db.py
│   └── schema.sql
├── docs/
│   └── api_endpoints.md
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
└── wsgi.py

```

---

## 🛠️ Environment Setup

### Using Conda

```bash
conda create -n blogapi python=3.10
conda activate blogapi
```

### Using Python venv

```bash
python -m venv blogapi
blogapi\Scripts\activate     # On Windows
# OR
source blogapi/bin/activate    # On Unix/macOS
```

---

## 🔄 Cloning the Repository

```bash
git clone https://github.com/your-username/innobyte_backend.git
cd innobyte_backend
```

---

## 📦 Installing Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Setting up Environment Variables

Create a `.env` file in the root directory with the following content:

```env
FLASK_ENV=development
FLASK_APP=run.py
DEBUG=True
DB_NAME=blogdb
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DATABASE_URL = postgresql://<username>:<password>@<host>:<port>/<database_name>
JWT_SECRET_KEY=your_secret_key
```

Make sure PostgreSQL is running and the credentials match your local configuration.

---

## 🗃️ Database Setup

Run the following to create the database and tables:

```bash
python db/create_db.py
flask db upgrade
```

You can also use the custom command:

```bash
flask db-upgrade
```

---

## ▶️ Running the Application

To start the server:

```bash
python run.py
```

The API will be available at: `http://localhost:5000`

To view Swagger UI:  
`http://localhost:5000/apidocs/`

---

## 🧪 Using the API

- Refer to [docs/api_endpoints.md](docs/api_endpoints.md) for a complete list of API endpoints, request/response formats, route methods, and response status codes.


- Refer to [USER_GUIDE.md](./USER_GUIDE.md) for complete usage instructions, including authentication flow and example requests using Swagger, Postman, and curl.

---

## 📘 API User Guide

Check out [`USER_GUIDE.md`](./USER_GUIDE.md) to learn how to:
- Register and log in
- Use JWT tokens
- Access post and comment endpoints
- Automate token usage in Swagger

---

## 👨‍💻 Developed by Jeet Nandigrami.
