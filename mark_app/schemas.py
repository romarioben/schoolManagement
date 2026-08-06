from typing import Optional, List
from pydantic import BaseModel, Field


# --- MarkType Schemas ---

class MarkTypeBase(BaseModel):
    pass


class MarkTypeCreate(MarkTypeBase):
    mark_type_name: str = Field(..., max_length=50, example="Devoir")
    coefficient: float = Field(default=1.0, example=2.0)
    is_by_subject: bool = False
    is_by_period: bool = False
    is_annual: bool = False
    is_inserted: bool = False
    used_to_calculate: Optional[int] = None


class MarkTypeUpdate(BaseModel):
    mark_type_name: Optional[str] = Field(None, max_length=50)
    coefficient: Optional[float] = None
    is_by_subject: Optional[bool] = None
    is_by_period: Optional[bool] = None
    is_annual: Optional[bool] = None
    is_inserted: Optional[bool] = None
    used_to_calculate: Optional[int] = None


class MarkTypeResponse(MarkTypeBase):
    id: int
    mark_type_name: str = Field(..., max_length=50, example="Devoir")
    coefficient: float = Field(default=1.0, example=2.0)
    is_by_subject: bool = False
    is_by_period: bool = False
    is_annual: bool = False
    is_inserted: bool = False
    used_to_calculate: Optional[int] = None

    class Config:
        from_attributes = True


# --- Mark Schemas ---

class MarkBase(BaseModel):
    value: float = Field(..., example=15.5)
    comment: Optional[str] = Field(None, max_length=255)
    student_id: int
    mark_type_id: int
    subject_id: Optional[int] = None
    period_id: Optional[int] = None
    school_class_id: Optional[int] = None


class MarkCreate(MarkBase):
    pass


class MarkUpdate(BaseModel):
    value: Optional[float] = None
    comment: Optional[str] = Field(None, max_length=255)
    student_id: Optional[int] = None
    mark_type_id: Optional[int] = None
    subject_id: Optional[int] = None
    period_id: Optional[int] = None
    school_class_id: Optional[int] = None


class MarkResponse(MarkBase):
    id: int

    class Config:
        from_attributes = True