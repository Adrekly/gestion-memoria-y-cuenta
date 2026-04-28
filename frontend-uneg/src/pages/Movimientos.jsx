import { useState, useEffect } from 'react';
import { Plus, ArrowLeftRight, Loader, X, Check } from 'lucide-react';
import { movimientosAPI, sedesAPI } from '../services/api';
import toast from 'react-hot-toast';

const TIPOS = ['ENTRADA', 'SALIDA', 'TRASLADO', 'REASIGNACION'];

export default function Movimientos() {
  const [movimientos, setMovimientos] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [sedes, setSedes] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [sending, setSending] = useState(false);
  const [form, setForm] = useState({ codigo_inventario: '', tipo: 'TRASLADO', sede_destino: '', motivo: '', autorizado_por: '', documento_soporte: '' });

  const cargar = async () => {
    setLoading(true);
    try {
      const data = await movimientosAPI.listar({ por_pagina: 50 });
      setMovimientos(data.movimientos);
      setTotal(data.total);
    } catch (e) { toast.error(e.message); }
    finally { setLoading(false); }
  };

  useEffect(() => { cargar(); sedesAPI.listar().then(setSedes).catch(() => {}); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSending(true);
    try {
      await movimientosAPI.crear(form);
      toast.success('Movimiento registrado');
      setShowForm(false);
      setForm({ codigo_inventario: '', tipo: 'TRASLADO', sede_destino: '', motivo: '', autorizado_por: '', documento_soporte: '' });
      cargar();
    } catch (e) { toast.error(e.message); }
    finally { setSending(false); }
  };

  return (
    <div className="page">
      <div className="page__header">
        <div>
          <h2 className="page__title">Movimientos de Bienes</h2>
          <p className="page__subtitle">{total} movimientos registrados</p>
        </div>
        <button className="btn btn--primary" onClick={() => setShowForm(true)}><Plus size={18} /> Nuevo Movimiento</button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead><tr><th>Fecha</th><th>Tipo</th><th>Bien</th><th>Descripcion</th><th>Origen</th><th>Destino</th><th>Motivo</th><th>Autorizado</th></tr></thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="8" className="table-loading"><Loader className="spin" size={20} /> Cargando...</td></tr>
            ) : movimientos.length === 0 ? (
              <tr><td colSpan="8" className="table-empty"><ArrowLeftRight size={32} /><br />No hay movimientos registrados</td></tr>
            ) : movimientos.map((m, i) => (
              <tr key={m.id || m._id || i}>
                <td>{m.fecha ? new Date(m.fecha).toLocaleDateString('es-VE') : ''}</td>
                <td><span className="badge badge--outline">{m.tipo}</span></td>
                <td className="td-code">{m.bien_codigo_inventario || ''}</td>
                <td>{m.bien_descripcion || ''}</td>
                <td>{m.sede_origen || ''}</td>
                <td>{m.sede_destino || ''}</td>
                <td>{m.motivo}</td>
                <td>{m.autorizado_por}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal modal--sm" onClick={e => e.stopPropagation()}>
            <div className="modal__header"><h3>Registrar Movimiento</h3><button className="btn-icon" onClick={() => setShowForm(false)}><X size={20} /></button></div>
            <form onSubmit={handleSubmit} className="modal__body">
              <div className="form-grid">
                <div className="form-group form-group--full"><label>Código Inventario *</label><input type="text" required value={form.codigo_inventario} onChange={e => setForm({...form, codigo_inventario: e.target.value})} placeholder="UNEG-ATL-03-00004" /></div>
                <div className="form-group"><label>Tipo *</label><select required value={form.tipo} onChange={e => setForm({...form, tipo: e.target.value})}>{TIPOS.map(t => <option key={t} value={t}>{t}</option>)}</select></div>
                <div className="form-group"><label>Sede Destino</label><select value={form.sede_destino} onChange={e => setForm({...form, sede_destino: e.target.value})}><option value="">Seleccionar</option>{sedes.map(s => <option key={s.codigo} value={s.codigo}>{s.nombre}</option>)}</select></div>
                <div className="form-group form-group--full"><label>Motivo *</label><input type="text" required value={form.motivo} onChange={e => setForm({...form, motivo: e.target.value})} /></div>
                <div className="form-group"><label>Autorizado por *</label><input type="text" required value={form.autorizado_por} onChange={e => setForm({...form, autorizado_por: e.target.value})} /></div>
                <div className="form-group"><label>Doc. Soporte</label><input type="text" value={form.documento_soporte} onChange={e => setForm({...form, documento_soporte: e.target.value})} placeholder="Oficio N..." /></div>
              </div>
              <div className="modal__actions">
                <button type="button" className="btn btn--ghost" onClick={() => setShowForm(false)}>Cancelar</button>
                <button type="submit" className="btn btn--primary" disabled={sending}>{sending ? <Loader className="spin" size={16} /> : <Check size={16} />} Registrar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
