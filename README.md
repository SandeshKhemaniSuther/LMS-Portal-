# LMS Portal - Learning Management System

A comprehensive Learning Management System built with Python FastAPI backend and Laravel frontend.

## Features

### Core Features
- User authentication (Students, Instructors, Admins)
- Course creation and management
- Student enrollment and progress tracking
- Video and document content delivery
- Assessments and grading system
- Discussion forums and messaging
- Analytics and reporting

### Advanced Features
- Live streaming capabilities
- Certificate generation
- Payment integration
- Mobile responsive design
- Multi-language support
- Real-time notifications

## Technology Stack

### Backend (Python FastAPI)
- FastAPI for REST API
- SQLAlchemy for ORM
- PostgreSQL database
- Redis for caching
- JWT authentication
- WebSocket support

### Frontend (Laravel)
- Laravel 10 framework
- Vue.js 3 for SPA components
- Blade templates for server-side rendering
- Tailwind CSS for styling
- Inertia.js for seamless navigation

## Installation

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
composer install
npm install
npm run dev
php artisan serve
```

## API Documentation
API documentation available at: `http://localhost:8000/docs`

## Project Structure
```
lms-portal/
├── backend/                 # Python FastAPI
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── alembic/            # Database migrations
│   └── tests/              # Backend tests
├── frontend/               # Laravel
│   ├── app/
│   │   ├── Http/           # Controllers
│   │   ├── Models/         # Eloquent models
│   │   └── Views/          # Blade templates
│   ├── resources/js/       # Vue.js components
│   ├── database/           # Laravel migrations
│   └── tests/              # Frontend tests
└── docs/                   # Documentation
```

## License
MIT License
