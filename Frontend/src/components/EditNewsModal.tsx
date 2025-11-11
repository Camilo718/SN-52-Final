import React, { useState, useEffect } from 'react';
import type { Noticia } from '../services/noticias';
import { getNoticiasCreadas } from '../services/noticias';
import './EditNewsModal.css';

interface EditNewsModalProps {
  isOpen: boolean;
  onClose: () => void;
  noticia: Noticia;
  onSave: (noticia: Noticia) => void;
}

const EditNewsModal: React.FC<EditNewsModalProps> = ({ isOpen, onClose, noticia, onSave }) => {
  const [titulo, setTitulo] = useState(noticia.titulo);
  const [contenidoTexto, setContenidoTexto] = useState(noticia.contenidoTexto);
  const [categoria, setCategoria] = useState(noticia.categoria);
  const [imagen, setImagen] = useState(noticia.imagen || '');
  const [etiquetas, setEtiquetas] = useState(noticia.etiquetas.join(', '));
  const [availableCategories, setAvailableCategories] = useState<string[]>([]);
  const [customCategory, setCustomCategory] = useState('');

  useEffect(() => {
    setTitulo(noticia.titulo);
    setContenidoTexto(noticia.contenidoTexto);
    const cap = (noticia.categoria || '').toString();
    setCategoria(cap ? (cap.charAt(0).toUpperCase() + cap.slice(1)) : '');
    setImagen(noticia.imagen || '');
    setEtiquetas(noticia.etiquetas.join(', '));
  }, [noticia]);

  useEffect(() => {
    // Build a categories list from existing created noticias + defaults
    const defaults = ['Deportes', 'Arte', 'Cultura', 'Bienestar', 'Tecnología'];
    try {
      const creadas = getNoticiasCreadas();
      const fromCreated = Array.from(new Set(creadas.map(n => n.categoria))).filter(Boolean);
      const merged = Array.from(new Set([...defaults.map(d => d.toLowerCase()), ...fromCreated.map(c => (c || '').toLowerCase())]));
      setAvailableCategories(merged.map(c => c.charAt(0).toUpperCase() + c.slice(1)));
    } catch (err) {
      console.error(err);
      setAvailableCategories(defaults);
    }
  }, [noticia]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const finalCategory = categoria === '__custom__' ? customCategory.trim() : categoria;
    const updated: Noticia = {
      ...noticia,
      titulo: titulo.trim(),
      contenidoTexto: contenidoTexto,
      contenido: contenidoTexto,
      categoria: (finalCategory || '').trim(),
      imagen: imagen || undefined,
      etiquetas: etiquetas.split(',').map(t => t.trim()).filter(Boolean),
    };

    onSave(updated);
  };

  const handleFileChange = (file?: File) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string | null;
      if (result) setImagen(result);
    };
    reader.readAsDataURL(file);
  };

  const onFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files && e.target.files[0];
    if (f) handleFileChange(f);
  };

  const removeImage = () => setImagen('');

  return (
    <div className="edit-modal-backdrop">
      <div className="edit-modal card">
        <header className="edit-header">
          <div>
            <h2>
              <span 
                className="pencil-icon" 
                style={{ 
                  color: '#21b0a6', 
                  marginRight: '10px', 
                  transform: 'rotate(-45deg)',
                  display: 'inline-block'
                }}
              >
                &#9998;
              </span>
              Editar noticia
            </h2>
            <p className="subtitle">Modifica título, categoría, resumen y la imagen. Los cambios se guardarán localmente.</p>
          </div>
          <button className="close-btn" onClick={onClose} aria-label="Cerrar">✕</button>
        </header>

        <div className="edit-body">
          <aside className="preview-col">
            <div className="image-preview">
              {imagen ? (
                <img src={imagen} alt="Preview" />
              ) : (
                <div className="image-placeholder">Sin imagen</div>
              )}
            </div>
            <div className="image-controls">
              <label className="file-btn">
                Subir imagen
                <input type="file" accept="image/*" onChange={onFileInput} />
              </label>
              <button type="button" className="btn-secondary small" onClick={removeImage}>Eliminar</button>
              <small className="hint">Se recomienda imágenes JPG/PNG; se convertirá a data URL.</small>
            </div>
          </aside>

          <form onSubmit={handleSubmit} className="edit-form main-col">
            <label className="field">
              <span className="label-title">Título</span>
              <input value={titulo} onChange={e => setTitulo(e.target.value)} />
            </label>

            <label className="field">
              <span className="label-title">Resumen / Contenido</span>
              <textarea value={contenidoTexto} onChange={e => setContenidoTexto(e.target.value)} rows={6} />
            </label>

            <label className="field">
              <span className="label-title">Categoría</span>
              <div className="category-row">
                <select value={categoria === '' ? '__custom__' : (availableCategories.includes(categoria) ? categoria : (categoria || '__custom__'))} onChange={e => setCategoria(e.target.value)}>
                  {availableCategories.map(c => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
                {categoria === '__custom__' && (
                  <input className="custom-input" placeholder="Escribe la categoría" value={customCategory} onChange={e => setCustomCategory(e.target.value)} />
                )}
              </div>
            </label>

            <label className="field">
              <span className="label-title">Etiquetas (separadas por coma)</span>
              <input value={etiquetas} onChange={e => setEtiquetas(e.target.value)} />
            </label>

            <div className="edit-actions">
              <button type="button" className="btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn-primary">Guardar cambios</button>
            </div>
          </form>
        </div>

      </div>


    </div>
  );
};

export default EditNewsModal;
