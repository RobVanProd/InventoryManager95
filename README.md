# InventoryManager95 🏢

A modern, user-friendly inventory management system built with Django and React.

## Features ✨

- Easy-to-use inventory tracking
- Real-time stock updates
- Modern, responsive UI
- Multi-user support with role-based access
- Detailed reporting and analytics
- Search and filter capabilities

## Tech Stack 🛠

- Backend: Django + Django REST Framework
- Frontend: React.js with Material-UI
- Database: PostgreSQL
- Authentication: JWT
- State Management: Redux Toolkit
- API Client: React Query

## Getting Started 🚀

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://localhost/inventory_db
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd inventory-management-ui
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## Development 🛠

### Code Quality

The project uses several tools to ensure code quality:

- Black for Python code formatting
- ESLint and Prettier for JavaScript/TypeScript
- Pre-commit hooks for consistent code style
- TypeScript for type safety

To set up pre-commit hooks:
```bash
pre-commit install
```

### Testing

Run backend tests:
```bash
python manage.py test
```

Run frontend tests:
```bash
cd inventory-management-ui
npm test
```

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

For support, please open an issue in the repository.