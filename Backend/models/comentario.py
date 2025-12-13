from db import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Comentario(Base):
    __tablename__ = "comentario"
    id_comentario = Column(Integer, primary_key=True)
    fecha_creacion = Column(Date)
    contenido = Column(String(200))

    usuario = relationship("Usuario", back_populates="comentario")
    # Clave foránea
    noticia_id = Column(Integer,
                        ForeignKey("noticias.id_noticia"))
    # clave foránea
    usuario_id = Column(Integer,
                        ForeignKey("usuarios.id_usuario"))

    noticia = relationship("Noticia", back_populates="comentarios")
