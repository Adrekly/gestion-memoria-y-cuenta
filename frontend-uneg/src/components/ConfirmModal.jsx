import { X, AlertTriangle } from 'lucide-react';

export default function ConfirmModal({ title, message, onConfirm, onCancel, confirmText = 'Confirmar', cancelText = 'Cancelar', isDanger = false, children }) {
  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal modal--sm" onClick={e => e.stopPropagation()} style={{ maxWidth: '400px' }}>
        <div className="modal__header" style={{ borderBottom: 'none', paddingBottom: '0' }}>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', color: isDanger ? 'var(--danger)' : 'var(--text)' }}>
            {isDanger && <AlertTriangle size={20} />} {title}
          </h3>
          <button className="btn-icon" onClick={onCancel}><X size={20} /></button>
        </div>
        <div className="modal__body">
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '16px' }}>{message}</p>
          {children}
        </div>
        <div className="modal__actions" style={{ borderTop: 'none', paddingTop: '0' }}>
          <button className="btn btn--ghost" onClick={onCancel}>{cancelText}</button>
          <button className={`btn ${isDanger ? 'btn--danger' : 'btn--primary'}`} onClick={onConfirm}>{confirmText}</button>
        </div>
      </div>
    </div>
  );
}
