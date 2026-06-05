from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from models.task import TaskCategory


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150, example="Vacuna antirrábica")
    description: Optional[str] = Field(None, example="Llevar a la clínica El Roble")
    category: TaskCategory = Field(default=TaskCategory.otro, example="vacuna")
    due_date: Optional[datetime] = Field(None, example="2025-06-15T10:00:00")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None
    category: Optional[TaskCategory] = None
    is_done: Optional[bool] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: TaskCategory
    is_done: bool
    due_date: Optional[datetime]
    pet_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
