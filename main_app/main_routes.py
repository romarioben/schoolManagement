from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, crud
from config.database import get_db
from auth_app.auth import get_current_active_user, require_admin_or_superadmin


# ==================== ROUTES STUDENTS ====================

student_router = APIRouter(tags=["Students"], dependencies=[Depends(get_current_active_user)])
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

@student_router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_route(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db=db, student_id=student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return None


# ==================== ROUTES PARENTS ====================

parent_router = APIRouter(tags=["Parents"], dependencies=[Depends(get_current_active_user)])
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

student_parent_router = APIRouter(tags=["Student-Parent Associations"], dependencies=[Depends(get_current_active_user)])
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




# ==================== LEVEL ROUTES ====================

level_router = APIRouter(tags=["Levels"], dependencies=[Depends(require_admin_or_superadmin)])

@level_router.post(
    "/levels/",
    response_model=schemas.LevelResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_level(level: schemas.LevelCreate, db: Session = Depends(get_db)):
  return crud.create_level(db=db, level=level)


@level_router.get("/levels/", response_model=List[schemas.LevelResponse])
def read_levels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return crud.get_levels(db, skip=skip, limit=limit)


@level_router.get("/levels/{level_id}", response_model=schemas.LevelResponse)
def read_level(level_id: int, db: Session = Depends(get_db)):
  db_level = crud.get_level(db, level_id=level_id)
  if db_level is None:
    raise HTTPException(status_code=404, detail="Level not found")
  return db_level


@level_router.put("/levels/{level_id}", response_model=schemas.LevelResponse)
def update_level(
    level_id: int, level: schemas.LevelCreate, db: Session = Depends(get_db)
):
  db_level = crud.update_level(db, level_id=level_id, level=level)
  if db_level is None:
    raise HTTPException(status_code=404, detail="Level not found")
  return db_level


@level_router.delete("/levels/{level_id}", response_model=schemas.LevelResponse)
def delete_level(level_id: int, db: Session = Depends(get_db)):
  db_level = crud.delete_level(db, level_id=level_id)
  if db_level is None:
    raise HTTPException(status_code=404, detail="Level not found")
  return db_level


# ==================== SERIE ROUTES ====================

serie_router = APIRouter(tags=["Series"], dependencies=[Depends(require_admin_or_superadmin)])
@serie_router.post(
    "/series/",
    response_model=schemas.SerieResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_serie(serie: schemas.SerieCreate, db: Session = Depends(get_db)):
  return crud.create_serie(db=db, serie=serie)


@serie_router.get("/series/", response_model=List[schemas.SerieResponse])
def read_series(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return crud.get_series(db, skip=skip, limit=limit)


@serie_router.get("/series/{serie_id}", response_model=schemas.SerieResponse)
def read_serie(serie_id: int, db: Session = Depends(get_db)):
  db_serie = crud.get_serie(db, serie_id=serie_id)
  if db_serie is None:
    raise HTTPException(status_code=404, detail="Serie not found")
  return db_serie


@serie_router.put("/series/{serie_id}", response_model=schemas.SerieResponse)
def update_serie(
    serie_id: int, serie: schemas.SerieCreate, db: Session = Depends(get_db)
):
  db_serie = crud.update_serie(db, serie_id=serie_id, serie=serie)
  if db_serie is None:
    raise HTTPException(status_code=404, detail="Serie not found")
  return db_serie


@serie_router.delete("/series/{serie_id}", response_model=schemas.SerieResponse)
def delete_serie(serie_id: int, db: Session = Depends(get_db)):
  db_serie = crud.delete_serie(db, serie_id=serie_id)
  if db_serie is None:
    raise HTTPException(status_code=404, detail="Serie not found")
  return db_serie


# ==================== SCHOOL CLASS ROUTES ====================

class_router = APIRouter(tags=["School Classes"], dependencies=[Depends(require_admin_or_superadmin)])

@class_router.post(
    "/classes/",
    response_model=schemas.SchoolClassResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_school_class(
    school_class: schemas.SchoolClassCreate, db: Session = Depends(get_db)
):
  return crud.create_school_class(db=db, school_class=school_class)


@class_router.get("/classes/", response_model=List[schemas.SchoolClassResponse])
def read_school_classes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
  return crud.get_school_classes(db, skip=skip, limit=limit)


@class_router.get("/classes/{class_id}", response_model=schemas.SchoolClassResponse)
def read_school_class(class_id: int, db: Session = Depends(get_db)):
  db_class = crud.get_school_class(db, class_id=class_id)
  if db_class is None:
    raise HTTPException(status_code=404, detail="School Class not found")
  return db_class


@class_router.put("/classes/{class_id}", response_model=schemas.SchoolClassResponse)
def update_school_class(
    class_id: int,
    school_class: schemas.SchoolClassCreate,
    db: Session = Depends(get_db),
):
  db_class = crud.update_school_class(
      db, class_id=class_id, school_class=school_class
  )
  if db_class is None:
    raise HTTPException(status_code=404, detail="School Class not found")
  return db_class


@class_router.delete("/classes/{class_id}", response_model=schemas.SchoolClassResponse)
def delete_school_class(class_id: int, db: Session = Depends(get_db)):
  db_class = crud.delete_school_class(db, class_id=class_id)
  if db_class is None:
    raise HTTPException(status_code=404, detail="School Class not found")
  return db_class



# --- School Year Endpoints ---
school_year_router = APIRouter(tags=["School Years"], dependencies=[Depends(require_admin_or_superadmin)])
@school_year_router.post("/school-years/", response_model=schemas.SchoolYearResponse, status_code=status.HTTP_201_CREATED)
def create_school_year(payload: schemas.SchoolYearCreate, db: Session = Depends(get_db)):
    return crud.create_school_year(db=db, name=payload.name, startYear=payload.startYear, endYear=payload.endYear)

@school_year_router.get("/school-years/", response_model=List[schemas.SchoolYearResponse])
def read_school_years(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_school_years(db=db, skip=skip, limit=limit)

@school_year_router.get("/school-years/{school_year_id}", response_model=schemas.SchoolYearResponse)
def read_school_year(school_year_id: int, db: Session = Depends(get_db)):
    db_school_year = crud.get_school_year(db=db, school_year_id=school_year_id)
    if not db_school_year:
        raise HTTPException(status_code=404, detail="School year not found")
    return db_school_year

@school_year_router.put("/school-years/{school_year_id}", response_model=schemas.SchoolYearResponse)
def update_school_year(school_year_id: int, payload: schemas.SchoolYearUpdate, db: Session = Depends(get_db)):
    updated = crud.update_school_year(db=db, school_year_id=school_year_id, name=payload.name, startYear=payload.startYear, endYear=payload.endYear)
    if not updated:
        raise HTTPException(status_code=404, detail="School year not found")
    return updated

@school_year_router.delete("/school-years/{school_year_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school_year(school_year_id: int, db: Session = Depends(get_db)):
    success = crud.delete_school_year(db=db, school_year_id=school_year_id)
    if not success:
        raise HTTPException(status_code=404, detail="School year not found")
    return None


# --- Period Endpoints ---

period_router = APIRouter(tags=["Periods"], dependencies=[Depends(require_admin_or_superadmin)])
@period_router.post("/periods/", response_model=schemas.PeriodResponse, status_code=status.HTTP_201_CREATED)
def create_period(payload: schemas.PeriodCreate, db: Session = Depends(get_db)):
    # Verify school year exists first
    if not crud.get_school_year(db, payload.schoolYear_id):
        raise HTTPException(status_code=400, detail="Associated School Year not found")
    return crud.create_period(db=db, periodName=payload.periodName, schoolYear_id=payload.schoolYear_id)

@period_router.get("/periods/", response_model=List[schemas.PeriodResponse])
def read_periods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_periods(db=db, skip=skip, limit=limit)

@period_router.get("/periods/{period_id}", response_model=schemas.PeriodResponse)
def read_period(period_id: int, db: Session = Depends(get_db)):
    db_period = crud.get_period(db=db, period_id=period_id)
    if not db_period:
        raise HTTPException(status_code=404, detail="Period not found")
    return db_period

@period_router.get("/school-years/{school_year_id}/periods", response_model=List[schemas.PeriodResponse])
def read_periods_by_school_year(school_year_id: int, db: Session = Depends(get_db)):
    if not crud.get_school_year(db, school_year_id):
        raise HTTPException(status_code=404, detail="School year not found")
    return crud.get_periods_by_school_year(db=db, schoolYear_id=school_year_id)

@period_router.put("/periods/{period_id}", response_model=schemas.PeriodResponse)
def update_period(period_id: int, payload: schemas.PeriodUpdate, db: Session = Depends(get_db)):
    if payload.schoolYear_id and not crud.get_school_year(db, payload.schoolYear_id):
        raise HTTPException(status_code=400, detail="Associated School Year not found")
        
    updated = crud.update_period(db=db, period_id=period_id, periodName=payload.periodName, schoolYear_id=payload.schoolYear_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Period not found")
    return updated

@period_router.delete("/periods/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_period(period_id: int, db: Session = Depends(get_db)):
    success = crud.delete_period(db=db, period_id=period_id)
    if not success:
        raise HTTPException(status_code=404, detail="Period not found")
    return None
  
  
# --- Subject Endpoints ---
subject_router = APIRouter(tags=["Subjects"], dependencies=[Depends(require_admin_or_superadmin)])

@subject_router.post("/subjects/", response_model=schemas.SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db=db, subject=subject)

@subject_router.get("/subjects/", response_model=List[schemas.SubjectResponse])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_subjects(db, skip=skip, limit=limit)

@subject_router.get("/subjects/{subject_id}", response_model=schemas.SubjectResponse)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.get_subject(db, subject_id=subject_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

@subject_router.put("/subjects/{subject_id}", response_model=schemas.SubjectResponse)
def update_subject(subject_id: int, subject: schemas.SubjectUpdate, db: Session = Depends(get_db)):
    db_subject = crud.update_subject(db, subject_id=subject_id, subject_update=subject)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

@subject_router.delete("/subjects/{subject_id}", response_model=schemas.SubjectResponse)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.delete_subject(db, subject_id=subject_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject



# --- Relationship (Association Class) GET and PUT Routes ---

subject_class_assoc_router = APIRouter(tags=["Class-Subject Associations"], dependencies=[Depends(require_admin_or_superadmin)])
@subject_class_assoc_router.post("/class-subjects/", response_model=schemas.ClassSubjectAssociationResponse, status_code=status.HTTP_201_CREATED)
def link_subject_to_class(assoc: schemas.ClassSubjectAssociationCreate, db: Session = Depends(get_db)):
    db_class = crud.get_school_class(db, assoc.school_class_id)
    db_subject = crud.get_subject(db, assoc.subject_id)
    if not db_class or not db_subject:
        raise HTTPException(status_code=404, detail="School Class or Subject not found")
    return crud.create_class_subject_assoc(db=db, assoc=assoc)

@subject_class_assoc_router.get("/classes/{class_id}/subjects/{subject_id}/periods/{period_id}", response_model=schemas.ClassSubjectAssociationResponse)
def get_class_subject_relationship(class_id: int, subject_id: int, period_id: int, db: Session = Depends(get_db)):
    db_assoc = crud.get_class_subject_assoc(db, class_id=class_id, subject_id=subject_id, period_id=period_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Relationship between Class and Subject not found")
    return db_assoc

@subject_class_assoc_router.get("/classes/{class_id}/subjects/{period_id}", response_model=List[schemas.ClassSubjectAssociationResponse])
def get_a_class_subjects(class_id : int, period_id: int, db: Session = Depends(get_db)):
    school_class = crud.get_school_class(db, class_id=class_id)
    if not school_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La classe est introuvable."
        )
        
    period = crud.get_period(db, period_id)
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La période est introuvable."
        )
        
    
    return crud.get_a_class_subjects(db, class_id, period_id)

@subject_class_assoc_router.put("/classes/{class_id}/subjects/{subject_id}/periods/{period_id}", response_model=schemas.ClassSubjectAssociationResponse)
def update_class_subject_relationship(class_id: int, subject_id: int, period_id: int, assoc_update: schemas.ClassSubjectAssociationUpdate, db: Session = Depends(get_db)):
    db_assoc = crud.update_class_subject_assoc(db, class_id=class_id, subject_id=subject_id, period_id=period_id, assoc_update=assoc_update)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Relationship between Class and Subject not found")
    return db_assoc

@subject_class_assoc_router.delete("/classes/{class_id}/subjects/{subject_id}/periods/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_subject_relationship(class_id: int, subject_id: int, period_id: int, db: Session = Depends(get_db)):
    db_assoc = crud.delete_class_subject_assoc(db, class_id=class_id, subject_id=subject_id, period_id=period_id)
    if not db_assoc:
        raise HTTPException(status_code=404, detail="Relationship between Class and Subject not found")
    return db_assoc


teacher_router = APIRouter(tags=["Teachers"], dependencies=[Depends(require_admin_or_superadmin)])

@teacher_router.post("/teachers/", response_model=schemas.TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db=db, teacher=teacher)

@teacher_router.get("/teachers/", response_model=List[schemas.TeacherResponse])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teachers(db, skip=skip, limit=limit)

@teacher_router.get("/teachers/{teacher_id}", response_model=schemas.TeacherResponse)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.get_teacher(db, teacher_id=teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@teacher_router.put("/teachers/{teacher_id}", response_model=schemas.TeacherResponse)
def update_teacher(teacher_id: int, teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = crud.update_teacher(db, teacher_id=teacher_id, teacher=teacher)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@teacher_router.delete("/teachers/{teacher_id}", response_model=schemas.TeacherResponse)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.delete_teacher(db, teacher_id=teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher

@teacher_router.post("/teachers/{teacher_id}/subjects/{subject_id}", response_model=schemas.TeacherResponse)
def add_subject_to_teacher(teacher_id: int, subject_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.assign_subject_to_teacher(db, teacher_id=teacher_id, subject_id=subject_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher or Subject not found")
    return db_teacher

@teacher_router.delete("/teachers/{teacher_id}/subjects/{subject_id}", response_model=schemas.TeacherResponse)
def remove_subject_from_teacher(teacher_id: int, subject_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.remove_subject_from_teacher(db, teacher_id=teacher_id, subject_id=subject_id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher or Subject not found")
    return db_teacher  



teacher_class_subject_period_router = APIRouter(tags=["Teacher-Class-Subject-Period Associations"], dependencies=[Depends(require_admin_or_superadmin)])
@teacher_class_subject_period_router.post("/teacher-class-subject-period/", response_model=schemas.TeacherClassSubjectPeriodResponse, status_code=status.HTTP_201_CREATED)
def create_teacher_class_subject_period(assoc: schemas.TeacherClassSubjectPeriodCreate, db: Session = Depends(get_db)):
    db_teacher = crud.get_teacher(db, assoc.teacher_id)
    db_class = crud.get_school_class(db, assoc.school_class_id)
    db_subject = crud.get_subject(db, assoc.subject_id)
    db_period = crud.get_period(db, assoc.period_id)
    
    if not all([db_teacher, db_class, db_subject, db_period]):
        raise HTTPException(status_code=404, detail="Teacher, Class, Subject or Period not found")
    
    return crud.create_teacher_class_subject_period(db=db, assoc=assoc)

@teacher_class_subject_period_router.get("/teacher-class-subject-period/", response_model=List[schemas.TeacherClassSubjectPeriodResponse])
def get_all_teacher_class_subject_period(teacher_id: Optional[int] | None = None, school_class_id: Optional[int] | None=None, subject_id: Optional[int] | None=None, period_id: Optional[int] | None=None, db: Session=Depends(get_db)):
    return crud.get_teacher_class_subject_periods(db,  teacher_id, school_class_id, subject_id, period_id)


@teacher_class_subject_period_router.delete("/teacher-class-subject-period/teacher/{teacher_id}/school-class/{school_class_id}/subject/{subject_id}/period/{period_id}", response_model=schemas.TeacherClassSubjectPeriodResponse)
def delete_teacher_class_subject_period(teacher_id: int, school_class_id: int, subject_id: int, period_id: int, db: Session = Depends(get_db)):
    return crud.delete_teacher_class_subject_period(db=db, teacher_id=teacher_id, school_class_id=school_class_id, subject_id=subject_id, period_id=period_id)



admin_router = APIRouter(tags=["Admins"], dependencies=[Depends(require_admin_or_superadmin)])
@admin_router.post("/admins/", response_model=schemas.AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud.create_admin(db=db, admin=admin)

@admin_router.get("/admins/", response_model=List[schemas.AdminResponse])
def read_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_admins(db, skip=skip, limit=limit)

@admin_router.get("/admins/{admin_id}", response_model=schemas.AdminResponse)
def read_admin(admin_id: int, db: Session = Depends(get_db)):   
    db_admin = crud.get_admin(db, admin_id=admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@admin_router.put("/admins/{admin_id}", response_model=schemas.AdminResponse)
def update_admin(admin_id: int, admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    db_admin = crud.update_admin(db, admin_id=admin_id, admin=admin)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@admin_router.delete("/admins/{admin_id}", response_model=schemas.AdminResponse)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.delete_admin(db, admin_id=admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

superAdmin_router = APIRouter(tags=["Super Admins"], dependencies=[Depends(require_admin_or_superadmin)])
@superAdmin_router.get("/super-admins/", response_model=List[schemas.SuperAdminResponse])
def read_superAdmins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_superAdmins(db, skip=skip, limit=limit)

@superAdmin_router.post("/super-admins/", response_model=schemas.SuperAdminResponse, status_code=status.HTTP_201_CREATED)
def create_superAdmin(superAdmin: schemas.SuperAdminCreate, db: Session = Depends(get_db)):
    return crud.create_superAdmin(db=db, superAdmin=superAdmin)

@superAdmin_router.get("/super-admins/{superAdmin_id}", response_model=schemas.SuperAdminResponse)
def read_superAdmin(superAdmin_id: int, db: Session = Depends(get_db)):
    db_superAdmin = crud.get_superAdmin(db, superAdmin_id=superAdmin_id)
    if not db_superAdmin:
        raise HTTPException(status_code=404, detail="Super Admin not found")
    return db_superAdmin

@superAdmin_router.put("/super-admins/{superAdmin_id}", response_model=schemas.SuperAdminResponse)
def update_superAdmin(superAdmin_id: int, superAdmin: schemas.SuperAdminCreate, db: Session = Depends(get_db)):
    db_superAdmin = crud.update_superAdmin(db, superAdmin_id=superAdmin_id, superAdmin=superAdmin)
    if not db_superAdmin:
        raise HTTPException(status_code=404, detail="Super Admin not found")
    return db_superAdmin

@superAdmin_router.delete("/super-admins/{superAdmin_id}", response_model=schemas.SuperAdminResponse)
def delete_superAdmin(superAdmin_id: int, db: Session = Depends(get_db)):
    db_superAdmin = crud.delete_superAdmin(db, superAdmin_id=superAdmin_id)
    if not db_superAdmin:
        raise HTTPException(status_code=404, detail="Super Admin not found")
    return db_superAdmin





main_router = APIRouter()
main_router.include_router(student_router)
main_router.include_router(parent_router)
main_router.include_router(student_parent_router)
main_router.include_router(serie_router)
main_router.include_router(level_router)
main_router.include_router(class_router)
main_router.include_router(school_year_router) 
main_router.include_router(period_router)
main_router.include_router(subject_router)
main_router.include_router(subject_class_assoc_router)
main_router.include_router(teacher_router)
main_router.include_router(teacher_class_subject_period_router)
main_router.include_router(admin_router)
main_router.include_router(superAdmin_router)
 # For School Year routes