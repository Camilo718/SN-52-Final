import React, { useState, useEffect } from 'react';
import { notificationsService, Notification } from '../services/notifications';
import './Notifications.css';

interface NotificationsProps {
  isOpen: boolean;
  onClose: () => void;
}

const Notifications: React.FC<NotificationsProps> = ({ isOpen, onClose }) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadNotifications();
    }
  }, [isOpen]);

  const loadNotifications = async () => {
    setLoading(true);
    try {
      const data = await notificationsService.getNotifications();
      setNotifications(data);
    } catch (error) {
      console.error('Error loading notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (notificationId: number) => {
    try {
      await notificationsService.markAsRead(notificationId);
      setNotifications(prev =>
        prev.map(notif =>
          notif.id_notificacion === notificationId
            ? { ...notif, leida: true }
            : notif
        )
      );
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const handleDelete = async (notificationId: number) => {
    try {
      await notificationsService.deleteNotification(notificationId);
      setNotifications(prev =>
        prev.filter(notif => notif.id_notificacion !== notificationId)
      );
    } catch (error) {
      console.error('Error deleting notification:', error);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (!isOpen) return null;

  return (
    <div className="notifications-overlay" onClick={onClose}>
      <div className="notifications-modal" onClick={e => e.stopPropagation()}>
        <div className="notifications-header">
          <h2>Notificaciones</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        <div className="notifications-content">
          {loading ? (
            <div className="loading">Cargando notificaciones...</div>
          ) : notifications.length === 0 ? (
            <div className="no-notifications">
              No tienes notificaciones pendientes
            </div>
          ) : (
            <div className="notifications-list">
              {notifications.map(notification => (
                <div
                  key={notification.id_notificacion}
                  className={`notification-item ${!notification.leida ? 'unread' : ''}`}
                >
                  <div className="notification-content">
                    <h4>{notification.titulo}</h4>
                    <p>{notification.mensaje}</p>
                    <span className="notification-date">
                      {formatDate(notification.fecha_creacion)}
                    </span>
                  </div>

                  <div className="notification-actions">
                    {!notification.leida && (
                      <button
                        className="mark-read-button"
                        onClick={() => handleMarkAsRead(notification.id_notificacion)}
                      >
                        Marcar como leída
                      </button>
                    )}
                    <button
                      className="delete-button"
                      onClick={() => handleDelete(notification.id_notificacion)}
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Notifications;
