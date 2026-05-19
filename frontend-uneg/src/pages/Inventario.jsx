import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Search, Eye, Edit, Package, X, Check, Loader, History, Wrench, RefreshCw } from 'lucide-react';
import { bienesAPI, sedesAPI, clasificadorAPI } from '../services/api';
import toast from 'react-hot-toast';

const ESTADOS_DISPONIBLES = [
  { value: 'EN_USO',        label: 'En Uso' },
  { value: 'EN_DESUSO',     label: 'En Desuso' },
  { value: 'INSERVIBLE',   label: 'Inservible' },
  { value: 'EN_REPARACION', label: 'En Reparación' },
  { value: 'FALTANTE',     label: 'Faltante' },
];

const ESTADOS = ['EN_USO', 'EN_DESUSO', 'INSERVIBLE', 'EN_REPARACION', 'FALTANTE', 'DESINCORPORADO'];
const CONDICIONES = ['BUENO', 'REGULAR', 'MALO'];
const ESTADO_COLORS = {
  EN_USO: '#2ECC71', EN_DESUSO: '#F39C12', INSERVIBLE: '#E74C3C',
  EN_REPARACION: '#3498DB', FALTANTE: '#E74C3C', DESINCORPORADO: '#95A5A6',
};

export default function Inventario() {
  const [bienes, setBienes] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [pagina, setPagina] = useState(1);
  const [busqueda, setBusqueda] = useState('');
  const [filtroSede, setFiltroSede] = useState('');
  const [filtroEstado, setFiltroEstado] = useState('');
  const [sedes, setSedes] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showDetail, setShowDetail] = useState(null);
  const [sending, setSending] = useState(false);

  // Estado para modal de cambio de estado
  const [showMaintModal, setShowMaintModal] = useState(false);
  const [maintBien, setMaintBien] = useState(null);
  const [maintNuevoEstado, setMaintNuevoEstado] = useState('');
  const [maintMotivo, setMaintMotivo] = useState('');
  const [maintProcesando, setMaintProcesando] = useState(false);

  const [form, setForm] = useState({
    codigo_sudebip: '', grupo_sudebip: '', descripcion: '', marca: '', modelo: '',
    serial: '', valor_adquisicion: '', fecha_adquisicion: '', condicion: 'BUENO',
    sede_codigo: '', ubicacion_especifica: '', responsable: '', cedula_responsable: '',
    departamento: '', observaciones: '',
  });

  const [editingId, setEditingId] = useState(null);

  const [sugerenciasSudebip, setSugerenciasSudebip] = useState([]);

  const cargarBienes = useCallback(async () => {
    setLoading(true);
    try {
      const params = { pagina, por_pagina: 15 };
      if (busqueda) params.busqueda = busqueda;
      if (filtroSede) params.sede = filtroSede;
      if (filtroEstado) params.estado = filtroEstado;
      const data = await bienesAPI.listar(params);
      setBienes(data.bienes);
      setTotal(data.total);
    } catch (e) {
      toast.error('Error al cargar bienes: ' + e.message);
    } finally {
      setLoading(false);
    }
  }, [pagina, busqueda, filtroSede, filtroEstado]);

  useEffect(() => { cargarBienes(); }, [cargarBienes]);
  useEffect(() => { sedesAPI.listar().then(setSedes).catch(() => {}); }, []);

  const buscarSudebip = async (query) => {
    if (query.length < 2) { setSugerenciasSudebip([]); return; }
    try {
      const data = await clasificadorAPI.buscar(query);
      setSugerenciasSudebip(data.resultados || []);
    } catch { setSugerenciasSudebip([]); }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSending(true);
    try {
      const raw = { ...form };
      // Limpiar strings vacíos a null para campos opcionales
      ['marca', 'modelo', 'serial', 'ubicacion_especifica', 'observaciones'].forEach(k => {
        if (!raw[k] || raw[k].trim() === '') raw[k] = null;
      });
      const payload = {
        ...raw,
        valor_adquisicion: parseFloat(raw.valor_adquisicion),
      };
      if (raw.fecha_adquisicion) {
         payload.fecha_adquisicion = new Date(raw.fecha_adquisicion).toISOString();
      }
      
      if (editingId) {
        await bienesAPI.actualizar(editingId, payload);
        toast.success('Bien actualizado exitosamente');
      } else {
        await bienesAPI.crear(payload);
        toast.success('Bien registrado exitosamente');
      }
      setShowForm(false);
      setEditingId(null);
      setForm({
        codigo_sudebip: '', grupo_sudebip: '', descripcion: '', marca: '', modelo: '',
        serial: '', valor_adquisicion: '', fecha_adquisicion: '', condicion: 'BUENO',
        sede_codigo: '', ubicacion_especifica: '', responsable: '', cedula_responsable: '',
        departamento: '', observaciones: '',
      });
      cargarBienes();
    } catch (e) {
      toast.error(e.message);
    } finally {
      setSending(false);
    }
  };

  const handleEdit = (bien) => {
    setForm({
      codigo_sudebip: bien.codigo_sudebip || '',
      grupo_sudebip: bien.grupo_sudebip || '',
      descripcion: bien.descripcion || '',
      marca: bien.marca || '',
      modelo: bien.modelo || '',
      serial: bien.serial || '',
      valor_adquisicion: bien.valor_adquisicion || '',
      fecha_adquisicion: bien.fecha_adquisicion ? bien.fecha_adquisicion.split('T')[0] : '',
      condicion: bien.condicion || 'BUENO',
      sede_codigo: bien.sede?.codigo || '',
      ubicacion_especifica: bien.ubicacion_especifica || '',
      responsable: bien.responsable || '',
      cedula_responsable: bien.cedula_responsable || '',
      departamento: bien.departamento || '',
      observaciones: bien.observaciones || '',
    });
    setEditingId(bien.id || bien._id);
    setShowForm(true);
  };

  const totalPaginas = Math.ceil(total / 15);

  const abrirCambioEstado = (bien) => {
    setMaintBien(bien);
    setMaintNuevoEstado(bien.estado);
    setMaintMotivo('');
    setShowDetail(null); // cerrar detalle rápido si estaba abierto
    setShowMaintModal(true);
  };

  const handleCambioEstado = async (e) => {
    e.preventDefault();
    if (!maintMotivo.trim() || maintMotivo.length < 10) {
      toast.error('El motivo debe tener al menos 10 caracteres');
      return;
    }
    if (maintNuevoEstado === maintBien.estado) {
      toast.error('Seleccione un estado diferente al actual');
      return;
    }
    setMaintProcesando(true);
    try {
      await bienesAPI.cambiarEstado(maintBien.id || maintBien._id, { estado: maintNuevoEstado, motivo: maintMotivo });
      const estadoLabel = ESTADOS_DISPONIBLES.find(e => e.value === maintNuevoEstado)?.label || maintNuevoEstado;
      toast.success(`Estado actualizado a "${estadoLabel}"`);
      setShowMaintModal(false);
      cargarBienes();
    } catch (err) {
      toast.error('Error: ' + err.message);
    } finally {
      setMaintProcesando(false);
    }
  };

  return (
    <div className="page">
      <div className="page__header">
        <div>
          <h2 className="page__title">Inventario de Bienes</h2>
          <p className="page__subtitle">{total} bienes registrados</p>
        </div>
        <button className="btn btn--primary" onClick={() => setShowForm(true)}>
          <Plus size={18} /> Nuevo Bien
        </button>
      </div>

      {/* Filtros */}
      <div className="filters-bar">
        <div className="search-input">
          <Search size={16} />
          <input type="text" placeholder="Buscar por descripcion..." value={busqueda}
            onChange={e => { setBusqueda(e.target.value); setPagina(1); }} />
        </div>
        <select className="select-filter" value={filtroSede} onChange={e => { setFiltroSede(e.target.value); setPagina(1); }}>
          <option value="">Todas las sedes</option>
          {sedes.map(s => <option key={s.codigo} value={s.codigo}>{s.nombre}</option>)}
        </select>
        <select className="select-filter" value={filtroEstado} onChange={e => { setFiltroEstado(e.target.value); setPagina(1); }}>
          <option value="">Todos los estados</option>
          {ESTADOS.map(e => <option key={e} value={e}>{e.replace(/_/g, ' ')}</option>)}
        </select>
      </div>

      {/* Tabla */}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Cod. Inventario</th>
              <th>Descripcion</th>
              <th>Sede</th>
              <th>Estado</th>
              <th>Condicion</th>
              <th>Valor</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="7" className="table-loading"><Loader className="spin" size={20} /> Cargando...</td></tr>
            ) : bienes.length === 0 ? (
              <tr><td colSpan="7" className="table-empty"><Package size={32} /><br />No se encontraron bienes</td></tr>
            ) : (
              bienes.map(b => (
                <tr key={b.id || b._id}>
                  <td className="td-code">{b.codigo_inventario}</td>
                  <td>{b.descripcion}</td>
                  <td>{b.sede?.nombre || ''}</td>
                  <td><span className="badge" style={{ background: ESTADO_COLORS[b.estado] }}>{b.estado?.replace(/_/g, ' ')}</span></td>
                  <td>{b.condicion}</td>
                  <td className="td-money">${(b.valor_adquisicion || 0).toLocaleString('es-VE', { minimumFractionDigits: 2 })}</td>
                  <td>
                    <div style={{ display: 'flex', gap: '4px' }}>
                      <button className="btn-icon" title="Ver detalle rapido" onClick={() => setShowDetail(b)}><Eye size={16} /></button>
                      <button className="btn-icon" title="Editar" onClick={() => handleEdit(b)}><Edit size={16} /></button>
                      <Link to={`/inventario/${b.id || b._id}`} className="btn-icon" title="Ficha y historial completo"><History size={16} /></Link>
                      {b.estado !== 'DESINCORPORADO' && (
                        <button
                          className="btn-icon"
                          title="Cambiar Estado"
                          onClick={() => abrirCambioEstado(b)}
                          style={{ color: '#4A90D9' }}
                        >
                          <Wrench size={16} />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Paginacion */}
      {totalPaginas > 1 && (
        <div className="pagination">
          <button className="btn btn--sm" disabled={pagina <= 1} onClick={() => setPagina(p => p - 1)}>Anterior</button>
          <span className="pagination__info">Pagina {pagina} de {totalPaginas}</span>
          <button className="btn btn--sm" disabled={pagina >= totalPaginas} onClick={() => setPagina(p => p + 1)}>Siguiente</button>
        </div>
      )}

      {/* Modal Formulario */}
      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal__header">
              <h3>{editingId ? 'Editar Bien' : 'Registrar Nuevo Bien'}</h3>
              <button className="btn-icon" onClick={() => { setShowForm(false); setEditingId(null); }}><X size={20} /></button>
            </div>
            <form onSubmit={handleSubmit} className="modal__body">
              <div className="form-grid">
                <div className="form-group form-group--full">
                  <label>Descripcion del bien *</label>
                  <input type="text" required value={form.descripcion}
                    onChange={e => { setForm({...form, descripcion: e.target.value}); buscarSudebip(e.target.value); }}
                    placeholder="Ej: Escritorio ejecutivo de madera" />
                  {sugerenciasSudebip.length > 0 && (
                    <div className="sudebip-suggestions">
                      <p className="sudebip-suggestions__title">Sugerencias SUDEBIP:</p>
                      {sugerenciasSudebip.slice(0, 5).map(s => (
                        <button key={s.codigo} type="button" className="sudebip-suggestion"
                          onClick={() => { setForm({...form, codigo_sudebip: s.codigo, grupo_sudebip: s.descripcion_subgrupo || s.descripcion}); setSugerenciasSudebip([]); }}>
                          <strong>{s.codigo}</strong> — {s.descripcion} ({s.descripcion_subgrupo})
                        </button>
                      ))}
                    </div>
                  )}
                </div>
                <div className="form-group">
                  <label>Codigo SUDEBIP *</label>
                  <input type="text" required value={form.codigo_sudebip} onChange={e => setForm({...form, codigo_sudebip: e.target.value})} placeholder="1.02.01.01" />
                </div>
                <div className="form-group">
                  <label>Grupo SUDEBIP *</label>
                  <input type="text" required value={form.grupo_sudebip} onChange={e => setForm({...form, grupo_sudebip: e.target.value})} placeholder="Mobiliario y Equipos" />
                </div>
                <div className="form-group"><label>Marca</label><input type="text" value={form.marca} onChange={e => setForm({...form, marca: e.target.value})} /></div>
                <div className="form-group"><label>Modelo</label><input type="text" value={form.modelo} onChange={e => setForm({...form, modelo: e.target.value})} /></div>
                <div className="form-group"><label>Serial</label><input type="text" value={form.serial} onChange={e => setForm({...form, serial: e.target.value})} /></div>
                <div className="form-group"><label>Valor de Adquisicion *</label><input type="number" step="0.01" required value={form.valor_adquisicion} onChange={e => setForm({...form, valor_adquisicion: e.target.value})} /></div>
                <div className="form-group"><label>Fecha de Adquisicion *</label><input type="date" required value={form.fecha_adquisicion} onChange={e => setForm({...form, fecha_adquisicion: e.target.value})} /></div>
                <div className="form-group">
                  <label>Condicion</label>
                  <select value={form.condicion} onChange={e => setForm({...form, condicion: e.target.value})}>
                    {CONDICIONES.map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label>Sede *</label>
                  <select required value={form.sede_codigo} onChange={e => setForm({...form, sede_codigo: e.target.value})}>
                    <option value="">Seleccionar sede</option>
                    {sedes.map(s => <option key={s.codigo} value={s.codigo}>{s.nombre}</option>)}
                  </select>
                </div>
                <div className="form-group"><label>Ubicacion especifica</label><input type="text" value={form.ubicacion_especifica} onChange={e => setForm({...form, ubicacion_especifica: e.target.value})} placeholder="Edificio A, Piso 2" /></div>
                <div className="form-group"><label>Responsable *</label><input type="text" required value={form.responsable} onChange={e => setForm({...form, responsable: e.target.value})} /></div>
                <div className="form-group"><label>Cedula *</label><input type="text" required value={form.cedula_responsable} onChange={e => setForm({...form, cedula_responsable: e.target.value})} placeholder="V-12345678" /></div>
                <div className="form-group"><label>Departamento *</label><input type="text" required value={form.departamento} onChange={e => setForm({...form, departamento: e.target.value})} /></div>
                <div className="form-group form-group--full"><label>Observaciones</label><textarea value={form.observaciones} onChange={e => setForm({...form, observaciones: e.target.value})} rows={2} /></div>
              </div>
              <div className="modal__actions">
                <button type="button" className="btn btn--ghost" onClick={() => { setShowForm(false); setEditingId(null); }}>Cancelar</button>
                <button type="submit" className="btn btn--primary" disabled={sending}>
                  {sending ? <><Loader className="spin" size={16} /> Guardando...</> : <><Check size={16} /> {editingId ? 'Actualizar Bien' : 'Registrar Bien'}</>}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Detalle */}
      {showDetail && (
        <div className="modal-overlay" onClick={() => setShowDetail(null)}>
          <div className="modal modal--sm" onClick={e => e.stopPropagation()}>
            <div className="modal__header">
              <h3>Detalle del Bien</h3>
              <button className="btn-icon" onClick={() => setShowDetail(null)}><X size={20} /></button>
            </div>
            <div className="modal__body detail-grid">
              {[
                ['Codigo Inventario', showDetail.codigo_inventario],
                ['Codigo SUDEBIP', showDetail.codigo_sudebip],
                ['Grupo', showDetail.grupo_sudebip],
                ['Descripcion', showDetail.descripcion],
                ['Marca', showDetail.marca],
                ['Modelo', showDetail.modelo],
                ['Serial', showDetail.serial],
                ['Valor', `$${(showDetail.valor_adquisicion || 0).toLocaleString('es-VE', { minimumFractionDigits: 2 })}`],
                ['Estado', showDetail.estado?.replace(/_/g, ' ')],
                ['Condicion', showDetail.condicion],
                ['Sede', showDetail.sede?.nombre],
                ['Ubicacion', showDetail.ubicacion_especifica],
                ['Responsable', showDetail.responsable],
                ['Cedula', showDetail.cedula_responsable],
                ['Departamento', showDetail.departamento],
              ].map(([label, value]) => value && (
                <div key={label} className="detail-item">
                  <span className="detail-item__label">{label}</span>
                  <span className="detail-item__value">{value}</span>
                </div>
              ))}
            </div>
            {showDetail.estado !== 'DESINCORPORADO' && (
              <div className="modal__actions">
                <Link
                  to={`/inventario/${showDetail.id || showDetail._id}`}
                  className="btn btn--ghost btn--sm"
                  onClick={() => setShowDetail(null)}
                >
                  <History size={14} /> Ver Ficha Completa
                </Link>
                <button
                  className="btn btn--primary btn--sm"
                  onClick={() => abrirCambioEstado(showDetail)}
                >
                  <Wrench size={14} /> Cambiar Estado
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Modal Cambio de Estado */}
      {showMaintModal && maintBien && (
        <div className="modal-overlay" onClick={() => setShowMaintModal(false)}>
          <div className="modal modal--sm" onClick={e => e.stopPropagation()}>
            <div className="modal__header">
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <RefreshCw size={18} color="var(--accent)" /> Cambiar Estado del Bien
              </h3>
              <button className="btn-icon" onClick={() => setShowMaintModal(false)}><X size={20} /></button>
            </div>
            <form onSubmit={handleCambioEstado} className="modal__body">
              <div className="form-group" style={{ marginBottom: '8px' }}>
                <label>Bien</label>
                <div style={{ padding: '8px 12px', background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)', fontSize: '13px', color: 'var(--accent)', border: '1px solid var(--border)', fontWeight: 600 }}>
                  {maintBien.codigo_inventario} — {maintBien.descripcion}
                </div>
              </div>
              <div className="form-group" style={{ marginBottom: '8px' }}>
                <label>Estado actual</label>
                <div style={{ padding: '8px 12px', background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)', fontSize: '13px', color: 'var(--text-secondary)', border: '1px solid var(--border)' }}>
                  {ESTADOS_DISPONIBLES.find(e => e.value === maintBien.estado)?.label || maintBien.estado}
                </div>
              </div>
              <div className="form-group" style={{ marginBottom: '8px' }}>
                <label>Nuevo estado *</label>
                <select
                  value={maintNuevoEstado}
                  onChange={e => setMaintNuevoEstado(e.target.value)}
                  required
                  style={{ background: 'var(--bg-input)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', padding: '10px 12px', color: 'var(--text)', fontSize: '13px', width: '100%' }}
                >
                  {ESTADOS_DISPONIBLES.map(opt => (
                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                  ))}
                </select>
              </div>
              <div className="form-group" style={{ marginBottom: '4px' }}>
                <label>Motivo del cambio * (mín. 10 caracteres)</label>
                <textarea
                  value={maintMotivo}
                  onChange={e => setMaintMotivo(e.target.value)}
                  placeholder="Describa el motivo del cambio de estado..."
                  rows={4}
                  required
                  minLength={10}
                  style={{ background: 'var(--bg-input)', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', padding: '10px 12px', color: 'var(--text)', fontSize: '13px', width: '100%', fontFamily: 'inherit', resize: 'vertical' }}
                />
                <span style={{ fontSize: '11px', color: maintMotivo.length < 10 ? 'var(--warning)' : 'var(--success)', marginTop: '4px', display: 'block' }}>
                  {maintMotivo.length} / 10 caracteres mínimos
                </span>
              </div>
              <div className="modal__actions">
                <button type="button" className="btn btn--ghost" onClick={() => setShowMaintModal(false)} disabled={maintProcesando}>
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn btn--primary"
                  disabled={maintProcesando || maintMotivo.length < 10 || maintNuevoEstado === maintBien.estado}
                >
                  {maintProcesando ? <Loader className="spin" size={16} /> : <><RefreshCw size={14} /> Confirmar Cambio</>}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
