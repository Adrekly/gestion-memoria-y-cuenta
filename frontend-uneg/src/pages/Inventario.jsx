import { useState, useEffect, useCallback } from 'react';
import { Plus, Search, Filter, Eye, Edit, Package, X, Check, Loader } from 'lucide-react';
import { bienesAPI, sedesAPI, clasificadorAPI } from '../services/api';
import toast from 'react-hot-toast';

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

  const [form, setForm] = useState({
    codigo_sudebip: '', grupo_sudebip: '', descripcion: '', marca: '', modelo: '',
    serial: '', valor_adquisicion: '', fecha_adquisicion: '', condicion: 'BUENO',
    sede_codigo: '', ubicacion_especifica: '', responsable: '', cedula_responsable: '',
    departamento: '', observaciones: '',
  });

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
        fecha_adquisicion: new Date(raw.fecha_adquisicion).toISOString(),
      };
      await bienesAPI.crear(payload);
      toast.success('Bien registrado exitosamente');
      setShowForm(false);
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

  const totalPaginas = Math.ceil(total / 15);

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
                    <button className="btn-icon" title="Ver detalle" onClick={() => setShowDetail(b)}><Eye size={16} /></button>
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
              <h3>Registrar Nuevo Bien</h3>
              <button className="btn-icon" onClick={() => setShowForm(false)}><X size={20} /></button>
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
                <button type="button" className="btn btn--ghost" onClick={() => setShowForm(false)}>Cancelar</button>
                <button type="submit" className="btn btn--primary" disabled={sending}>
                  {sending ? <><Loader className="spin" size={16} /> Guardando...</> : <><Check size={16} /> Registrar Bien</>}
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
                ['Estado', showDetail.estado],
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
          </div>
        </div>
      )}
    </div>
  );
}
