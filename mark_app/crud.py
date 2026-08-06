from typing import List, Optional
from sqlalchemy.orm import Session

from mark_app.schemas import MarkCreate, MarkTypeCreate, MarkTypeUpdate, MarkUpdate

from mark_app.schemas import MarkTypeCreate
# Assuming your models are imported from your models module
from .models import MarkType, Mark 


# --- MarkType CRUD ---

def get_mark_type(db: Session, mark_type_id: int) -> Optional[MarkType]:
    return db.query(MarkType).filter(MarkType.id == mark_type_id).first()


def get_mark_types(db: Session, skip: int = 0, limit: int = 100) -> List[MarkType]:
    return db.query(MarkType).offset(skip).limit(limit).all()


def create_mark_type(db: Session, mark_type: MarkTypeCreate) -> MarkType:
    db_mark_type = MarkType(**mark_type.model_dump())
    db.add(db_mark_type)
    db.commit()
    db.refresh(db_mark_type)
    return db_mark_type


def update_mark_type(db: Session, mark_type_id: int, mark_type_update: MarkTypeUpdate) -> Optional[MarkType]:
    db_mark_type = get_mark_type(db, mark_type_id)
    if not db_mark_type:
        return None
    
    update_data = mark_type_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_mark_type, key, value)
        
    db.commit()
    db.refresh(db_mark_type)
    return db_mark_type


def delete_mark_type(db: Session, mark_type_id: int) -> Optional[MarkType]:
    db_mark_type = get_mark_type(db, mark_type_id)
    if not db_mark_type:
        return None
    db.delete(db_mark_type)
    db.commit()
    return db_mark_type


# --- Mark CRUD ---

def get_mark(db: Session, mark_id: int) -> Optional[Mark]:
    return db.query(Mark).filter(Mark.id == mark_id).first()


def get_marks(db: Session, skip: int = 0, limit: int = 100) -> List[Mark]:
    return db.query(Mark).offset(skip).limit(limit).all()


# def get_marks_by_student(db: Session, student_id: int) -> List[Mark]:
#     return db.query(Mark).filter(Mark.student_id == student_id).all()


def create_mark(db: Session, mark: MarkCreate) -> Mark:
    db_mark = Mark(**mark.model_dump())
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark


def update_mark(db: Session, mark_id: int, mark_update: MarkUpdate) -> Optional[Mark]:
    db_mark = get_mark(db, mark_id)
    if not db_mark:
        return None
        
    update_data = mark_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_mark, key, value)
        
    db.commit()
    db.refresh(db_mark)
    return db_mark


def delete_mark(db: Session, mark_id: int) -> Optional[Mark]:
    db_mark = get_mark(db, mark_id)
    if not db_mark:
        return None
    db.delete(db_mark)
    db.commit()
    return db_mark