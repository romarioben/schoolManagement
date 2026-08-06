from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Adjust imports based on your project structure:
from config.database import get_db
from . import crud, schemas

from auth_app.auth import get_current_active_user, require_admin_or_superadmin

router = APIRouter(tags=["Marks & Mark Types"], prefix="/mark-app", dependencies=[Depends(get_current_active_user)])


# --- Mark Type Routes ---

@router.post("/mark-types/", response_model=schemas.MarkTypeResponse, status_code=status.HTTP_201_CREATED)
def create_mark_type(mark_type: schemas.MarkTypeCreate, db: Session = Depends(get_db)):
    return crud.create_mark_type(db=db, mark_type=mark_type)


@router.get("/mark-types/", response_model=List[schemas.MarkTypeResponse])
def read_mark_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_mark_types(db, skip=skip, limit=limit)


@router.get("/mark-types/{mark_type_id}", response_model=schemas.MarkTypeResponse)
def read_mark_type(mark_type_id: int, db: Session = Depends(get_db)):
    db_mark_type = crud.get_mark_type(db, mark_type_id=mark_type_id)
    if db_mark_type is None:
        raise HTTPException(status_code=404, detail="Mark type not found")
    return db_mark_type


@router.put("/mark-types/{mark_type_id}", response_model=schemas.MarkTypeResponse)
def update_mark_type(mark_type_id: int, mark_type: schemas.MarkTypeUpdate, db: Session = Depends(get_db)):
    db_mark_type = crud.update_mark_type(db, mark_type_id=mark_type_id, mark_type_update=mark_type)
    if db_mark_type is None:
        raise HTTPException(status_code=404, detail="Mark type not found")
    return db_mark_type


@router.delete("/mark-types/{mark_type_id}", response_model=schemas.MarkTypeResponse)
def delete_mark_type(mark_type_id: int, db: Session = Depends(get_db)):
    db_mark_type = crud.delete_mark_type(db, mark_type_id=mark_type_id)
    if db_mark_type is None:
        raise HTTPException(status_code=404, detail="Mark type not found")
    return db_mark_type


# --- Mark Routes ---

@router.post("/marks/", response_model=schemas.MarkResponse, status_code=status.HTTP_201_CREATED)
def create_mark(mark: schemas.MarkCreate, db: Session = Depends(get_db)):
    return crud.create_mark(db=db, mark=mark)


@router.get("/marks/", response_model=List[schemas.MarkResponse])
def read_marks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_marks(db, skip=skip, limit=limit)


@router.get("/marks/{mark_id}", response_model=schemas.MarkResponse)
def read_mark(mark_id: int, db: Session = Depends(get_db)):
    db_mark = crud.get_mark(db, mark_id=mark_id)
    if db_mark is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    return db_mark


# @router.get("/students/{student_id}/marks", response_model=List[schemas.MarkResponse])
# def read_marks_by_student(student_id: int, db: Session = Depends(get_db)):
#     return crud.get_marks_by_student(db, student_id=student_id)


@router.put("/marks/{mark_id}", response_model=schemas.MarkResponse)
def update_mark(mark_id: int, mark: schemas.MarkUpdate, db: Session = Depends(get_db)):
    db_mark = crud.update_mark(db, mark_id=mark_id, mark_update=mark)
    if db_mark is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    return db_mark


@router.delete("/marks/{mark_id}", response_model=schemas.MarkResponse)
def delete_mark(mark_id: int, db: Session = Depends(get_db)):
    db_mark = crud.delete_mark(db, mark_id=mark_id)
    if db_mark is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    return db_mark