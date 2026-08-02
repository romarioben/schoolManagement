from datetime import date, datetime

from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from auth_app.schemas import UserCreate, UserOut
from main_app.models import DomaineEnum

# --- Schémas Parent ---
class ParentBase(UserOut):
    pass

class ParentCreate(UserCreate):
    profession: Optional[str] = None  # Profession du parent
    role: str = "parent"  # Le rôle est fixé à "parent" pour tous les parents

class ParentResponse(ParentBase):
    id: int
    email: str
    username: str
    surname: Optional[str] = None
    firstname: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    profession: Optional[str] = None
    
    #student_associations: List[ParentStudentLinkResponse] = []

    class Config:
        from_attributes = True


# --- Schémas Association (Lien) ---
class StudentParentLinkCreate(BaseModel):
    parent_type: str  # ex: "Père", "Mère", "Tuteur"

class StudentParentLinkResponse(BaseModel):
    parent: ParentResponse
    parent_type: str

    class Config:
        from_attributes = True

class ParentStudentLinkResponse(BaseModel):
    student: "StudentResponse0"
    parent_type: str

    class Config:
        from_attributes = True


# --- Schémas Student ---
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    studentMatricule: str
    birth_date: Optional[date]  # Format: YYYY-MM-DD

class StudentCreate(StudentBase):
    pass

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    studentMatricule: str
    birth_date: Optional[date]  # Format: YYYY-MM-DD
    # On renvoie la liste des associations contenant le parent et son type
    parent_associations: List[StudentParentLinkResponse] = []

    class Config:
        from_attributes = True

class StudentResponse0(BaseModel):
    id: int
    first_name: str
    last_name: str
    studentMatricule: str
    birth_date: Optional[date]  # Format: YYYY-MM-DD
    # On renvoie la liste des associations contenant le parent et son type
    #parent_associations: List[StudentParentLinkResponse] = []

    class Config:
        from_attributes = True


# --- Schéma Parent avec ses étudiants ---
class ParentWithStudentsResponse(ParentResponse):
    student_associations: List[ParentStudentLinkResponse] = []

    class Config:
        from_attributes = True


# ==================== LEVEL SCHEMAS ====================


class LevelBase(BaseModel):
  pass


class LevelCreate(LevelBase):
    levelName: str
    pass


class LevelResponse(LevelBase):
  id: int
  levelName: str

  model_config = ConfigDict(from_attributes=True)


# ==================== SERIE SCHEMAS ====================


class SerieBase(BaseModel):
  pass


class SerieCreate(SerieBase):
    serieName: str
  


class SerieResponse(SerieBase):
  id: int
  serieName: str

  model_config = ConfigDict(from_attributes=True)


# ==================== SCHOOL CLASS SCHEMAS ====================


class SchoolClassBase(BaseModel):
  className: str
  level_id: int
  serie_id: Optional[int] = None


class SchoolClassCreate(SchoolClassBase):
  pass


class SchoolClassResponse(SchoolClassBase):
  id: int
  level: Optional[LevelResponse] = None
  serie: Optional[SerieResponse] = None

  model_config = ConfigDict(from_attributes=True)


# --- school year Schemas ---


class SchoolYearCreate(BaseModel):
    name: str
    startYear: int
    endYear: int

class SchoolYearUpdate(BaseModel):
    name: Optional[str] = None
    startYear: Optional[int] = None
    endYear: Optional[int] = None

class SchoolYearResponse(BaseModel):
    id: int
    name: str
    startYear: int
    endYear: int

    class Config:
        from_attributes = True


# --- Period Schemas ---

class PeriodCreate(BaseModel):
    periodName: str
    schoolYear_id: int

class PeriodUpdate(BaseModel):
    periodName: Optional[str] = None
    schoolYear_id: Optional[int] = None

class PeriodResponse(BaseModel):
    id: int
    periodName: str
    schoolYear: SchoolYearResponse  # Nested SchoolYearResponse

    class Config:
        from_attributes = True
        
        

class SubjectBase(BaseModel):
    subjectName: str
    domaine: DomaineEnum

class SubjectCreate(BaseModel):
    subjectName: str
    domaine: DomaineEnum
    
class SubjectUpdate(BaseModel):
    subjectName: Optional[str] = None
    domaine: Optional[DomaineEnum] = None

class SubjectResponse(BaseModel):
    id: int
    subjectName: str
    domaine: DomaineEnum

    model_config = ConfigDict(from_attributes=True)



# --- Association Schemas (Many-to-Many Class) ---
class ClassSubjectAssociationBase(BaseModel):
    hours_per_week: Optional[int] = None
    coefficient: Optional[int] = None
    
class ClassSubjectAssociationCreate(ClassSubjectAssociationBase):
    school_class_id: int
    subject_id: int
    period_id: int
    coefficient: int

class ClassSubjectAssociationUpdate(BaseModel):
    hours_per_week: Optional[int] = None
    coefficient: Optional[int] = None
   
class ClassSubjectAssociationResponse(ClassSubjectAssociationBase):
    school_class_id: int
    subject_id: int
    period_id: int
    coefficient: int
    school_class: SchoolClassResponse
    subject: SubjectResponse
    period: PeriodResponse

    model_config = ConfigDict(from_attributes=True)
        



class TeacherCreate(UserCreate):
    teacherMatricule: Optional[str] = None  # Matricule de l'enseignant
    role: str = "teacher"  # Le rôle est fixé à "teacher" pour tous les enseignants

class TeacherResponse(UserOut):
    id: int
    teacherMatricule: Optional[str] = None
    subjects: List[SubjectResponse] = []

    class Config:
        from_attributes = True
        
class TeacherClassSubjectPeriodCreate(BaseModel):
    teacher_id: int
    school_class_id: int
    subject_id: int
    period_id: int
        
class TeacherClassSubjectPeriodResponse(BaseModel):
    teacher_id: int
    school_class_id: int
    subject_id: int
    period_id: int
    teacher: TeacherResponse
    school_class: SchoolClassResponse
    subject: SubjectResponse
    period: PeriodResponse

    model_config = ConfigDict(from_attributes=True)


class AdminCreate(TeacherCreate):
    poste: Optional[str] = None  # Poste de l'administrateur, peut être nul
    role: str = "admin"  # Le rôle est fixé à "admin" pour tous les administrateurs

class SuperAdminCreate(AdminCreate):
    poste: Optional[str] = None  # Poste du super administrateur, peut être nul
    role: str = "superadmin"  # Le rôle est fixé à "superadmin" pour tous les super administrateurs


class AdminResponse(TeacherResponse):
    id: int
    poste: Optional[str] = None

    class Config:
        from_attributes = True

class SuperAdminResponse(AdminResponse):
    id: int
    poste: Optional[str] = None

    class Config:
        from_attributes = True

  
# Résolution des références circulaires Pydantic si nécessaire
ParentStudentLinkResponse.model_rebuild()
ParentWithStudentsResponse.model_rebuild()
StudentResponse.model_rebuild()
PeriodResponse.model_rebuild()
SchoolClassResponse.model_rebuild()
SubjectResponse.model_rebuild()
ClassSubjectAssociationResponse.model_rebuild()
StudentResponse0.model_rebuild()