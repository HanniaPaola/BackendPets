from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.pet import Pet
from schemas.pet import PetCreate, PetUpdate, PetResponse

router = APIRouter(prefix="/pets", tags=["🐾 Mascotas"])


def get_pet_or_404(pet_id: int, owner_id: int, db: Session) -> Pet:
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == owner_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    return pet


@router.post(
    "/",
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar mascota",
    description="Agrega una nueva mascota al perfil del usuario."
)
def create_pet(
    data: PetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pet = Pet(**data.model_dump(), owner_id=current_user.id)
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get(
    "/",
    response_model=List[PetResponse],
    summary="Listar mis mascotas",
    description="Devuelve todas las mascotas del usuario. Puedes filtrar por especie."
)
def list_pets(
    species: Optional[str] = Query(None, description="Filtrar por especie (perro, gato, etc.)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Pet).filter(Pet.owner_id == current_user.id)
    if species:
        query = query.filter(Pet.species.ilike(f"%{species}%"))
    return query.order_by(Pet.name).all()


@router.get(
    "/{pet_id}",
    response_model=PetResponse,
    summary="Ver detalle de mascota",
    description="Devuelve los datos completos de una mascota por su ID."
)
def get_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_pet_or_404(pet_id, current_user.id, db)


@router.put(
    "/{pet_id}",
    response_model=PetResponse,
    summary="Actualizar mascota",
    description="Actualiza uno o más campos de una mascota. Solo los campos enviados se modifican."
)
def update_pet(
    pet_id: int,
    data: PetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pet = get_pet_or_404(pet_id, current_user.id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pet, field, value)
    db.commit()
    db.refresh(pet)
    return pet


@router.delete(
    "/{pet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar mascota",
    description="Elimina una mascota y todos sus pendientes asociados."
)
def delete_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pet = get_pet_or_404(pet_id, current_user.id, db)
    db.delete(pet)
    db.commit()
