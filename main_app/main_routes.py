from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from config.database import get_db
from auth_app.auth import get_current_user

router = APIRouter(
    tags=["Students, Parents & Associations"],
    dependencies=[Depends(get_current_user)]
)

# ==================== ROUTES STUDENTS ====================

student_router = APIRouter(tags=["Students"], dependencies=[Depends(get_current_user)])
@student_router.post("/students/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student_route(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@student_router.get("/students/", response_model=List[schemas.StudentResponse])
def read_students_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_students(db=db, skip=skip, limit=limit)

@student_router.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student_route(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db=db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@student_router.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student_route(student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.update_student(db=db, student_id=student_id, student=student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_route(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db=db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return None


# ==================== ROUTES PARENTS ====================

parent_router = APIRouter(tags=["Parents"], dependencies=[Depends(get_current_user)])
@parent_router.post("/parents/", response_model=schemas.ParentResponse, status_code=status.HTTP_201_CREATED)
def create_parent_route(parent: schemas.ParentCreate, db: Session = Depends(get_db)):
    return crud.create_parent(db=db, parent=parent)

@parent_router.get("/parents/", response_model=List[schemas.ParentWithStudentsResponse])
def read_parents_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_parents(db=db, skip=skip, limit=limit)

@parent_router.get("/parents/{parent_id}", response_model=schemas.ParentResponse)
def read_parent_route(parent_id: int, db: Session = Depends(get_db)):
    db_parent = crud.get_parent(db=db, parent_id=parent_id)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent

@parent_router.put("/parents/{parent_id}", response_model=schemas.ParentResponse)
def update_parent_route(parent_id: int, parent: schemas.ParentCreate, db: Session = Depends(get_db)):
    db_parent = crud.update_parent(db=db, parent_id=parent_id, parent=parent)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent

@parent_router.delete("/parents/{parent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parent_route(parent_id: int, db: Session = Depends(get_db)):
    db_parent = crud.delete_parent(db=db, parent_id=parent_id)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return None


# ==================== ROUTES ASSOCIATION (STUDENT-PARENT) ====================

student_parent_router = APIRouter(tags=["Student-Parent Associations"], dependencies=[Depends(get_current_user)])
@student_parent_router.post("/students/{student_id}/parents/{parent_id}", response_model=schemas.StudentResponse)
def assign_parent_route(student_id: int, parent_id: int, link_data: schemas.StudentParentLinkCreate, db: Session = Depends(get_db)):
    """Associe ou met à jour le type de lien entre un étudiant et un parent."""
    result = crud.assign_parent_to_student(db=db, student_id=student_id, parent_id=parent_id, link_data=link_data)
    if not result:
        raise HTTPException(status_code=404, detail="Student or Parent not found")
    return result

@student_parent_router.get("/students/{student_id}/parents/{parent_id}", response_model=schemas.StudentParentLinkResponse)
def get_association_route(student_id: int, parent_id: int, db: Session = Depends(get_db)):
    """Récupère les détails d'une association spécifique (ex: parent_type)."""
    assoc = crud.get_association(db=db, student_id=student_id, parent_id=parent_id)
    if not assoc:
        raise HTTPException(status_code=404, detail="Association not found")
    return assoc

@student_parent_router.put("/students/{student_id}/parents/{parent_id}", response_model=schemas.StudentParentLinkResponse)
def update_association_route(student_id: int, parent_id: int, link_data: schemas.StudentParentLinkCreate, db: Session = Depends(get_db)):
    """Met à jour l'attribut (parent_type) d'une association existante."""
    assoc = crud.update_association(db=db, student_id=student_id, parent_id=parent_id, link_data=link_data)
    if not assoc:
        raise HTTPException(status_code=404, detail="Association not found")
    return assoc

@student_parent_router.delete("/students/{student_id}/parents/{parent_id}", response_model=schemas.StudentResponse)
def remove_parent_route(student_id: int, parent_id: int, db: Session = Depends(get_db)):
    """Supprime l'association entre un étudiant et un parent."""
    result = crud.remove_parent_from_student(db=db, student_id=student_id, parent_id=parent_id)
    if not result:
        raise HTTPException(status_code=404, detail="Student, Parent or Link not found")
    return result

main_router = APIRouter()
main_router.include_router(student_router)
main_router.include_router(parent_router)
main_router.include_router(student_parent_router)