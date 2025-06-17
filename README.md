# 🚀 Blogifyon - A Modern Blogging Platform 🚀

Blogifyon is a modern, full-featured blogging platform built with Django and ReactJS. It allows users to write, edit, and share blog posts with rich formatting using CKEditor5. The platform also offers user interaction features like likes, comments, saving posts, and real-time notifications.

---

## ✨ Features

- 🔐 **User Authentication**
  - Register, login, logout
  - Email verification for account activation
  - Password reset functionality

- 🔒 **CAPTCHA Protection**
  - Integrated CAPTCHA in registration & login to prevent bot attacks.

- 📝 **Rich Text Editor (CKEditor5)**
  - Fully integrated rich-text editor for creating beautiful blog posts with images, and formatted content.

- ⚡ **Real-Time Notifications**
  - Powered by Django Channels and WebSockets.

- 🔍 **Search & Filter System**
  - Search posts by title, category, and filter results.

- ❤️ **User Engagement**
  - Like posts
  - Comment & reply system
  - Save favorite posts

- 🖼️ **Profile Management**
  - Edit user profile
  - Upload profile picture

- 🚀 **Performance Optimization**
  - Redis integration for real-time WebSocket notifications and caching.

---

## 🛠 Tech Stack

### Frontend
- React.js
- Tailwind CSS
- React Router
- CKEditor5

### Backend
- Django
- Django Rest Framework (DRF)
- Django Channels (WebSockets)
- Redis (for real-time notifications & caching)


### Deployment
- Frontend: Vercel
- Backend: Render

---

## 🔗 Live Demo

👉 [https://blogifyon.vercel.app/](https://blogifyon.vercel.app/)

---

## 📂 Project Repositories

- 🖥 **Frontend** — [Blogifyon-Frontend GitHub](https://github.com/saminmahmud/Blogifyon-Frontend.git)
- 🖥 **Backend** — [Blogifyon-Backend GitHub](https://github.com/saminmahmud/Blogifyon-Backend.git)

---

---
### API Documentation
- 🖥 **Swagger UI**: [Swagger UI Url](https://blogifyon-backend-fghv.onrender.com/api/schema/swagger-ui/)
- 🖥 **Redoc**: [Redoc Url](https://blogifyon-backend-fghv.onrender.com/api/schema/redoc/)
---

## 🚀 Installation & Setup

### Backend (Django)

1️⃣ Clone the repository:

```bash
git clone https://github.com/saminmahmud/Blogifyon-Backend.git
cd Blogifyon-Backend
```

2️⃣ Create virtual environment and activate it:

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

3️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

4️⃣ Setup environment variables (.env file)

```bash
ENVIRONMENT=development # or production
EMAIL=
EMAIL_PASSWORD=
DATA_SITE_KEY=
RECAPTCHA_SECRET_KEY=
REDIS_URL=
SECRET_KEY=
```
5️⃣ Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6️⃣ Run server:
```bash
python manage.py runserver
```

7️⃣ Start Redis server and Django Channels for WebSockets support.


### Frontend (React)

1️⃣ Clone frontend repo:
```bash
git clone https://github.com/saminmahmud/Blogifyon-Frontend.git
cd Blogifyon-Frontend
```

3️⃣ Create .env file and configure backend API URL.
```bash
VITE_SITE_KEY=YOUR_CAPTCHA_SITE_KEY
```
4️⃣ Change baseUrl & SOCKET_URL from src/baseUrl/baseUrl.js

5️⃣ Start development server:
```bash
npm run dev
```
