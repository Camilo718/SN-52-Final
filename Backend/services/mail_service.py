 # Backend/services/mail_service.py
from mailjet_rest import Client
import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")

if not MAILJET_API_KEY or not MAILJET_SECRET_KEY:
    raise ValueError("⚠️ Faltan las claves de Mailjet en el archivo .env")

# Inicializar cliente de Mailjet
mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')


# 📩 --- Correo de bienvenida ---
def enviar_correo_bienvenida(destinatario: str, nombre: str):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "dilanramirezv2007@gmail.com",  # Tu remitente Mailjet verificado
                    "Name": "SN-52 Noticias"
                },
                "To": [{"Email": destinatario, "Name": nombre}],
                "Subject": "🎉 ¡Bienvenido a SN-52!",
                "HTMLPart": f"""
                <html>
                  <body style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 10px; padding: 20px;">
                      <h2 style="color: #004aad;">👋 ¡Hola {nombre}!</h2>
                      <p>Tu registro en <strong>SN-52</strong> fue exitoso.</p>
                      <p>Gracias por unirte a nuestro periódico digital. A partir de ahora podrás estar al día con las noticias y novedades del SENA.</p>
                      <p>Con aprecio,<br><strong>El equipo de SN-52</strong></p>
                    </div>
                  </body>
                </html>
                """
            }
        ]
    }
    try:
        response = mailjet.send.create(data=data)
        print("✅ Correo de bienvenida enviado:", response.status_code)
        return response.json()
    except Exception as e:
        print("⚠️ Error al enviar correo de bienvenida:", e)
        return None


# 🔐 --- Correo de recuperación de contraseña ---
def enviar_correo_recuperacion(destinatario: str, nombre: str, token: str):
    reset_link = f"http://localhost:5173/reset-password?token={token}"  # 🔗 Puedes cambiarlo por la URL real de tu frontend

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "dilanramirezv2007@gmail.com",
                    "Name": "SN-52 Noticias"
                },
                "To": [{"Email": destinatario, "Name": nombre}],
                "Subject": "🔑 Recuperación de contraseña - SN-52",
                "HTMLPart": f"""
                <html>
                  <body style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 10px; padding: 20px;">
                      <h2 style="color: #004aad;">🔒 Recuperar tu contraseña</h2>
                      <p>Hola {nombre},</p>
                      <p>Recibimos una solicitud para restablecer tu contraseña en <strong>SN-52</strong>.</p>
                      <p>Haz clic en el siguiente enlace para continuar con el proceso:</p>
                      <a href="{reset_link}"
                         style="background-color:#004aad; color:white; padding:10px 20px; border-radius:5px; text-decoration:none; font-weight:bold;">
                         Restablecer contraseña
                      </a>
                      <p style="margin-top:20px;">Este enlace expirará en 1 hora.</p>
                      <p>Si no solicitaste este cambio, puedes ignorar este mensaje.</p>
                      <br>
                      <p>Con aprecio,<br><strong>El equipo de SN-52</strong></p>
                    </div>
                  </body>
                </html>
                """
            }
        ]
    }
    try:
        response = mailjet.send.create(data=data)
        print("✅ Correo de recuperación enviado:", response.status_code)
        return response.json()
    except Exception as e:
        print("⚠️ Error al enviar correo de recuperación:", e)
        return None


# 📝 --- Correo de notificación de borrador ---
def enviar_correo_notificacion_borrador(destinatarios: list, titulo_noticia: str, escritor_nombre: str):
    """
    Envía notificación por email a editores cuando un escritor guarda un borrador.
    destinatarios: lista de dicts con 'email' y 'nombre'
    """
    if not destinatarios:
        print("⚠️ No hay destinatarios para notificación de borrador")
        return None

    to_list = [{"Email": d["email"], "Name": d["nombre"]} for d in destinatarios]

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "dilanramirezv2007@gmail.com",
                    "Name": "SN-52 Noticias"
                },
                "To": to_list,
                "Subject": f"📝 Nuevo borrador disponible para revisión - {titulo_noticia}",
                "HTMLPart": f"""
                <html>
                  <body style="font-family: Arial, sans-serif; color: #333; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 10px; padding: 20px;">
                      <h2 style="color: #004aad;">📝 Nuevo borrador para revisión</h2>
                      <p>Hola,</p>
                      <p>El escritor <strong>{escritor_nombre}</strong> ha guardado un nuevo borrador titulado:</p>
                      <p style="font-size: 18px; font-weight: bold; color: #004aad;">"{titulo_noticia}"</p>
                      <p>Por favor, revisa el borrador en el panel de administración y proporciona retroalimentación al escritor.</p>
                      <a href="http://localhost:5173/dashboard"
                         style="background-color:#004aad; color:white; padding:10px 20px; border-radius:5px; text-decoration:none; font-weight:bold;">
                         Ir al panel de administración
                      </a>
                      <br><br>
                      <p>Con aprecio,<br><strong>El equipo de SN-52</strong></p>
                    </div>
                  </body>
                </html>
                """
            }
        ]
    }
    try:
        response = mailjet.send.create(data=data)
        print(f"✅ Correo de notificación de borrador enviado a {len(destinatarios)} editores:", response.status_code)
        return response.json()
    except Exception as e:
        print("⚠️ Error al enviar correo de notificación de borrador:", e)
        return None
