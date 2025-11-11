import React, { useState, useContext, useEffect } from 'react';
import { Heart, MessageCircle, Share2, Bookmark, Edit2 } from 'lucide-react';
import type { Noticia } from '../services/noticias';
import { toggleLikeNoticia, toggleSaveNoticia, shareNoticia, actualizarNoticia } from '../services/noticias';
import CommentsModal from './CommentsModal';
import EditNewsModal from './EditNewsModal';
import { UserContext } from '../context/UserContext';

interface ArticleCardProps {
  noticia: Noticia;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ noticia }) => {
  const [isLiked, setIsLiked] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [showCommentsModal, setShowCommentsModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [noticiaState, setNoticiaState] = useState<Noticia>(noticia);
  const { user } = useContext(UserContext);

  const handleLike = () => {
    setIsLiked(!isLiked);
    toggleLikeNoticia(noticia.id);
  };

  const handleSave = () => {
    setIsSaved(!isSaved);
    toggleSaveNoticia(noticia.id);
  };

  const handleShare = () => {
    shareNoticia(noticia);
  };

  const handleOpenComments = () => {
    setShowCommentsModal(true);
  };

  const handleCloseComments = () => {
    setShowCommentsModal(false);
  };

  const handleOpenEdit = () => {
    setShowEditModal(true);
  };

  const handleCloseEdit = () => {
    setShowEditModal(false);
  };

  const handleSaveEdit = async (updated: Noticia) => {
    try {
      const saved = await actualizarNoticia(updated);
      setNoticiaState(saved);
      setShowEditModal(false);
    } catch (error) {
      console.error('Error guardando noticia:', error);
      alert('No se pudo guardar la noticia.');
    }
  };

  return (
    <>
      <article className="news-card">
        {noticiaState.imagen && (
          <div className="image-wrapper">
            <img
              src={noticiaState.imagen}
              alt={noticiaState.titulo}
              className="news-image"
            />
            {user && user.rol === 'editor' && (
              <button className="edit-overlay" onClick={handleOpenEdit} title="Editar noticia">
                <Edit2 size={18} />
              </button>
            )}
          </div>
        )}
        <div className="news-content">
          <span className="news-category">{noticiaState.categoria.toUpperCase()}</span>
          <h3 className="news-title">{noticiaState.titulo}</h3>
          <p className="news-summary">
            {noticiaState.contenidoTexto.length > 150
              ? noticiaState.contenidoTexto.substring(0, 150) + '...'
              : noticiaState.contenidoTexto}
          </p>
          <div className="news-meta">
            <span className="news-author">{noticiaState.autor}</span>
            <span className="news-date">{new Date(noticiaState.fecha).toLocaleDateString('es-ES')}</span>
          </div>
          {noticiaState.etiquetas.length > 0 && (
            <div className="news-tags">
              {noticiaState.etiquetas.map((tag, index) => (
                <span key={index} className="news-tag">#{tag}</span>
              ))}
            </div>
          )}
          <div className="news-actions">
            <button
              onClick={handleLike}
              className={`action-btn like-btn ${isLiked ? 'active' : ''}`}
            >
              <Heart size={16} />
              <span>{noticiaState.likes + (isLiked ? 1 : 0)}</span>
            </button>
            <button
              onClick={handleOpenComments}
              className="action-btn comment-btn"
            >
              <MessageCircle size={16} />
              <span>{noticiaState.comentarios}</span>
            </button>
            <button
              onClick={handleShare}
              className="action-btn share-btn"
            >
              <Share2 size={16} />
              <span>{noticiaState.compartidos}</span>
            </button>
            <button
              onClick={handleSave}
              className={`action-btn save-btn ${isSaved ? 'active' : ''}`}
            >
              <Bookmark size={16} />
            </button>
            {user && user.rol === 'editor' && (
              <button onClick={handleOpenEdit} title="Editar noticia" className="action-btn edit-btn">
                <Edit2 size={16} />
              </button>
            )}
          </div>
        </div>
      </article>

      <CommentsModal
        isOpen={showCommentsModal}
        onClose={handleCloseComments}
        noticiaId={noticia.id}
        noticiaTitle={noticia.titulo}
      />
      <EditNewsModal
        isOpen={showEditModal}
        onClose={handleCloseEdit}
        noticia={noticiaState}
        onSave={handleSaveEdit}
      />
      <style>{`
        .news-card .image-wrapper{position:relative}
        .news-card .edit-overlay{position:absolute;top:8px;right:8px;background:rgba(11,99,255,0.9);border:none;color:#fff;padding:6px;border-radius:8px;display:flex;align-items:center;justify-content:center;cursor:pointer}
        .news-card .edit-overlay:hover{transform:scale(1.03)}
      `}</style>
    </>
  );
};

export default ArticleCard;
