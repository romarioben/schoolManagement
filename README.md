# Shool Management System

## Project Structure
```
- alembic/: Database migration scripts
- auth_app/: Authentication module (Python files)
- config/: Configuration files
- main_app/: Core application
- routing/: API routing logic
```

## Requirements
Install dependencies with:
```bash
pip install -r requirements.txt
```

## How to Run
1. Activate virtual environment:
```bash
source venv/bin/activate
```
2. Run the application (adjust according to your entry point):
```bash
fastapi dev
```

## Configuration
Environment variables are loaded from `.env` file. Copy `.env.example` and customize as needed.