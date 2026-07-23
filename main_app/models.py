"""
models.py
=========
SQLAlchemy 2.0 ORM models for the School Management System FastAPI app.

Generated from the corrected UML class diagram (6 modules):
    1. Users              -> User, Teacher, Parent, Admin, SuperAdmin, ParentType
    2. Academic structure  -> Serie, Promotion, SchoolClass, Subject,
                               SubjectClass, TeacherClassSubject, StudentClassPeriod,
                               Periode, Exam, ExamType

Notes on naming vs. the diagram:
- The diagram's "Class" is implemented as `SchoolClass` (table "classes") since
  `class` is a reserved word in Python.

Usage:
    from sqlalchemy import create_engine
    from models import Base

    engine = create_engine("postgresql+psycopg2://user:pass@localhost/school")
    Base.metadata.create_all(engine)
"""

from datetime import date
import enum
from typing import Optional

from sqlalchemy import Column, Date, Enum, Integer, String, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.database import Base

from auth_app.models import User  # noqa: F401  -- imports every model so metadata is complete

class ParentTypeEnum(str, enum.Enum):
    FATHER = "Père"
    MOTHER = "Mère"
    TUTOR = "Tuteur"
    OTHER = "Autre"

# Table d'association sous forme de modèle pour supporter l'attribut 'parent_type'
class StudentParentAssociation(Base):
    __tablename__ = "student_parent"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), primary_key=True)
    parent_type: Mapped[ParentTypeEnum] = mapped_column(Enum(ParentTypeEnum), default=ParentTypeEnum.FATHER)

    # Relations pour naviguer facilement depuis la table intermédiaire
    student = relationship("Student", back_populates="parent_associations")
    parent = relationship("Parent", back_populates="student_associations")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    studentMatricule: Mapped[str] = mapped_column(String(30), unique=True)
    first_name : Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
    last_name : Mapped[str] = mapped_column(String(100), nullable=False)
    email : Mapped[Optional[str]] = mapped_column(String, unique=True, index=True, nullable=True)
    birth_date : Mapped[date] = mapped_column(Date)

    # Relation Many-to-Many via la table d'association
    parent_associations = relationship(
        "StudentParentAssociation", 
        back_populates="student", 
        cascade="all, delete-orphan"
    )


class Parent(User):
    __tablename__ = "parents"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    profession: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Relation Many-to-Many via la table d'association
    student_associations = relationship(
        "StudentParentAssociation", 
        back_populates="parent", 
        cascade="all, delete-orphan"
    )



class Level(Base):
  __tablename__ = "levels"

  id = Column(Integer, primary_key=True, index=True)
  levelName = Column(String, unique=True, index=True, nullable=False)

  # Relationship to SchoolClass
  classes = relationship("SchoolClass", back_populates="level")


class Serie(Base):
  __tablename__ = "series"

  id = Column(Integer, primary_key=True, index=True)
  serieName = Column(String, unique=True, index=True, nullable=False)

  # Relationship to SchoolClass
  classes = relationship("SchoolClass", back_populates="serie")


class SchoolClass(Base):
  __tablename__ = "school_classes"

  id = Column(Integer, primary_key=True, index=True)
  className = Column(String, nullable=False)
  level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
  serie_id = Column(Integer, ForeignKey("series.id"), nullable=True)

  # Relationships
  level = relationship("Level", back_populates="classes")
  serie = relationship("Serie", back_populates="classes")