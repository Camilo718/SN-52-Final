import { useSearchParams } from "react-router-dom";
import { useState } from "react";
import "./ResetPassword.css";

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirm) {
      setMessage("⚠️ Las contraseñas no coinciden");
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/usuarios/reset-password/${token}`,
        {
          method: "POST",
          body: new URLSearchParams({
            nueva_contrasena: password,
            confirmar_contrasena: confirm,
          }),
        }
      );

      if (response.ok) {
        setMessage("✅ Contraseña restablecida correctamente");
        setPassword("");
        setConfirm("");
      } else {
        const data = await response.json();
        setMessage(data.detail || "Error al cambiar la contraseña");
      }
    } catch (error) {
      setMessage("❌ Error de conexión con el servidor");
    }
  };

  return (
    <div className="reset-container">
      <div className="reset-card">
        <h2>Restablecer Contraseña</h2>
        <p>Ingresa tu nueva contraseña para continuar</p>
        <form onSubmit={handleSubmit} className="reset-form">
          <input
            type="password"
            placeholder="Nueva contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Confirmar contraseña"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
          />
          <button type="submit">Actualizar contraseña</button>
        </form>
        {message && <p className="reset-message">{message}</p>}
      </div>
    </div>
  );
};

export default ResetPassword;
