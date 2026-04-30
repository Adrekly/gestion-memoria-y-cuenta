import { useState, useEffect } from 'react';
import { Package, Building2, AlertTriangle, DollarSign, TrendingUp, Activity, ShieldAlert, ArrowLeftRight, Wrench } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { bienesAPI } from '../services/api';

const COLORS = ['#003366', '#4A90D9', '#C4A35A', '#2ECC71', '#E74C3C', '#9B59B6', '#F39C12', '#1ABC9C'];
const CONDICION_COLORS = { BUENO: '#2ECC71', REGULAR: '#F39C12', MALO: '#E74C3C' };

function KPICard({ icon: Icon, label, value, color, sub }) {
  return (
    <div className="kpi-card" style={{ '--kpi-color': color }}>
      <div className="kpi-card__icon">
        <Icon size={24} />
      </div>
      <div className="kpi-card__info">
        <p className="kpi-card__label">{label}</p>
        <h3 className="kpi-card__value">{value}</h3>
        {sub && <p className="kpi-card__sub">{sub}</p>}
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    bienesAPI.estadisticas()
      .then(setStats)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="page-loading"><Activity className="spin" size={32} /> Cargando dashboard...</div>;
  if (error) return (
    <div className="page">
      <div className="page__header">
        <h2 className="page__title">Dashboard</h2>
      </div>
      <div className="empty-state">
        <AlertTriangle size={48} />
        <h3>No se pudo conectar con el servidor</h3>
        <p>{error}</p>
        <p className="empty-state__hint">Asegurate de que el backend y MongoDB esten corriendo.</p>
      </div>
    </div>
  );

  const sedeData = Object.entries(stats.por_sede || {}).map(([name, value]) => ({ name, value }));
  const estadoData = Object.entries(stats.por_estado || {}).map(([name, value]) => ({ name, value }));
  const grupoData = Object.entries(stats.por_grupo_sudebip || {}).map(([name, value]) => ({ name: name.substring(0, 25), value }));
  const condicionData = Object.entries(stats.por_condicion || {}).map(([name, value]) => ({ name, value }));

  const faltantes = stats.por_estado?.FALTANTE || 0;
  const enUso = stats.por_estado?.EN_USO || 0;

  return (
    <div className="page">
      <div className="page__header">
        <h2 className="page__title">Dashboard</h2>
        <p className="page__subtitle">Resumen del inventario de bienes de la UNEG</p>
      </div>

      {/* KPI Cards */}
      <div className="kpi-grid">
        <KPICard icon={Package} label="Total de Bienes" value={stats.total_bienes} color="#003366" sub="Registrados en el sistema" />
        <KPICard icon={TrendingUp} label="En Uso" value={enUso} color="#2ECC71" sub={`${stats.total_bienes ? ((enUso / stats.total_bienes) * 100).toFixed(0) : 0}% del total`} />
        <KPICard icon={DollarSign} label="Valor Total" value={`$${(stats.valor_total || 0).toLocaleString('es-VE', { minimumFractionDigits: 2 })}`} color="#C4A35A" sub="Patrimonio activo" />
        <KPICard icon={AlertTriangle} label="Faltantes" value={faltantes} color={faltantes > 0 ? '#E74C3C' : '#2ECC71'} sub={faltantes > 0 ? 'Requiere atencion' : 'Sin novedades'} />
        <KPICard icon={ShieldAlert} label="Bajas Pendientes" value={stats.desincorporaciones_pendientes || 0} color={stats.desincorporaciones_pendientes > 0 ? '#F39C12' : '#2ECC71'} sub={stats.desincorporaciones_pendientes > 0 ? 'Solicitudes por revisar' : 'Al dia'} />
      </div>

      {/* Charts */}
      <div className="charts-grid">
        {/* Por Sede */}
        <div className="chart-card">
          <h3 className="chart-card__title">
            <Building2 size={18} /> Bienes por Sede
          </h3>
          {sedeData.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={sedeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                <XAxis dataKey="name" tick={{ fontSize: 10 }} angle={-20} textAnchor="end" height={60} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="value" name="Bienes" radius={[6, 6, 0, 0]}>
                  {sedeData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="chart-card__empty">No hay datos de sedes disponibles</p>
          )}
        </div>

        {/* Por Estado */}
        <div className="chart-card">
          <h3 className="chart-card__title">
            <Activity size={18} /> Distribucion por Estado
          </h3>
          {estadoData.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={estadoData} cx="50%" cy="50%" innerRadius={55} outerRadius={90} dataKey="value" label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`} labelLine={true}>
                  {estadoData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="chart-card__empty">No hay datos de estados disponibles</p>
          )}
        </div>

        {/* Por Condición */}
        {condicionData.length > 0 && (
          <div className="chart-card">
            <h3 className="chart-card__title">
              <Wrench size={18} /> Condicion de los Bienes
            </h3>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={condicionData} cx="50%" cy="50%" innerRadius={55} outerRadius={90} dataKey="value" label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`} labelLine={true}>
                  {condicionData.map((entry, i) => <Cell key={i} fill={CONDICION_COLORS[entry.name] || COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Por Grupo SUDEBIP */}
        {grupoData.length > 0 && (
          <div className="chart-card chart-card--wide">
            <h3 className="chart-card__title">
              <Package size={18} /> Bienes por Grupo SUDEBIP
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={grupoData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                <XAxis type="number" tick={{ fontSize: 11 }} />
                <YAxis type="category" dataKey="name" width={180} tick={{ fontSize: 9 }} />
                <Tooltip />
                <Bar dataKey="value" name="Cantidad" fill="#4A90D9" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Últimos Movimientos */}
      {stats.ultimos_movimientos && stats.ultimos_movimientos.length > 0 && (
        <div style={{ marginTop: '16px' }}>
          <div className="chart-card">
            <h3 className="chart-card__title">
              <ArrowLeftRight size={18} /> Ultimos Movimientos
            </h3>
            <table className="data-table">
              <thead>
                <tr><th>Fecha</th><th>Tipo</th><th>Bien</th><th>Descripcion</th><th>Autorizado</th></tr>
              </thead>
              <tbody>
                {stats.ultimos_movimientos.map((m, i) => (
                  <tr key={i}>
                    <td>{m.fecha ? new Date(m.fecha).toLocaleDateString('es-VE') : ''}</td>
                    <td><span className="badge badge--outline">{m.tipo}</span></td>
                    <td className="td-code">{m.bien}</td>
                    <td>{m.descripcion}</td>
                    <td>{m.autorizado_por}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
