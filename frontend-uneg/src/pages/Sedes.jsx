import { useState, useEffect } from 'react';
import { Building2, Loader, MapPin } from 'lucide-react';
import { sedesAPI } from '../services/api';
import toast from 'react-hot-toast';

export default function Sedes() {
  const [sedes, setSedes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    sedesAPI.listar()
      .then(setSedes)
      .catch(e => toast.error(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="page-loading"><Loader className="spin" size={32} /></div>;

  return (
    <div className="page">
      <div className="page__header">
        <div>
          <h2 className="page__title">Sedes de la UNEG</h2>
          <p className="page__subtitle">{sedes.length} sedes registradas</p>
        </div>
      </div>

      <div className="sedes-grid">
        {sedes.map(s => (
          <div key={s.codigo} className={`sede-card ${s.activa ? '' : 'sede-card--inactive'}`}>
            <div className="sede-card__header">
              <Building2 size={24} />
              <span className="sede-card__code">{s.codigo}</span>
            </div>
            <h3 className="sede-card__name">{s.nombre}</h3>
            <div className="sede-card__info">
              <MapPin size={14} />
              <span>{s.ciudad}</span>
            </div>
            {s.direccion && <p className="sede-card__address">{s.direccion}</p>}
            <span className={`badge ${s.activa ? 'badge--success' : 'badge--muted'}`}>
              {s.activa ? 'Activa' : 'Inactiva'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
