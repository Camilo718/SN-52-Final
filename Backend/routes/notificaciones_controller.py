from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from models.notificacion import Notificacion
from dtos.notificacion_dto import NotificacionCreate, NotificacionUpdate, NotificacionResponse
from security.auth import get_current_user
from models.usuario import Usuario

router = APIRouter(
    prefix="/api/notificaciones",
    tags=["notificaciones"]
)

@router.post("/", response_model=NotificacionResponse)
async def crear_notificacion(
    notificacion: NotificacionCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Solo administradores pueden crear notificaciones manualmente
    if current_user.rol_id != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear notificaciones")

    nueva_notificacion = Notificacion(
        **notificacion.dict(),
        fecha_creacion=None  # Se usa default
    )

    db.add(nueva_notificacion)
    db.commit()
    db.refresh(nueva_notificacion)
    return nueva_notificacion

@router.get("/", response_model=List[NotificacionResponse])
async def obtener_notificaciones_usuario(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notificaciones = db.query(Notificacion)\
        .filter(Notificacion.usuario_id == current_user.id_usuario)\
        .order_by(Notificacion.fecha_creacion.desc())\
        .all()
    return notificaciones

@router.put("/{notificacion_id}", response_model=NotificacionResponse)
async def actualizar_notificacion(
    notificacion_id: int,
    notificacion_update: NotificacionUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_notificacion = db.query(Notificacion).filter(Notificacion.id_notificacion == notificacion_id).first()
    if not db_notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    # Solo el propietario puede actualizar su notificación
    if db_notificacion.usuario_id != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar esta notificación")

    update_data = notificacion_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_notificacion, key, value)

    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

@router.delete("/{notificacion_id}")
async def eliminar_notificacion(
    notificacion_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_notificacion = db.query(Notificacion).filter(Notificacion.id_notificacion == notificacion_id).first()
    if not db_notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    # Solo el propietario o admin puede eliminar
    if current_user.rol_id != 1 and db_notificacion.usuario_id != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta notificación")

    db.delete(db_notificacion)
    db.commit()
    return {"message": "Notificación eliminada correctamente"}
