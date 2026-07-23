from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from auth_app.auth import hash_password
from . import models, schemas
from auth_app.models import User

# --- CRUD STUDENTS ---
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: schemas.StudentCreate):
    matricule_exists = db.query(models.Student).filter(models.Student.studentMatricule == student.studentMatricule).first()
    if matricule_exists:
        raise HTTPException(status_code=400, detail="Ce numéro matricule est déjà utilisé pour un autre étudiant.")
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student: schemas.StudentCreate):
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    for key, value in student.model_dump().items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    db.delete(db_student)
    db.commit()
    return db_student


# --- CRUD PARENTS ---
def get_parent(db: Session, parent_id: int):
    return db.query(models.Parent).filter(models.Parent.id == parent_id).first()

def get_parents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Parent).offset(skip).limit(limit).all()

def create_parent(db: Session, parent: schemas.ParentCreate):
    #print(parent.model_dump())
    existing_user = db.query(User).filter(User.email == parent.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    
    db_parent = models.Parent(
        profession=parent.profession,
        username=parent.username,
        surname=parent.surname,
        firstname=parent.firstname,
        phone_number=parent.phone_number,
        role=parent.role,
        hashed_password=hash_password(parent.password),
        email=parent.email,
    )
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    # db.refresh(db_user)
    return db_parent

def update_parent(db: Session, parent_id: int, parent: schemas.ParentCreate):
    db_parent = get_parent(db, parent_id)
    if not db_parent:
        return None
    for key, value in parent.model_dump().items():
        setattr(db_parent, key, value)
    db.commit()
    db.refresh(db_parent)
    return db_parent

def delete_parent(db: Session, parent_id: int):
    db_parent = get_parent(db, parent_id)
    if not db_parent:
        return None
    db.delete(db_parent)
    db.commit()
    return db_parent


# --- CRUD ASSOCIATION MANY-TO-MANY (AVEC ATTRIBUT) ---

def get_association(db: Session, student_id: int, parent_id: int):
    return db.query(models.StudentParentAssociation).filter_by(
        student_id=student_id, parent_id=parent_id
    ).first()

def assign_parent_to_student(db: Session, student_id: int, parent_id: int, link_data: schemas.StudentParentLinkCreate):
    student = get_student(db, student_id)
    parent = get_parent(db, parent_id)
    
    if not student or not parent:
        return None
        
    existing_assoc = get_association(db, student_id, parent_id)
    
    if existing_assoc:
        existing_assoc.parent_type = link_data.parent_type
    else:
        association = models.StudentParentAssociation(
            student_id=student_id,
            parent_id=parent_id,
            parent_type=link_data.parent_type
        )
        db.add(association)
        
    db.commit()
    db.refresh(student)
    return student

def update_association(db: Session, student_id: int, parent_id: int, link_data: schemas.StudentParentLinkCreate):
    association = get_association(db, student_id, parent_id)
    if not association:
        return None
    association.parent_type = link_data.parent_type
    db.commit()
    db.refresh(association)
    return association

def remove_parent_from_student(db: Session, student_id: int, parent_id: int):
    student = get_student(db, student_id)
    association = get_association(db, student_id, parent_id)
    
    if not student or not association:
        return None
        
    db.delete(association)
    db.commit()
    db.refresh(student)
    return student