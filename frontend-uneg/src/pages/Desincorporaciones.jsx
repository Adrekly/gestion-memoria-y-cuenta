import { useState, useEffect } from 'react';
import { Plus, XCircle, Loader, X, Check, CheckCircle, AlertTriangle } from 'lucide-react';
import { desincorporacionesAPI } from '../services/api';
import toast from 'react-hot-toast';

const MOTIVOS = ['OBSOLESCENCIA', 'INSERVIBILIDAD', 'HURTO', 'ROBO', 'SINIESTRO', 'DONACION', 'OTRO'];
const ESTADO_COLORS = { SOLICITADA: '#F39C12', EN_REVISION: '#3498DB', APROBADA: '#2ECC71', RECHAZADA: '#E74C3C', EJECUTADA: '#95A5A6' };

export default function Desincorporaciones() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [sending, setSending] = useState(false);
  const [form, setForm] = useState({ codigo_inventario: '', motivo: 'OBSOLESCENCIA', justificacion_tecnica: '', solicitado_por: '' });

  const cargar = async () => {
    setLoading(true);
    try {
      const data = await desincorporacionesAPI.listar({ por_pagina: 50 });
      setItems(data.desincorporaciones);
      setTotal(data.total);
    } catch (e) { toast.error(e.message); }
    finally { setLoading(false); }
  };

  useEffect(() => { cargar(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSending(true);
    try {
      await desincorporacionesAPI.crear(form);
      toast.success('Solicitud de desincorporacion creada');
      setShowForm(false);
      setForm({ codigo_inventario: '', motivo: 'OBSOLESCENCIA', justificacion_tecnica: '', solicitado_por: '' });
      cargar();
    } catch (e) { toast.error(e.message); }
    finally { setSending(false); }
  };

  const aprobar = async (id) => {
    const nombre = prompt('Nombre del aprobador:');
    if (!nombre) return;
    try {
      await desincorporacionesAPI.cambiarEstado(id, { estado: 'APROBADA', aprobado_por: nombre });
      toast.success('Desincorporacion aprobada');
      cargar();
    } catch (e) { toast.error(e.message); }
  };

  const rechazar = async (id) => {
    const nombre = prompt('Nombre del supervisor:');
    if (!nombre) return;
    const obs = prompt('Observaciones:');
    try {
      await desincorporacionesAPI.cambiarEstado(id, { estado: 'RECHAZADA', aprobado_por: nombre, observaciones: obs });
      toast.success('Solicitud rechazada');
      cargar();
    } catch (e) { toast.error(e.message); }
  };

  return (
    <div className="page">
      <div className="page__header">
        <div>
          <h2 className="page__title">Desincorporaciones</h2>
          <p className="page__subtitle">{total} solicitudes</p>
        </div>
        <button className="btn btn--primary" onClick={() => setShowForm(true)}><Plus size={18} /> Nueva Solicitud</button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead><tr><th>Fecha</th><th>Bien</th><th>Motivo</th><th>Estado</th><th>Solicitado por</th><th>IA</th><th>Acciones</th></tr></thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="7" className="table-loading"><Loader className="spin" size={20} /></td></tr>
            ) : items.length === 0 ? (
              <tr><td colSpan="7" className="table-empty"><XCircle size={32} /><br />No hay solicitudes</td></tr>
            ) : items.map((d, i) => (
              <tr key={d.id || d._id || i}>
                <td>{d.fecha_solicitud ? new Date(d.fecha_solicitud).toLocaleDateString('es-VE') : ''}</td>
                <td className="td-code">{d.bien_codigo_inventario || d.bien_id}</td>
                <td>{d.motivo}</td>
                <td><span className="badge" style={{ background: ESTADO_COLORS[d.estado_proceso] }}>{d.estado_proceso?.replace(/_/g, ' ')}</span></td>
                <td>{d.solicitado_por}</td>
                <td>{d.validacion_ia?.cumple_criterios ? <CheckCircle size={16} color="#2ECC71" /> : <AlertTriangle size={16} color="#F39C12" />}</td>
                <td>
                  {d.estado_proceso === 'EN_REVISION' && (
                    <>
                      <button className="btn btn--sm btn--success" onClick={() => aprobar(d.id || d._id)}><Check size={14} /></button>
                      <button className="btn btn--sm btn--danger" onClick={() => rechazar(d.id || d._id)}><X size={14} /></button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal modal--sm" onClick={e => e.stopPropagation()}>
            <div className="modal__header"><h3>Solicitar Desincorporacion</h3><button className="btn-icon" onClick={() => setShowForm(false)}><X size={20} /></button></div>
            <form onSubmit={handleSubmit} className="modal__body">
              <div className="form-grid">
                <div className="form-group form-group--full"><label>Código Inventario *</label><input type="text" required value={form.codigo_inventario} onChange={e => setForm({...form, codigo_inventario: e.target.value})} placeholder="UNEG-ATL-03-00004" /></div>
                <div className="form-group"><label>Motivo *</label><select required value={form.motivo} onChange={e => setForm({...form, motivo: e.target.value})}>{MOTIVOS.map(m => <option key={m} value={m}>{m}</option>)}</select></div>
                <div className="form-group"><label>Solicitado por *</label><input type="text" required value={form.solicitado_por} onChange={e => setForm({...form, solicitado_por: e.target.value})} /></div>
                <div className="form-group form-group--full"><label>Justificacion tecnica * (min. 20 caracteres)</label><textarea required minLength={20} rows={4} value={form.justificacion_tecnica} onChange={e => setForm({...form, justificacion_tecnica: e.target.value})} placeholder="Describa detalladamente el motivo de la baja..." /></div>
              </div>
              <div className="modal__actions">
                <button type="button" className="btn btn--ghost" onClick={() => setShowForm(false)}>Cancelar</button>
                <button type="submit" className="btn btn--primary" disabled={sending}>{sending ? <Loader className="spin" size={16} /> : <Check size={16} />} Solicitar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
