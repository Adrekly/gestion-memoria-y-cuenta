import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Package, MapPin, Loader, Clock, Tag, User, AlignLeft, ShieldAlert, ArrowLeftRight, Wrench, CheckCircle } from 'lucide-react';
import { bienesAPI } from '../services/api';
import toast from 'react-hot-toast';

const ACCION_LABELS = {
  CREAR: 'Registro Inicial',
  ACTUALIZAR: 'Actualización de Datos',
  CAMBIO_ESTADO: 'Cambio de Estado',
  DESINCORPORAR: 'Solicitud de Baja',
  DESINCORPORACION_APROBADA: 'Baja Aprobada',
  DESINCORPORACION_RECHAZADA: 'Baja Rechazada',
  MOVIMIENTO: 'Movimiento Registrado',
};

export default function BienDetalle() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Estados para Mantenimiento
  const [showModal, setShowModal] = useState(false);
  const [motivo, setMotivo] = useState('');
  const [procesando, setProcesando] = useState(false);

  useEffect(() => {
    bienesAPI.obtenerHistorial(id)
      .then(setData)
      .catch(e => toast.error('Error cargando historial: ' + e.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="page-loading"><Loader className="spin" size={32} /> Cargando detalles...</div>;
  if (!data) return <div className="empty-state">No se encontró el bien.</div>;

  const { bien, historial } = data;

  const handleMantenimiento = async (e) => {
    e.preventDefault();
    if (!motivo.trim() || motivo.length < 5) {
      toast.error('Ingrese un motivo detallado (mín. 5 caracteres)');
      return;
    }
    
    setProcesando(true);
    try {
      const nuevoEstado = bien.estado === 'EN_REPARACION' ? 'EN_USO' : 'EN_REPARACION';
      await bienesAPI.cambiarEstado(bien._id, { estado: nuevoEstado, motivo });
      
      toast.success(nuevoEstado === 'EN_USO' ? 'Reparación finalizada' : 'Enviado a reparación');
      setShowModal(false);
      setMotivo('');
      
      // Recargar datos
      const newData = await bienesAPI.obtenerHistorial(id);
      setData(newData);
    } catch (error) {
      toast.error('Error al actualizar estado: ' + error.message);
    } finally {
      setProcesando(false);
    }
  };

  return (
    <div className="page" style={{ maxWidth: '900px' }}>
      <div className="page__header" style={{ marginBottom: '16px' }}>
        <div>
          <Link to="/inventario" className="btn btn--ghost btn--sm" style={{ marginBottom: '12px' }}>
            <ArrowLeft size={14} /> Volver al inventario
          </Link>
          <h2 className="page__title" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {bien.codigo_inventario}
            <span className="badge" style={{ fontSize: '12px', background: 'var(--primary)' }}>
              {bien.estado}
            </span>
          </h2>
          <p className="page__subtitle" style={{ fontSize: '16px', color: 'var(--text)', marginTop: '4px' }}>
            {bien.descripcion}
          </p>
        </div>
        
        {/* Acciones de Mantenimiento */}
        {bien.estado !== 'DESINCORPORADO' && bien.estado !== 'FALTANTE' && (
          <div>
            {bien.estado === 'EN_REPARACION' ? (
              <button className="btn btn--primary" onClick={() => setShowModal(true)}>
                <CheckCircle size={16} /> Finalizar Reparación
              </button>
            ) : (
              <button className="btn btn--secondary" onClick={() => setShowModal(true)} style={{ background: '#f59e0b', color: 'white', borderColor: '#f59e0b' }}>
                <Wrench size={16} /> Enviar a Reparación
              </button>
            )}
          </div>
        )}
      </div>

      <div className="reportes-grid" style={{ marginBottom: '24px' }}>
        <div className="reporte-card" style={{ padding: '16px' }}>
          <div className="detail-item__label"><MapPin size={12} style={{ display: 'inline', marginRight: 4 }}/> Ubicación Actual</div>
          <div className="detail-item__value">{bien.sede?.nombre}</div>
          {bien.departamento && <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Dpto: {bien.departamento}</div>}
          {bien.ubicacion_especifica && <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Área: {bien.ubicacion_especifica}</div>}
        </div>
        <div className="reporte-card" style={{ padding: '16px' }}>
          <div className="detail-item__label"><Tag size={12} style={{ display: 'inline', marginRight: 4 }}/> Identificación</div>
          <div className="detail-item__value">{bien.marca || 'S/M'} {bien.modelo ? `- ${bien.modelo}` : ''}</div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Serial: {bien.serial || 'N/A'}</div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>SUDEBIP: {bien.codigo_sudebip}</div>
        </div>
        <div className="reporte-card" style={{ padding: '16px' }}>
          <div className="detail-item__label"><User size={12} style={{ display: 'inline', marginRight: 4 }}/> Responsable</div>
          <div className="detail-item__value">{bien.responsable}</div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>C.I: {bien.cedula_responsable}</div>
        </div>
      </div>

      <h3 style={{ fontSize: '16px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Clock size={18} color="var(--accent)" /> Historial de Vida del Bien
      </h3>

      <div className="table-container" style={{ padding: '0' }}>
        {historial.length === 0 ? (
          <div className="table-empty">No hay eventos registrados.</div>
        ) : (
          <div className="audit-timeline">
            {historial.map((log) => (
              <div key={log._id} className={`audit-entry audit-entry--${log.accion}`}>
                <div className="audit-entry__time">
                  {new Date(log.fecha).toLocaleString('es-VE', { dateStyle: 'short', timeStyle: 'short' })}
                </div>
                <div className="audit-entry__body">
                  <div className="audit-entry__action">
                    {ACCION_LABELS[log.accion] || log.accion}
                  </div>
                  <div className="audit-entry__detail">
                    {log.usuario && log.usuario !== 'Sistema' && <><User size={10} style={{ display: 'inline' }} /> {log.usuario}</>}
                    {log.detalles?.motivo && <> — Motivo: {log.detalles.motivo}</>}
                    {log.detalles?.tipo && <> — Tipo: {log.detalles.tipo}</>}
                    {log.detalles?.sede_destino && <> — Destino: {log.detalles.sede_destino}</>}
                  </div>
                  {log.cambios && Object.keys(log.cambios).length > 0 && (
                    <div className="audit-entry__changes">
                      {Object.entries(log.cambios).map(([campo, vals]) => (
                        <span key={campo} className="audit-change">
                          {campo}: <span className="audit-change__old">{vals.anterior}</span>
                          <ArrowLeftRight size={10} style={{ margin: '0 4px' }} />
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

      {/* Modal Mantenimiento */}
      {showModal && (
        <div className="modal-backdrop">
          <div className="modal">
            <div className="modal__header">
              <h3>{bien.estado === 'EN_REPARACION' ? 'Finalizar Reparación' : 'Enviar a Reparación'}</h3>
            </div>
            <div className="modal__body">
              <form onSubmit={handleMantenimiento}>
                <div className="form-group">
                  <label>{bien.estado === 'EN_REPARACION' ? 'Reporte de la reparación realizada' : 'Motivo / Falla que presenta el bien'}</label>
                  <textarea
                    className="form-input"
                    value={motivo}
                    onChange={(e) => setMotivo(e.target.value)}
                    placeholder="Escriba los detalles aquí..."
                    rows={4}
                    required
                  ></textarea>
                </div>
                <div className="modal__footer">
                  <button type="button" className="btn btn--ghost" onClick={() => setShowModal(false)} disabled={procesando}>
                    Cancelar
                  </button>
                  <button type="submit" className="btn btn--primary" disabled={procesando}>
                    {procesando ? <Loader className="spin" size={16} /> : 'Confirmar'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
