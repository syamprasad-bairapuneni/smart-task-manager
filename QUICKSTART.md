# Quick Start Guide

## 🚀 Fastest Way to Get Started

### Using Docker (Recommended - Easiest)

1. **Navigate to the project directory**
   ```bash
   cd smart-task-manager
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Wait for services to initialize** (about 30 seconds)
   ```bash
   docker-compose logs -f
   ```
   Press `Ctrl+C` to exit logs once you see services running

4. **Access the application**
   - Open your browser: **http://localhost:5173**
   - Create an account and start using!

### Manual Setup (Step by Step)

#### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (or copy from example)
echo "SECRET_KEY=my-super-secret-key-12345" > .env
echo "DATABASE_URL=mysql+pymysql://root:password@localhost:3306/task_manager" >> .env
echo "CORS_ORIGINS=http://localhost:5173" >> .env

# Make sure MySQL is running and create database
mysql -u root -p
CREATE DATABASE task_manager;
exit;

# Run the backend
python app.py
```

#### 2. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file (optional, defaults to http://localhost:5000)
echo "VITE_API_URL=http://localhost:5000" > .env

# Start development server
npm run dev
```

#### 3. Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## 📝 First Steps After Starting

1. **Register a new account** at http://localhost:5173/register
2. **Login** with your credentials
3. **Create your first task** using the "New Task" button
4. **Explore the Dashboard** to see your productivity stats
5. **Check Analytics** for detailed insights

## 🐛 Troubleshooting

### Database Connection Issues
- Make sure MySQL is running
- Check your database credentials in `.env`
- Verify the database `task_manager` exists

### Port Already in Use
- Backend (5000): Change port in `app.py` or kill the process using port 5000
- Frontend (5173): Vite will automatically use the next available port

### CORS Errors
- Make sure `CORS_ORIGINS` in backend `.env` matches your frontend URL
- Include both `http://localhost:5173` and `http://localhost:3000` if needed

### Docker Issues
- Make sure Docker Desktop is running
- Check logs: `docker-compose logs`
- Restart services: `docker-compose restart`

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API endpoints
- Customize the UI in `frontend/src`
- Add new features to the backend in `backend/routes/`

## 🎉 You're All Set!

Start managing your tasks and boosting your productivity! 🚀

