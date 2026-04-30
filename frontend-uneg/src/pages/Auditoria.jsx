import { useState, useEffect } from 'react';
import { Shield, Loader, ChevronLeft, ChevronRight, ArrowRight } from 'lucide-react';
import { auditoriaAPI } from '../services/api';
import toast from 'react-hot-toast';

const ACCION_LABELS = {
  CREAR: 'Bien Registrado',
  ACTUALIZAR: 'Bien Actualizado',
  CAMBIO_ESTADO: 'Cambio de Estado',
  DESINCORPORAR: 'Solicitud de Baja',
  DESINCORPORACION_APROBADA: 'Baja Aprobada',
  DESINCORPORACION_RECHAZADA: 'Baja Rechazada',
  MOVIMIENTO: 'Movimiento',
};

export default function Auditoria() {
  const [registros, setRegistros] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [pagina, setPagina] = useState(1);

  const cargar = async () => {
    setLoading(true);
    try {
      const data = await auditoriaAPI.listar({ pagina, por_pagina: 30 });
      setRegistros(data.registros);
      setTotal(data.total);
    } catch (e) { toast.error(e.message); }
    finally { setLoading(false); }
  };

  useEffect(() => { cargar(); }, [pagina]);

  const totalPaginas = Math.ceil(total / 30);

  return (
    <div className="page">
      <div className="page__header">
        <div>
          <h2 className="page__title">Registro de Auditoria</h2>
          <p className="page__subtitle">{total} acciones registradas — Trazabilidad completa del sistema</p>
        </div>
        <div className="status-badge"><span className="status-dot" /> Registrando</div>
      </div>

      <div className="table-container" style={{ padding: '0' }}>
        {loading ? (
          <div className="page-loading"><Loader className="spin" size={24} /> Cargando historial...</div>
        ) : registros.length === 0 ? (
          <div className="table-empty"><Shield size={40} /><br />No hay registros de auditoria aun</div>
        ) : (
          <div className="audit-timeline">
            {registros.map((r, i) => (
              <div key={r._id || i} className={`audit-entry audit-entry--${r.accion}`}>
                <div className="audit-entry__time">
                  {r.fecha ? new Date(r.fecha).toLocaleString('es-VE', { dateStyle: 'short', timeStyle: 'short' }) : ''}
                </div>
                <div className="audit-entry__body">
                  <div className="audit-entry__action">
                    {ACCION_LABELS[r.accion] || r.accion}
                    <span className="badge" style={{ background: 'var(--primary-light)' }}>{r.coleccion}</span>
                  </div>
                  <div className="audit-entry__detail">
                    <strong>{r.documento_id}</strong>
                    {r.usuario && r.usuario !== 'Sistema' && <> — por {r.usuario}</>}
                    {r.detalles?.descripcion && <> — {r.detalles.descripcion}</>}
                    {r.detalles?.motivo && <> — Motivo: {r.detalles.motivo}</>}
                    {r.detalles?.tipo && <> — Tipo: {r.detalles.tipo}</>}
                    {r.detalles?.bien && <> — {r.detalles.bien}</>}
                  </div>
                  {r.cambios && Object.keys(r.cambios).length > 0 && (
                    <div className="audit-entry__changes">
                      {Object.entries(r.cambios).map(([campo, vals]) => (
                        <span key={campo} className="audit-change">
                          {campo}: <span className="audit-change__old">{vals.anterior}</span>
                          <ArrowRight size={10} />
                          <span className="audit-change__new">{vals.nuevo}</span>
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {totalPaginas > 1 && (
        <div className="pagination">
          <button className="btn btn--ghost btn--sm" disabled={pagina <= 1} onClick={() => setPagina(p => p - 1)}><ChevronLeft size={16} /></button>
          <span className="pagination__info">{pagina} / {totalPaginas}</span>
          <button className="btn btn--ghost btn--sm" disabled={pagina >= totalPaginas} onClick={() => setPagina(p => p + 1)}><ChevronRight size={16} /></button>
        </div>
      )}
    </div>
  );
}
