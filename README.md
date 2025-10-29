# Smart Task & Productivity Manager

A modern full-stack task management application with productivity analytics, built with React, Flask, and MySQL.

## 🚀 Features

### Authentication
- JWT-based user authentication
- Secure signup, login, and logout
- Token refresh mechanism
- Role-based access control (Admin/User)

### Task Management
- Full CRUD operations for tasks
- Task properties: title, description, deadline, priority, status, category
- Advanced filtering, search, and sorting
- Task completion tracking with timestamps
- Category and priority labels

### Productivity Dashboard
- Visual charts and graphs using Recharts
- Weekly productivity trends
- Task completion statistics
- Category and priority distribution
- Recent tasks overview

### Analytics & Insights
- Calculate most productive day and hour
- Track average task completion time
- Productivity patterns analysis
- Comprehensive data visualization

### Focus & Time Management
- Pomodoro timer with presets (5/15/25/45/60) and custom duration (1–60 mins)
- Start/Pause/Reset controls with progress ring
- Optional bell sound on session completion

### UI/UX
- Modern, responsive design with TailwindCSS
- Dark/Light mode toggle
- Smooth animations and transitions
- Loading states and error handling
- Toast notifications

### Platform & Ops
- Health check endpoint (`GET /api/health`)
- CORS configuration for local and hosted environments
- Dockerized development setup for frontend, backend, and database
- Flexible database support: MySQL in production, SQLite fallback for local dev

## 🛠️ Tech Stack

### Frontend
- **React.js 18** - UI library
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Recharts** - Data visualization
- **Lucide React** - Icons
- **React Router** - Routing
- **Axios** - HTTP client
- **React Hot Toast** - Notifications

### Backend
- **Python 3.11** - Programming language
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **PyJWT** - JWT authentication
- **PyMySQL** - MySQL adapter
- **Flask-CORS** - CORS handling
  
  Note: The backend supports a SQLite fallback when `DATABASE_URL` is not provided, making local setup easy.

### Database
- **MySQL 8.0** - Relational database

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- npm or yarn

## 🔧 Installation & Setup

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   cd smart-task-manager
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - MySQL database on port 3306
   - Backend API on port 5000
   - Frontend on port 5173

3. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**
   - Create a MySQL database named `task_manager`
   - Update the database connection in `.env` file:
     ```
     DATABASE_URL=mysql+pymysql://username:password@localhost:3306/task_manager
     ```

5. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Initialize database**
   ```bash
   # Run schema.sql in MySQL or let Flask create tables
   python app.py
   ```

7. **Start the backend server**
   ```bash
   python app.py
   ```
   Backend will run on http://localhost:5000

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env if needed (default: http://localhost:5000)
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```
   Frontend will run on http://localhost:5173

## 📁 Project Structure

```
smart-task-manager/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── models.py              # SQLAlchemy models
│   ├── requirements.txt       # Python dependencies
│   ├── routes/
│   │   ├── auth_routes.py     # Authentication endpoints
│   │   ├── task_routes.py     # Task CRUD endpoints
│   │   └── analytics_routes.py # Analytics endpoints
│   └── utils/
│       ├── auth.py            # JWT utilities
│       └── helpers.py         # Helper functions
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── context/          # React context providers
│   │   ├── App.jsx           # Main app component
│   │   └── main.jsx          # Entry point
│   ├── package.json
│   └── tailwind.config.js
├── database/
│   └── schema.sql            # Database schema
├── docker-compose.yml        # Docker configuration
└── README.md
```

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Tasks
- `GET /api/tasks/` - Get all tasks (with filters)
- `GET /api/tasks/:id` - Get task by ID
- `POST /api/tasks/` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `PUT /api/tasks/:id/complete` - Toggle task completion

### Analytics
- `GET /api/analytics/stats` - Get productivity stats
- `GET /api/analytics/weekly` - Get weekly data
- `GET /api/analytics/productive-time` - Get productive time analysis
- `GET /api/analytics/completion-time` - Get average completion time
- `GET /api/analytics/dashboard` - Get complete dashboard data

## 🚢 Deployment

### Render / Railway / Azure

#### Backend Deployment
1. Set environment variables:
   - `SECRET_KEY` - A strong secret key
   - `DATABASE_URL` - Your MySQL connection string
   - `CORS_ORIGINS` - Your frontend URL

2. Update `requirements.txt` if needed

3. Deploy to your chosen platform

#### Frontend Deployment
1. Update `VITE_API_URL` in environment variables to your backend URL

2. Build the application:
   ```bash
   npm run build
   ```

3. Deploy the `dist` folder to your hosting service

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest  # If you add tests
```

### Frontend Testing
```bash
cd frontend
npm test  # If you add tests
```

## 📝 Environment Variables

### Backend (.env)
```
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=mysql+pymysql://user:password@host:port/database
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built with ❤️ for productivity and learning

---

## 🎯 Future Enhancements

- [ ] Email notifications for task deadlines
- [ ] AI-powered task suggestions
- [ ] Calendar integration
- [ ] Team collaboration features
- [ ] Mobile app (React Native)
- [ ] Advanced analytics with ML predictions
- [ ] Task templates
- [ ] Export/Import functionality
- [ ] Time tracking


