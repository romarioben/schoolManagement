import enum
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Column,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from auth_app.models import User 

from config.database import Base  # SQLAlchemy declarative base from database.py

class ExamType(Base):
    __tablename__ = "exam_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    exam_type_name: Mapped[str] = mapped_column(String(50))  # e.g. "Devoir", "Examen final"
    percentage: Mapped[float] = mapped_column(Float)  # weight in the final grade

    exams: Mapped[List["Exam"]] = relationship(back_populates="exam_type")


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    date: Mapped[date] = mapped_column(Date)
    max_score: Mapped[float] = mapped_column(Float, default=20.0)

    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"))
    period_id: Mapped[int] = mapped_column(ForeignKey("periodes.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    exam_type_id: Mapped[int] = mapped_column(ForeignKey("exam_types.id"))

    school_class: Mapped["SchoolClass"] = relationship(back_populates="exams")
    period: Mapped["Periode"] = relationship(back_populates="exams")
    subject: Mapped["Subject"] = relationship(back_populates="exams")
    exam_type: Mapped["ExamType"] = relationship(back_populates="exams")

    marks: Mapped[List["Mark"]] = relationship(back_populates="exam", cascade="all, delete-orphan")


# =========================================================================
# 3. MARKS & EVALUATIONS
# =========================================================================


class Mark(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(Float)
    comment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"))
    report_card_id: Mapped[Optional[int]] = mapped_column(ForeignKey("report_cards.id"), nullable=True)

    student: Mapped["Student"] = relationship(back_populates="marks")
    exam: Mapped["Exam"] = relationship(back_populates="marks")
    report_card: Mapped[Optional["ReportCard"]] = relationship(back_populates="marks")


class ReportCard(Base):
    __tablename__ = "report_cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    gpa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    generated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    period_id: Mapped[int] = mapped_column(ForeignKey("periodes.id"))

    student: Mapped["Student"] = relationship(back_populates="report_cards")
    period: Mapped["Periode"] = relationship(back_populates="report_cards")
    marks: Mapped[List["Mark"]] = relationship(back_populates="report_card")

    def generate_pdf(self) -> bytes:
        """Business logic placeholder: render this report card to PDF."""
        raise NotImplementedError
