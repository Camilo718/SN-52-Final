import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export interface Notification {
  id_notificacion: number;
  titulo: string;
  mensaje: string;
  fecha_creacion: string;
  leida: boolean;
  usuario_id: number;
  noticia_id?: number;
}

export const notificationsService = {
  // Obtener notificaciones del usuario actual
  async getNotifications(): Promise<Notification[]> {
    const token = localStorage.getItem('token');
    const response = await axios.get(`${API_BASE_URL}/api/notificaciones/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  },

  // Marcar notificación como leída
  async markAsRead(notificationId: number): Promise<Notification> {
    const token = localStorage.getItem('token');
    const response = await axios.put(
      `${API_BASE_URL}/api/notificaciones/${notificationId}`,
      { leida: true },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  },

  // Eliminar notificación
  async deleteNotification(notificationId: number): Promise<void> {
    const token = localStorage.getItem('token');
    await axios.delete(`${API_BASE_URL}/api/notificaciones/${notificationId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};
