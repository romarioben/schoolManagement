# Shool Management System

## Project Structure
- alembic/: Database migration scripts
- auth_app/: Authentication module (Python files)
- config/: Configuration files
- main_app/: Core application
- routing/: API routing logic

## How to Run
1. Customize environment variables:
```bash
cp .env.example .env
# Then edit .env to set your configuration values
``` 
2. Install virtual environment (if not already created):
```bash
python -m venv venv
``` 
3. Activate virtual environment:
```bash
source venv/bin/activate
``` 
4. Install dependencies:
```bash
pip install -r requirements.txt
``` 
5. Apply database migrations:
```bash
alembic upgrade head
``` 
6. Run the application:
```bash
fastapi dev
``` 

Environment variables are loaded from `.env` file. Alembic automatically handles database schema migrations when using `alembic upgrade head`.

## Routes Overview
The `main_routes.py` file defines API endpoints organized into the following sections:

### Student Routes
- `POST /students/`: Create a new student
- `GET /students/`: List all students (with pagination)
- `GET /students/{student_id}`: Get details of a specific student
- `PUT /students/{student_id}`: Update a student's information
- `DELETE /students/{student_id}`: Delete a student

### Parent Routes
- `POST /parents/`: Create a new parent
- `GET /parents/`: List all parents (with pagination)
- `GET /parents/{parent_id}`: Get details of a specific parent
- `PUT /parents/{parent_id}`: Update a parent's information
- `DELETE /parents/{parent_id}`: Delete a parent

### Student-Parent Associations
- `POST /students/{student_id}/parents/{parent_id}`: Assign or update a student-parent relationship
- `GET /students/{student_id}/parents/{parent_id}`: Get details of a specific association
- `PUT /students/{student_id}/parents/{parent_id}`: Update an existing association
- `DELETE /students/{student_id}/parents/{parent_id}`: Remove a student-parent association

### Level Routes
- `POST /levels/`: Create a new school level
- `GET /levels/`: List all school levels
- `GET /levels/{level_id}`: Get details of a specific level
- `PUT /levels/{level_id}`: Update a level
- `DELETE /levels/{level_id}`: Delete a level

### Series Routes
- `POST /series/`: Create a new school series
- `GET /series/`: List all school series
- `GET /series/{serie_id}`: Get details of a specific series
- `PUT /series/{serie_id}`: Update a series
- `DELETE /series/{serie_id}`: Delete a series

### School Class Routes
- `POST /classes/`: Create a new school class
- `GET /classes/`: List all school classes
- `GET /classes/{class_id}`: Get details of a specific class
- `PUT /classes/{class_id}`: Update a class
- `DELETE /classes/{class_id}`: Delete a class

### School Year Routes
- `POST /school-years/`: Create a new school year
- `GET /school-years/`: List all school years
- `GET /school-years/{school_year_id}`: Get details of a specific school year
- `PUT /school-years/{school_year_id}`: Update a school year
- `DELETE /school-years/{school_year_id}`: Delete a school year

### Period Routes
- `POST /periods/`: Create a new period
- `GET /periods/`: List all periods
- `GET /periods/{period_id}`: Get details of a specific period
- `GET /school-years/{school_year_id}/periods`: List periods by school year
- `PUT /periods/{period_id}`: Update a period
- `DELETE /periods/{period_id}`: Delete a period

### Subject Routes
- `POST /subjects/`: Create a new subject
- `GET /subjects/`: List all subjects
- `GET /subjects/{subject_id}`: Get details of a specific subject
- `PUT /subjects/{subject_id}`: Update a subject
- `DELETE /subjects/{subject_id}`: Delete a subject

### Class-Subject Associations
- `POST /class-subjects/`: Link a subject to a class
- `GET /classes/{class_id}/subjects/{period_id}`: Get subjects for a class in a specific period
- `PUT /classes/{class_id}/subjects/{period_id}`: Update class-subject-period relationships
- `DELETE /classes/{class_id}/subjects/{period_id}`: Remove class-subject-period relationships

### Teacher Routes
- `POST /teachers/`: Create a new teacher
- `GET /teachers/`: List all teachers
- `GET /teachers/{teacher_id}`: Get details of a specific teacher
- `PUT /teachers/{teacher_id}`: Update a teacher
- `DELETE /teachers/{teacher_id}`: Delete a teacher
- `POST /teachers/{teacher_id}/subjects/{subject_id}`: Assign a subject to a teacher
- `DELETE /teachers/{teacher_id}/subjects/{subject_id}`: Remove a subject from a teacher

### Teacher-Class-Subject-Period Associations
- `POST /teacher-class-subject-period/`: Create a teacher-class-subject-period association
- `DELETE /teacher-class-subject-period/teacher/{teacher_id}/school-class/{school_class_id}/subject/{subject_id}/period/{period_id}`: Delete a teacher-class-subject-period association

All routes follow RESTful conventions and include appropriate HTTP status codes. Authentication requirements vary by route, with some requiring admin/superadmin privileges (marked in route descriptions).