from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Fido")
    species: str = Field(..., example="perro")
    breed: Optional[str] = Field(None, example="Labrador")
    age_years: Optional[float] = Field(None, ge=0, example=3.5)
    weight_kg: Optional[float] = Field(None, ge=0, example=12.5)
    photo_url: Optional[str] = Field(None, example="https://ejemplo.com/foto.jpg")
    notes: Optional[str] = Field(None, example="Le gusta correr en el parque")


class PetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    species: Optional[str] = None
    breed: Optional[str] = None
    age_years: Optional[float] = Field(None, ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    photo_url: Optional[str] = None
    notes: Optional[str] = None


class PetResponse(BaseModel):
    id: int
    name: str
    species: str
    breed: Optional[str]
    age_years: Optional[float]
    weight_kg: Optional[float]
    photo_url: Optional[str]
    notes: Optional[str]
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
