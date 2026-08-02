from typing import Optional

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
    existing_username = db.query(User).filter(User.username == parent.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    
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


def create_level(db: Session, level: schemas.LevelCreate):
  db_level = models.Level(levelName=level.levelName)
  db.add(db_level)
  db.commit()
  db.refresh(db_level)
  return db_level


def get_levels(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Level).offset(skip).limit(limit).all()


def get_level(db: Session, level_id: int):
  return db.query(models.Level).filter(models.Level.id == level_id).first()


def update_level(db: Session, level_id: int, level: schemas.LevelCreate):
  db_level = get_level(db, level_id)
  if not db_level:
    return None
  db_level.levelName = level.levelName
  db.commit()
  db.refresh(db_level)
  return db_level


def delete_level(db: Session, level_id: int):
  db_level = get_level(db, level_id)
  if not db_level:
    return None
  db.delete(db_level)
  db.commit()
  return db_level


# ==================== SERIE CRUD ====================


def create_serie(db: Session, serie: schemas.SerieCreate):
  db_serie = models.Serie(serieName=serie.serieName)
  db.add(db_serie)
  db.commit()
  db.refresh(db_serie)
  return db_serie


def get_series(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Serie).offset(skip).limit(limit).all()


def get_serie(db: Session, serie_id: int):
  return db.query(models.Serie).filter(models.Serie.id == serie_id).first()


def update_serie(db: Session, serie_id: int, serie: schemas.SerieCreate):
  db_serie = get_serie(db, serie_id)
  if not db_serie:
    return None
  db_serie.serieName = serie.serieName
  db.commit()
  db.refresh(db_serie)
  return db_serie


def delete_serie(db: Session, serie_id: int):
  db_serie = get_serie(db, serie_id)
  if not db_serie:
    return None
  db.delete(db_serie)
  db.commit()
  return db_serie


# ==================== SCHOOL CLASS CRUD ====================


def create_school_class(db: Session, school_class: schemas.SchoolClassCreate):
  # Verify Level exists
  if not get_level(db, school_class.level_id):
    raise HTTPException(status_code=404, detail="Level not found")
  # Verify Serie exists if provided
  if school_class.serie_id and not get_serie(db, school_class.serie_id):
    raise HTTPException(status_code=404, detail="Serie not found")

  db_class = models.SchoolClass(**school_class.dict())
  db.add(db_class)
  db.commit()
  db.refresh(db_class)
  return db_class


def get_school_classes(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.SchoolClass).offset(skip).limit(limit).all()


def get_school_class(db: Session, class_id: int):
  return (
      db.query(models.SchoolClass)
      .filter(models.SchoolClass.id == class_id)
      .first()
  )


def update_school_class(
    db: Session, class_id: int, school_class: schemas.SchoolClassCreate
):
  db_class = get_school_class(db, class_id)
  if not db_class:
    return None

  if not get_level(db, school_class.level_id):
    raise HTTPException(status_code=404, detail="Level not found")
  if school_class.serie_id and not get_serie(db, school_class.serie_id):
    raise HTTPException(status_code=404, detail="Serie not found")

  for key, value in school_class.dict().items():
    setattr(db_class, key, value)

  db.commit()
  db.refresh(db_class)
  return db_class


def delete_school_class(db: Session, class_id: int):
  db_class = get_school_class(db, class_id)
  if not db_class:
    return None
  db.delete(db_class)
  db.commit()
  return db_class


def create_school_year(db: Session, name: str, startYear: int, endYear: int):
    db_school_year = models.SchoolYear(name=name, startYear=startYear, endYear=endYear)
    db.add(db_school_year)
    db.commit()
    db.refresh(db_school_year)
    return db_school_year

def get_school_year(db: Session, school_year_id: int):
    return db.query(models.SchoolYear).filter(models.SchoolYear.id == school_year_id).first()

def get_school_years(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SchoolYear).offset(skip).limit(limit).all()

def update_school_year(db: Session, school_year_id: int, name: str = None, startYear: int = None, endYear: int = None):
    db_school_year = get_school_year(db, school_year_id)
    if not db_school_year:
        return None
    
    if name is not None:
        db_school_year.name = name
    if startYear is not None:
        db_school_year.startYear = startYear
    if endYear is not None:
        db_school_year.endYear = endYear
        
    db.commit()
    db.refresh(db_school_year)
    return db_school_year

def delete_school_year(db: Session, school_year_id: int):
    db_school_year = get_school_year(db, school_year_id)
    if db_school_year:
        db.delete(db_school_year)
        db.commit()
        return True
    return False


# --- Period CRUD Operations ---

def create_period(db: Session, periodName: str, schoolYear_id: int):
    db_period = models.Period(periodName=periodName, schoolYear_id=schoolYear_id)
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    return db_period

def get_period(db: Session, period_id: int):
    return db.query(models.Period).filter(models.Period.id == period_id).first()

def get_periods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Period).offset(skip).limit(limit).all()

