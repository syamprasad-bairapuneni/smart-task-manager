# 🚀 How to Run This Project

## Quick Start (Easiest Method)

Since you don't have MySQL installed, the project is now configured to use **SQLite** by default (no database setup needed!).

### Step 1: Start the Backend

Open **PowerShell** or **Command Prompt** in the project directory:

```powershell
# Navigate to backend
cd backend

# Activate virtual environment (if not already activated)
.\venv\Scripts\Activate.ps1

# Start the backend server
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

**Keep this terminal open!**

### Step 2: Start the Frontend

Open a **NEW** PowerShell/Command Prompt window:

```powershell
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start the frontend server
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Step 3: Access the Application

1. Open your browser
2. Go to: **http://localhost:5173**
3. Register a new account
4. Start using the Task Manager! 🎉

---

## Detailed Setup Instructions

### Prerequisites (You Already Have These ✅)
- ✅ Python 3.13.7
- ✅ Node.js v25.1.0

### Backend Setup (Already Done ✅)
Dependencies are installed and backend is ready to run!

### Frontend Setup (Need to Do)

1. **Install frontend dependencies:**
   ```powershell
   cd frontend
   npm install
   ```

2. **Start frontend:**
   ```powershell
   npm run dev
   ```

---

## 📝 What to Do After Starting

1. **Register:** Create your account at http://localhost:5173/register
2. **Login:** Sign in with your credentials
3. **Create Tasks:** Click "New Task" to add your first task
4. **View Dashboard:** See your productivity stats
5. **Check Analytics:** Explore detailed insights

---

## 🐛 Troubleshooting

### Backend Issues

**Port 5000 already in use:**
```powershell
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with the number from above)
taskkill /PID <PID> /F
```

**Module not found errors:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend Issues

**Port 5173 already in use:**
- Vite will automatically use the next available port (5174, 5175, etc.)
- Check the terminal output for the actual port

**npm install fails:**
```powershell
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
Remove-Item -Recurse -Force node_modules
npm install
```

**CORS errors:**
- Make sure backend is running on port 5000
- Check that frontend is trying to connect to http://localhost:5000

---

## 🔄 Using MySQL Instead (Optional)

If you want to use MySQL instead of SQLite:

1. **Install MySQL:**
   - Download from: https://dev.mysql.com/downloads/installer/
   - Or use MySQL via XAMPP/WAMP

2. **Create database:**
   ```sql
   CREATE DATABASE task_manager;
   ```

3. **Create `.env` file in backend folder:**
   ```
   SECRET_KEY=your-secret-key-change-in-production
   DATABASE_URL=mysql+pymysql://root:password@localhost:3306/task_manager
   CORS_ORIGINS=http://localhost:5173
   ```

4. **Restart backend**

---

## 📋 Summary

**To run the project:**

1. **Terminal 1 (Backend):**
   ```powershell
   cd backend
   .\venv\Scripts\Activate.ps1
   python app.py
   ```

2. **Terminal 2 (Frontend):**
   ```powershell
   cd frontend
   npm install  # First time only
   npm run dev
   ```

3. **Browser:**
   - Open http://localhost:5173
   - Register and enjoy! 🎉

---

## 🎯 Next Steps

- Read [README.md](README.md) for full documentation
- Check [QUICKSTART.md](QUICKSTART.md) for more details
- Customize the UI in `frontend/src/`
- Add features in `backend/routes/`

**Happy coding! 🚀**

