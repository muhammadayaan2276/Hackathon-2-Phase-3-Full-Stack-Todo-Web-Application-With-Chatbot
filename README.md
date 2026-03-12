# 🤖 Todo Chatbot - Full Stack Web Application (Hackathon Phase 3)

A full-stack **Todo Management Web Application** with a **Chatbot Assistant** that provides insights about a user's todos.
Built using **Next.js, FastAPI, PostgreSQL, and Tailwind CSS**.

---

## 🚀 Features

### 📝 Todo Management

* Create new todos
* View all todos
* Update existing todos
* Delete todos
* Mark todos as completed

### 🔐 Authentication

* User Signup & Login
* JWT-based authentication
* Protected routes

### 🤖 Chatbot Assistant

The chatbot **does not create or modify todos**.
Instead, it provides **information and insights about the user's existing todos**.

Examples:

* Total number of todos created
* Completed vs pending todos
* Information about the user's tasks

The chatbot fetches this data through the backend API.

### 📱 Responsive UI

* Built with **Next.js**
* Styled using **Tailwind CSS**

---

## 🛠 Tech Stack

**Frontend**

* Next.js
* TypeScript
* Tailwind CSS

**Backend**

* FastAPI
* Python
* SQLAlchemy

**Database**

* PostgreSQL

---

## 📂 Project Structure

```
project-root
│
├── backend
│   └── src
│       ├── api
│       ├── models
│       ├── schemas
│       └── main.py
│
├── frontend
│   ├── app
│   ├── components
│   └── lib
│
└── README.md
```

---

## ⚙️ Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Backend runs on:

```
http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```
http://localhost:3000
```

---

## 🔗 API Endpoints

### Authentication

```
POST /signup
POST /login
```

### Todos

```
GET /todos
POST /todos
PUT /todos/{id}
DELETE /todos/{id}
```

### Chatbot

```
POST /chat
```

The `/chat` endpoint allows the chatbot to **retrieve information about the user's todos** and respond with useful insights.

---

## 👨‍💻 Author

**Ayaan Zeeshan**
Computer Science Student | Full Stack Developer
Learning **Next.js, FastAPI, and AI integrations**

---

⭐ If you like this project, consider giving it a **star on GitHub**.
