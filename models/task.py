from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from core.database import Base


class TaskCategory(str, enum.Enum):
    vacuna = "vacuna"
    veterinario = "veterinario"
    medicamento = "medicamento"
    baño = "baño"
    alimentacion = "alimentacion"
    ejercicio = "ejercicio"
    otro = "otro"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(TaskCategory), default=TaskCategory.otro)
    is_done = Column(Boolean, default=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    pet = relationship("Pet", back_populates="tasks")