def get_periods_by_school_year(db: Session, schoolYear_id: int):
    return db.query(models.Period).filter(models.Period.schoolYear_id == schoolYear_id).all()

def update_period(db: Session, period_id: int, periodName: str = None, schoolYear_id: int = None):
    db_period = get_period(db, period_id)
    if not db_period:
        return None
        
    if periodName is not None:
        db_period.periodName = periodName
    if schoolYear_id is not None:
        db_period.schoolYear_id = schoolYear_id
        
    db.commit()
    db.refresh(db_period)
    return db_period

def delete_period(db: Session, period_id: int):
    db_period = get_period(db, period_id)
    if db_period:
        db.delete(db_period)
        db.commit()
        return True
    return False



def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()

def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subject).offset(skip).limit(limit).all()

def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(subjectName=subject.subjectName, domaine=subject.domaine)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def update_subject(db: Session, subject_id: int, subject_update: schemas.SubjectUpdate):
    db_subject = get_subject(db, subject_id)
    if not db_subject:
        return None
    for key, value in subject_update.model_dump(exclude_unset=True).items():
        setattr(db_subject, key, value)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def delete_subject(db: Session, subject_id: int):
    db_subject = get_subject(db, subject_id)
    if not db_subject:
        return None
    db.delete(db_subject)
    db.commit()
    return db_subject


# --- SchoolClass CRUD ---
def get_school_class(db: Session, class_id: int):
    return db.query(models.SchoolClass).filter(models.SchoolClass.id == class_id).first()

def get_school_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SchoolClass).offset(skip).limit(limit).all()

def create_school_class(db: Session, school_class: schemas.SchoolClassCreate):
    db_class = models.SchoolClass(name=school_class.name)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def update_school_class(db: Session, class_id: int, class_update: schemas.SchoolClassUpdate):
    db_class = get_school_class(db, class_id)
    if not db_class:
        return None
    for key, value in class_update.model_dump(exclude_unset=True).items():
        setattr(db_class, key, value)
    db.commit()
    db.refresh(db_class)
    return db_class

def delete_school_class(db: Session, class_id: int):
    db_class = get_school_class(db, class_id)
    if not db_class:
        return None
    db.delete(db_class)
    db.commit()
    return db_class


# --- Relationship CRUD (Association Class) ---
def get_class_subject_assoc(db: Session, class_id: int, subject_id: int, period_id: int):
    return db.query(models.ClassSubjectAssociation).filter(
        models.ClassSubjectAssociation.school_class_id == class_id,
        models.ClassSubjectAssociation.subject_id == subject_id,
        models.ClassSubjectAssociation.period_id == period_id
    ).first()
    

def create_class_subject_assoc(db: Session, assoc: schemas.ClassSubjectAssociationCreate):
    db_assoc = models.ClassSubjectAssociation(
        school_class_id=assoc.school_class_id,
        subject_id=assoc.subject_id,
        period_id=assoc.period_id,
        hours_per_week=assoc.hours_per_week,
        coefficient=assoc.coefficient,
        #room=assoc.room
    )
    db.add(db_assoc)
    db.commit()
    db.refresh(db_assoc)
    return db_assoc

def get_a_class_subjects(db: Session, class_id: int, period_id: int):
    associations = db.query(models.ClassSubjectAssociation).filter(models.ClassSubjectAssociation.school_class_id==class_id and models.ClassSubjectAssociation.period_id == period_id)
    return associations.all()

def update_class_subject_assoc(db: Session, class_id: int, subject_id: int, period_id: int, assoc_update: schemas.ClassSubjectAssociationUpdate):
    db_assoc = get_class_subject_assoc(db, class_id, subject_id, period_id)
    if not db_assoc:
        return None
    for key, value in assoc_update.model_dump(exclude_unset=True).items():
        setattr(db_assoc, key, value)
    db.commit()
    db.refresh(db_assoc)
    return db_assoc


def delete_class_subject_assoc(db: Session, class_id: int, subject_id: int, period_id: int):
    db_assoc = get_class_subject_assoc(db, class_id, subject_id, period_id)
    if not db_assoc:
        return None
    db.delete(db_assoc)
    db.commit()
    return db_assoc



def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()

