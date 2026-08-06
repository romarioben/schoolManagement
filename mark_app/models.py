import enum
from datetime import date, datetime, timezone
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

from main_app.models import SchoolClass, Period, Subject, Student  # Importing models from main_app

from config.database import Base  # SQLAlchemy declarative base from database.py


class MarkType(Base):
    __tablename__ = "mark_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    mark_type_name: Mapped[str] = mapped_column(String(50), unique=True)  # e.g. "Devoir", "Examen final"
    coefficient: Mapped[int] = mapped_column(Float, default=1)  # weight in the final grade
    is_by_subject: Mapped[bool] = mapped_column(Boolean, default=False)  # whether this mark type is associated with an exam
    is_by_period: Mapped[bool] = mapped_column(Boolean, default=False)  # whether this mark type is associated with a period
    is_annual: Mapped[bool] = mapped_column(Boolean, default=False)  # whether this mark type is associated with an annual evaluation
    is_inserted : Mapped[bool] = mapped_column(Boolean, default=False)  # whether this mark type is inserted by the teacher or system
    used_to_calculate : Mapped[Optional[int]] = mapped_column(ForeignKey("mark_types.id"), nullable=True)  # self-referential foreign key for hierarchical mark types, this marktype can be used to calculate another mark type (e.g., "Moyenne" can be used to calculate "Moyenne générale")
    

    
class Mark(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(Float)
    comment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    mark_type_id: Mapped[int] = mapped_column(ForeignKey("mark_types.id"))
    subject_id: Mapped[Optional[int]] = mapped_column(ForeignKey("subjects.id"), nullable=True)
    period_id: Mapped[Optional[int]] = mapped_column(ForeignKey("periods.id"), nullable=True)
    school_class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("school_classes.id"))
    
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
        )
    
    updated_at: Mapped[Optional[datetime]] = mapped_column(
            DateTime(timezone=True), default=None, nullable=True, onupdate=lambda: datetime.now(timezone.utc)
        )

    #student: Mapped["Student"] = relationship(back_populates="marks")
    #mark_type: Mapped["MarkType"] = relationship(back_populates="marks")
    #subject: Mapped[Optional["Subject"]] = relationship(back_populates="marks")
    #period: Mapped[Optional["Period"]] = relationship(back_populates="marks")
    #school_class: Mapped[Optional["SchoolClass"]] = relationship(back_populates="marks")






# class ReportCard(Base):
#     __tablename__ = "report_cards"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     gpa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
#     generated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

#     student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
#     period_id: Mapped[int] = mapped_column(ForeignKey("periodes.id"))

#     student: Mapped["Student"] = relationship(back_populates="report_cards")
#     period: Mapped["Periode"] = relationship(back_populates="report_cards")
#     marks: Mapped[List["Mark"]] = relationship(back_populates="report_card")

#     def generate_pdf(self) -> bytes:
#         """Business logic placeholder: render this report card to PDF."""
#         raise NotImplementedError
