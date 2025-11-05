# usuarios_controller.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Body
from sqlalchemy.orm import Session
from db import get_db
from models.usuario import Usuario
from models.schemas import UsuarioOut, TokenResponse, RecuperarPasswordRequest
from security.passwords import encriptar_contrasena, verificar_contrasena
from security.jwt import crear_token
import uuid

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# ----------------- Registro -----------------
@router.post("/register", response_model=UsuarioOut)
async def register(
    nombre_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    correo_usuario: str = Form(...),
    contrasena_usuario: str = Form(...),
    rol_id: int = Form(1),
    foto_usuario: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    if db.query(Usuario).filter(Usuario.correo_usuario == correo_usuario).first():
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    hashed_password = encriptar_contrasena(contrasena_usuario)

    nuevo_usuario = Usuario(
        nombre_usuario=nombre_usuario,
        apellido_usuario=apellido_usuario,
        correo_usuario=correo_usuario,
        contrasena_usuario=hashed_password,
        rol_id=rol_id,
        foto_usuario=foto_usuario.filename if foto_usuario else None
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    if foto_usuario:
        with open(f"uploads/{foto_usuario.filename}", "wb") as f:
            f.write(await foto_usuario.read())

    return UsuarioOut(
        id=nuevo_usuario.id_usuario,
        nombre=nuevo_usuario.nombre_usuario,
        apellidos=nuevo_usuario.apellido_usuario,
        correo=nuevo_usuario.correo_usuario,
        foto=nuevo_usuario.foto_usuario,
        rol_id=nuevo_usuario.rol_id
    )

# ----------------- Login -----------------
@router.post("/login", response_model=TokenResponse)
def login(
    correo_usuario: str = Form(...),
    contrasena_usuario: str = Form(...),
    db: Session = Depends(get_db)
):
    from datetime import datetime, timedelta

    usuario = db.query(Usuario).filter(Usuario.correo_usuario == correo_usuario).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Correo no registrado")

    # Verificar si la cuenta está bloqueada
    if usuario.bloqueado_hasta and usuario.bloqueado_hasta > datetime.utcnow():
        tiempo_restante = usuario.bloqueado_hasta - datetime.utcnow()
        minutos = int(tiempo_restante.total_seconds() / 60)
        raise HTTPException(status_code=429, detail=f"Cuenta bloqueada. Intenta de nuevo en {minutos} minutos.")

    if not verificar_contrasena(contrasena_usuario, usuario.contrasena_usuario):
        # Incrementar intentos fallidos
        usuario.intentos_fallidos += 1

        if usuario.intentos_fallidos >= 3:
            # Bloquear por 15 minutos
            usuario.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=15)
            usuario.intentos_fallidos = 0  # Resetear intentos
            db.commit()
            raise HTTPException(status_code=429, detail="Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos.")
        else:
            db.commit()
            raise HTTPException(status_code=400, detail=f"Contraseña incorrecta. Intentos restantes: {3 - usuario.intentos_fallidos}")

    # Login exitoso: resetear intentos fallidos
    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    db.commit()

    token = crear_token({"sub": usuario.id_usuario, "rol_id": usuario.rol_id})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        usuario=UsuarioOut(
            id=usuario.id_usuario,
            nombre=usuario.nombre_usuario,
            apellidos=usuario.apellido_usuario,
            correo=usuario.correo_usuario,
            foto=usuario.foto_usuario,
            rol_id=usuario.rol_id
        )
    )

# ----------------- Actualizar perfil -----------------
@router.put("/update/{user_id}", response_model=UsuarioOut)
async def update_user(
    user_id: int,
    nombre_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    correo_usuario: str = Form(...),
    foto_usuario: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre_usuario = nombre_usuario
    usuario.apellido_usuario = apellido_usuario
    usuario.correo_usuario = correo_usuario

    if foto_usuario:
        filename = foto_usuario.filename
        with open(f"uploads/{filename}", "wb") as f:
            f.write(await foto_usuario.read())
        usuario.foto_usuario = filename

    db.commit()
    db.refresh(usuario)

    return UsuarioOut(
        id=usuario.id_usuario,
        nombre=usuario.nombre_usuario,
        apellidos=usuario.apellido_usuario,
        correo=usuario.correo_usuario,
        foto=usuario.foto_usuario,
        rol_id=usuario.rol_id
    )

# ----------------- Recuperar contraseña (demo) -----------------
@router.post("/recuperar-password")
async def recuperar_password(req: RecuperarPasswordRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo_usuario == req.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    token = str(uuid.uuid4())
    usuario.reset_token = token
    db.commit()

    # Devolvemos el token directamente para la demo
    return {
        "msg": "Token generado. Úsalo para restablecer tu contraseña",
        "token": token
    }

# ----------------- Restablecer contraseña -----------------
@router.post("/reset-password")
def reset_password(
    token: str = Body(...),
    nueva_password: str = Body(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.reset_token == token).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Token inválido")

    usuario.contrasena_usuario = encriptar_contrasena(nueva_password)
    usuario.reset_token = None
    db.commit()

    return {"msg": "Contraseña actualizada correctamente"}
