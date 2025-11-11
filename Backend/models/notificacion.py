from db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Notificacion(Base):
    __tablename__ = "notificaciones"
    id_notificacion = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    mensaje = Column(String(500), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    leida = Column(Boolean, default=False)

    # Relaciones
    usuario_id = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    usuario = relationship("Usuario", back_populates="notificaciones")

    noticia_id = Column(Integer, ForeignKey("noticias.id_noticia"), nullable=True)
    noticia = relationship("Noticia", back_populates="notificaciones")
