from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionBase(BaseModel):
    titulo: str
    mensaje: str
    leida: Optional[bool] = False
    noticia_id: Optional[int] = None

class NotificacionCreate(NotificacionBase):
    usuario_id: int

class NotificacionUpdate(BaseModel):
    leida: Optional[bool] = None

class NotificacionResponse(NotificacionBase):
    id_notificacion: int
    fecha_creacion: datetime
    usuario_id: int

    class Config:
        from_attributes = True
