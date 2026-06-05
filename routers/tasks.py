from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.pet import Pet
from models.task import Task, TaskCategory
from schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/pets/{pet_id}/tasks", tags=["📋 Pendientes"])


def get_pet_or_404(pet_id: int, owner_id: int, db: Session) -> Pet:
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == owner_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    return pet


def get_task_or_404(task_id: int, pet_id: int, db: Session) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.pet_id == pet_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear pendiente",
    description="Agrega un nuevo pendiente/recordatorio para la mascota."
)
def create_task(
    pet_id: int,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_pet_or_404(pet_id, current_user.id, db)
    task = Task(**data.model_dump(), pet_id=pet_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Listar pendientes",
    description="Lista todos los pendientes de la mascota. Puedes filtrar por categoría o estado."
)
def list_tasks(
    pet_id: int,
    category: Optional[TaskCategory] = Query(None, description="Filtrar por categoría"),
    is_done: Optional[bool] = Query(None, description="Filtrar por completado (true/false)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_pet_or_404(pet_id, current_user.id, db)
    query = db.query(Task).filter(Task.pet_id == pet_id)
    if category:
        query = query.filter(Task.category == category)
    if is_done is not None:
        query = query.filter(Task.is_done == is_done)
    return query.order_by(Task.due_date.asc().nullslast(), Task.created_at.desc()).all()


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Ver pendiente",
    description="Devuelve el detalle de un pendiente específico."
)
def get_task(
    pet_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_pet_or_404(pet_id, current_user.id, db)
    return get_task_or_404(task_id, pet_id, db)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Actualizar pendiente",
    description="Modifica campos de un pendiente. Usa `is_done: true` para marcarlo como completado."
)
def update_task(
    pet_id: int,
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_pet_or_404(pet_id, current_user.id, db)
    task = get_task_or_404(task_id, pet_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.patch(
    "/{task_id}/toggle",
    response_model=TaskResponse,
    summary="Marcar/desmarcar como completado",
    description="Alterna el estado `is_done` del pendiente."
)
def toggle_task(
    pet_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_pet_or_404(pet_id, current_user.id, db)
    task = get_task_or_404(task_id, pet_id, db)
    task.is_done = not task.is_done
    db.commit()
    db.refresh(task)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar pendiente",
    description="Elimina permanentemente un pendiente."
)
def delete_task(
    pet_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_pet_or_404(pet_id, current_user.id, db)
    task = get_task_or_404(task_id, pet_id, db)
    db.delete(task)
    db.commit()
