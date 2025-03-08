# MultiAuth

MultiAuth is a multi-tenant authentication system that supports both **email/password** authentication and **Google OAuth**. It allows different organizations (tenants) to have isolated authentication while enabling admin functionalities for user management.

## 🚀 Features
- **User Authentication** (Signup/Login with Email & Password)
- **Google OAuth Authentication**
- **Multi-Tenant Support** (Users belong to different organizations)
- **Admin Functionality** (Admins can see users in their tenant and promote them)
- **Session Handling with JWT Tokens**
- **Frontend in React (Vite) and Backend in Flask**

---

## 🛠️ Tech Stack
- **Frontend:** React (Vite), TypeScript, Axios, TailwindCSS
- **Backend:** Flask, Flask-JWT-Extended, Flask-CORS, Flask-Session
- **Database:** SQLite (for local development), PostgreSQL (for production)
- **Authentication:** JWT for API protection, Google OAuth for third-party login

---

## 📥 Local Development Setup

### 1️⃣ **Clone the Repository**
```sh
 git clone https://github.com/your-repo/MultiAuth.git
 cd MultiAuth
```

### 2️⃣ **Set Up the Backend** (Flask)
```sh
cd backend
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate virtual environment (Mac/Linux)
venv\Scripts\activate  # Activate virtual environment (Windows)
```

#### **Install Dependencies**
```sh
pip install -r requirements.txt
```

#### **Create .env File** (Backend Config)
Create a `.env` file inside `backend/` and add:
```ini
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///multiauth.db
JWT_SECRET_KEY=your-jwt-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

#### **Run Flask Backend Locally**
```sh
flask db upgrade  # Apply migrations
flask run  # Start Backend (Runs on http://127.0.0.1:5000)
```

---

### 3️⃣ **Set Up the Frontend** (React + Vite)
```sh
cd ../frontend
npm install  # Install dependencies
```

#### **Run React Frontend Locally**
```sh
npm run dev  # Runs on http://127.0.0.1:5173
```

#### **Configure API URL in Frontend**
Inside `frontend/src/api/auth.ts`, update the backend API URL:
```ts
const API_URL = "http://127.0.0.1:5000/api";
```

---

## ✅ How to Use
1. **Sign up** with a tenant name (first user in a tenant is admin)
2. **Log in** using Email/Password or Google OAuth
3. **Admins can see users** in their tenant (`/api/users`)
4. **Admins can promote users** to admins (`/api/promote`)
5. **Logout & Session Handling**

---

## 🔥 Common Issues & Fixes

### **1️⃣ Backend Doesn't Start?**
- Ensure the `.env` file is properly set up.
- Run `flask db upgrade` to apply migrations.
- Restart the virtual environment:
  ```sh
  deactivate && source venv/bin/activate  # Mac/Linux
  deactivate && venv\Scripts\activate  # Windows
  ```

### **2️⃣ Frontend API Calls Fail?**
- Ensure backend is running on `http://127.0.0.1:5000`.
- Check if the API URL in `vite.config.ts` is correct.

### **3️⃣ Google OAuth Not Working?**
- Ensure **Google Client ID** and **Secret** are set in `.env`.
- Check **OAuth Redirect URI** in Google Developer Console.

---



