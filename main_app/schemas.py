from datetime import date, datetime

from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from auth_app.schemas import UserCreate, UserOut

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
        
        
        
        
        
        
# Résolution des références circulaires Pydantic si nécessaire
ParentStudentLinkResponse.model_rebuild()