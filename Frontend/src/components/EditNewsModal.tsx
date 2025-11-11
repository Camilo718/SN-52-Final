import React, { useState, useEffect } from 'react';
import type { Noticia } from '../services/noticias';
import { getNoticiasCreadas } from '../services/noticias';

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
    const defaults = ['Deportes', 'Arte', 'Cultura', 'Bienestar', 'Tecnología', 'Educación', 'Política'];
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
            <h2>Editar noticia</h2>
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
                  <option value="__custom__">Otra / Personalizada</option>
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

      <style>{`
        .edit-modal-backdrop{position:fixed;inset:0;background:linear-gradient(180deg, rgba(0,0,0,0.45), rgba(0,0,0,0.6));display:flex;align-items:center;justify-content:center;z-index:3000;padding:20px}
        .edit-modal.card{background:linear-gradient(180deg,#ffffff,#fbfbff);padding:0;border-radius:12px;max-width:1000px;width:100%;box-shadow:0 10px 40px rgba(2,6,23,0.4);overflow:hidden;font-family:Inter,Segoe UI,Roboto,Arial}
        .edit-header{display:flex;justify-content:space-between;align-items:center;padding:20px 24px;border-bottom:1px solid #eef2ff}
        .edit-header h2{margin:0;font-size:20px}
        .edit-header .subtitle{margin:4px 0 0;color:#5b6470;font-size:13px}
        .close-btn{background:transparent;border:none;font-size:20px;cursor:pointer}
        .edit-body{display:flex;gap:20px;padding:20px}
        .preview-col{width:320px;display:flex;flex-direction:column;gap:12px}
        .image-preview{background:#f6f8ff;border-radius:8px;height:220px;display:flex;align-items:center;justify-content:center;overflow:hidden}
        .image-preview img{width:100%;height:100%;object-fit:cover}
        .image-placeholder{color:#9aa3b2}
        .image-controls{display:flex;flex-direction:column;gap:8px}
        .file-btn{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;background:#eef6ff;border-radius:8px;color:#0b63ff;cursor:pointer}
        .file-btn input{display:none}
        .hint{color:#8892a8;font-size:12px}
        .main-col{flex:1}
        .field{display:block;margin-bottom:12px}
        .label-title{display:block;font-weight:600;margin-bottom:6px}
        .edit-form input,.edit-form textarea,.edit-form select{width:100%;padding:10px;border:1px solid #e6e9f2;border-radius:8px;background:#fff}
        .category-row{display:flex;gap:8px}
        .custom-input{width:40%}
        .edit-actions{display:flex;gap:10px;justify-content:flex-end;margin-top:10px}
        .btn-primary{background:#0b63ff;color:#fff;padding:10px 16px;border-radius:10px;border:none;cursor:pointer}
        .btn-secondary{background:#f1f5ff;color:#0b63ff;padding:8px 12px;border-radius:8px;border:none;cursor:pointer}
        .btn-secondary.small{padding:6px 10px;font-size:13px}
        @media (max-width:880px){.edit-body{flex-direction:column}.preview-col{width:100%}.custom-input{width:100%}}
      `}</style>
    </div>
  );
};

export default EditNewsModal;