def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    existing_user = db.query(models.User).filter(models.User.email == teacher.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username = db.query(models.User).filter(models.User.username == teacher.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    db_teacher = models.Teacher(
        username=teacher.username,
        email=teacher.email,
        hashed_password=hash_password(teacher.password),
        role="teacher",
        surname=teacher.surname,
        firstname=teacher.firstname,
        phone_number=teacher.phone_number,
        teacherMatricule=teacher.teacherMatricule
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def assign_subject_to_teacher(db: Session, teacher_id: int, subject_id: int):
    teacher = get_teacher(db, teacher_id)
    subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if teacher and subject:
        if subject not in teacher.subjects:
            teacher.subjects.append(subject)
            db.commit()
            db.refresh(teacher)
        else:
            raise HTTPException(status_code=400, detail="Subject already assigned to teacher")
    else:
        raise HTTPException(status_code=404, detail="Teacher or Subject not found")
    return teacher

def remove_subject_from_teacher(db: Session, teacher_id: int, subject_id: int):
    teacher = get_teacher(db, teacher_id)
    subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if teacher and subject:
        if subject in teacher.subjects:
            teacher.subjects.remove(subject)
            db.commit()
            db.refresh(teacher)
        else:
            raise HTTPException(status_code=400, detail="Subject not assigned to teacher")
    else:
        raise HTTPException(status_code=404, detail="Teacher or Subject not found")
    return teacher
  
  
def create_teacher_class_subject_period(db: Session, assoc: schemas.TeacherClassSubjectPeriodCreate):
    db_assoc = models.TeacherClassSubjectPeriod(
        teacher_id=assoc.teacher_id,
        school_class_id=assoc.school_class_id,
        subject_id=assoc.subject_id,
        period_id=assoc.period_id
    )
    db.add(db_assoc)
    db.commit()
    db.refresh(db_assoc)
    return db_assoc

def get_teacher_class_subject_periods(db: Session, teacher_id: Optional[int]=None, school_class_id: Optional[int]=None, subject_id: Optional[int]=None, period_id: Optional[int]=None):
    return db.query(models.TeacherClassSubjectPeriod).filter(
        (models.TeacherClassSubjectPeriod.teacher_id == teacher_id if teacher_id is not None else True) &
        (models.TeacherClassSubjectPeriod.school_class_id == school_class_id if school_class_id is not None else True) &
        (models.TeacherClassSubjectPeriod.subject_id == subject_id if subject_id is not None else True) &
        (models.TeacherClassSubjectPeriod.period_id == period_id if period_id is not None else True)
    ).all()

def delete_teacher_class_subject_period(db: Session, teacher_id: int, school_class_id: int, subject_id: int, period_id: int):
    db_assoc = db.query(models.TeacherClassSubjectPeriod).filter_by(
        teacher_id=teacher_id,
        school_class_id=school_class_id,
        subject_id=subject_id,
        period_id=period_id
    ).first()
    
    if not db_assoc:
        return None
    
    db.delete(db_assoc)
    db.commit()
    return db_assoc

def get_admin(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.id == admin_id).first()

def get_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Admin).offset(skip).limit(limit).all()

def create_admin(db: Session, admin: schemas.AdminCreate):
    existing_user = db.query(models.User).filter(models.User.email == admin.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username = db.query(models.User).filter(models.User.username == admin.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    db_admin = models.Admin(
        username=admin.username,
        email=admin.email,
        hashed_password=hash_password(admin.password),
        role="admin",
        surname=admin.surname,
        firstname=admin.firstname,
        phone_number=admin.phone_number,
        teacherMatricule=admin.teacherMatricule,
        poste=admin.poste
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_admin(db: Session, admin_id: int, admin_update: schemas.AdminCreate):
    db_admin = get_admin(db, admin_id)
    if not db_admin:
        return None
    for key, value in admin_update.model_dump(exclude_unset=True).items():
        setattr(db_admin, key, value)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, admin_id: int):
    db_admin = get_admin(db, admin_id)
    if not db_admin:
        return None
    db.delete(db_admin)
    db.commit()
    return db_admin


def get_superAdmin(db: Session, superAdmin_id: int):
    return db.query(models.SuperAdmin).filter(models.SuperAdmin.id == superAdmin_id).first()

def get_superAdmins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SuperAdmin).offset(skip).limit(limit).all()

def create_superAdmin(db: Session, superAdmin: schemas.SuperAdminCreate):
    existing_user = db.query(models.User).filter(models.User.email == superAdmin.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username = db.query(models.User).filter(models.User.username == superAdmin.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    db_superAdmin = models.SuperAdmin(
        username=superAdmin.username,
        email=superAdmin.email,
        hashed_password=hash_password(superAdmin.password),
        role="superadmin",
        surname=superAdmin.surname,
        firstname=superAdmin    .firstname,
        phone_number=superAdmin.phone_number,
        teacherMatricule=superAdmin.teacherMatricule,
        poste=superAdmin.poste
    )
    db.add(db_superAdmin)
    db.commit()
    db.refresh(db_superAdmin)
    return db_superAdmin

def update_superAdmin(db: Session, superAdmin_id: int, superAdmin_update: schemas.SuperAdminCreate):
    db_superAdmin = get_superAdmin(db, superAdmin_id)
    if not db_superAdmin:
        return None
    for key, value in superAdmin_update.model_dump(exclude_unset=True).items():
        setattr(db_superAdmin, key, value)
    db.commit()
    db.refresh(db_superAdmin)
    return db_superAdmin


def delete_superAdmin(db: Session, superAdmin_id: int):
    db_superAdmin = get_superAdmin(db, superAdmin_id)
    if not db_superAdmin:
        return None
    db.delete(db_superAdmin)
    db.commit()
    return db_superAdmin
