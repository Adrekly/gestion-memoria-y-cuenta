import { useState, useEffect } from 'react';
import { Plus, XCircle, Loader, X, Check, CheckCircle, AlertTriangle, Search } from 'lucide-react';
import ConfirmModal from '../components/ConfirmModal';
import { desincorporacionesAPI, bienesAPI } from '../services/api';
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

  // Autocompletado
  const [bienQuery, setBienQuery] = useState('');
  const [sugerencias, setSugerencias] = useState([]);
  const [bienSeleccionado, setBienSeleccionado] = useState(null);

  // Confirm Modal
  const [confirmState, setConfirmState] = useState(null);
  const [confirmForm, setConfirmForm] = useState({ nombre: '', observaciones: '' });

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

  const buscarBienes = async (q) => {
    setBienQuery(q);
    if (q.length < 2) { setSugerencias([]); return; }
    try {
      const res = await bienesAPI.buscarCodigo(q);
      setSugerencias(res);
    } catch { setSugerencias([]); }
  };

  const seleccionarBien = (bien) => {
    setForm({ ...form, codigo_inventario: bien.codigo_inventario });
    setBienQuery(bien.codigo_inventario);
    setBienSeleccionado(bien);
    setSugerencias([]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSending(true);
    try {
      await desincorporacionesAPI.crear(form);
      toast.success('Solicitud de desincorporacion creada');
      setShowForm(false);
      setForm({ codigo_inventario: '', motivo: 'OBSOLESCENCIA', justificacion_tecnica: '', solicitado_por: '' });
      setBienQuery('');
      setBienSeleccionado(null);
      cargar();
    } catch (e) { toast.error(e.message); }
    finally { setSending(false); }
  };

  const aprobar = async (id) => {
    setConfirmForm({ nombre: '', observaciones: '' });
    setConfirmState({ type: 'aprobar', id });
  };

  const rechazar = async (id) => {
    setConfirmForm({ nombre: '', observaciones: '' });
    setConfirmState({ type: 'rechazar', id });
  };

  const ejecutarConfirmacion = async () => {
    if (!confirmForm.nombre) { toast.error('El nombre es requerido'); return; }
    
    try {
      if (confirmState.type === 'aprobar') {
        await desincorporacionesAPI.cambiarEstado(confirmState.id, { estado: 'APROBADA', aprobado_por: confirmForm.nombre });
        toast.success('Desincorporacion aprobada');
      } else {
        await desincorporacionesAPI.cambiarEstado(confirmState.id, { estado: 'RECHAZADA', aprobado_por: confirmForm.nombre, observaciones: confirmForm.observaciones });
        toast.success('Solicitud rechazada');
      }
      setConfirmState(null);
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
                <div className="form-group form-group--full" style={{ position: 'relative' }}>
                  <label><Search size={14} style={{ marginRight: 4 }} />Buscar Bien *</label>
                  <input
                    type="text"
                    required
                    value={bienQuery}
                    onChange={e => buscarBienes(e.target.value)}
                    placeholder="Escriba código o descripción del bien..."
                    autoComplete="off"
                  />
                  {sugerencias.length > 0 && (
                    <ul className="autocomplete-list">
                      {sugerencias.map(s => (
                        <li key={s.codigo_inventario} className="autocomplete-item" onClick={() => seleccionarBien(s)}>
                          <strong>{s.codigo_inventario}</strong>
                          <span>{s.descripcion}</span>
                          <small>{s.sede}</small>
                        </li>
                      ))}
                    </ul>
                  )}
                  {bienSeleccionado && (
                    <p className="form-hint" style={{ color: '#2ECC71' }}>
                      <CheckCircle size={12} /> {bienSeleccionado.descripcion} — {bienSeleccionado.sede}
                    </p>
                  )}
                </div>
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

      {confirmState && (
        <ConfirmModal
          title={confirmState.type === 'aprobar' ? 'Aprobar Solicitud' : 'Rechazar Solicitud'}
          message={confirmState.type === 'aprobar' ? '¿Está seguro de que desea aprobar esta desincorporación?' : 'Por favor, indique el motivo del rechazo.'}
          onConfirm={ejecutarConfirmacion}
          onCancel={() => setConfirmState(null)}
          confirmText={confirmState.type === 'aprobar' ? 'Aprobar' : 'Rechazar'}
          isDanger={confirmState.type === 'rechazar'}
        >
          <div className="form-group" style={{ marginBottom: '12px' }}>
            <label>Nombre del responsable *</label>
            <input 
              type="text" 
              required 
              value={confirmForm.nombre} 
              onChange={e => setConfirmForm({...confirmForm, nombre: e.target.value})} 
            />
          </div>
          {confirmState.type === 'rechazar' && (
            <div className="form-group">
              <label>Observaciones</label>
              <textarea 
                rows="2" 
                value={confirmForm.observaciones} 
                onChange={e => setConfirmForm({...confirmForm, observaciones: e.target.value})} 
              />
            </div>
          )}
        </ConfirmModal>
      )}
    </div>
  );
}
