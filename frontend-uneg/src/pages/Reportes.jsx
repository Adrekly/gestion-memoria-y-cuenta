import { useState } from 'react';
import { FileBarChart, Download, Loader, FileText } from 'lucide-react';
import toast from 'react-hot-toast';

const API_BASE = 'http://localhost:8000/api';

const reportes = [
  { id: 'bm1', code: 'BM-1', title: 'Inventario de Bienes', desc: 'Foto actual de todos los bienes muebles de la UNEG.', color: '#003366' },
  { id: 'bm2', code: 'BM-2', title: 'Movimiento de Bienes', desc: 'Registro de entradas, salidas y traslados del periodo.', color: '#4A90D9' },
  { id: 'bm3', code: 'BM-3', title: 'Relacion de Bienes Faltantes', desc: 'Bienes extraviados, robados o no localizados.', color: '#E74C3C' },
  { id: 'bm4', code: 'BM-4', title: 'Resumen del Movimiento', desc: 'Insumo principal para la Memoria y Cuenta.', color: '#C4A35A' },
];

export default function Reportes() {
  const [generating, setGenerating] = useState(null);

  const descargar = async (id) => {
    setGenerating(id);
    try {
      const res = await fetch(`${API_BASE}/reportes/${id}`);
      if (!res.ok) throw new Error('Error generando reporte');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${id.toUpperCase()}_UNEG.pdf`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success(`Reporte ${id.toUpperCase()} descargado`);
    } catch (e) { toast.error(e.message); }
    finally { setGenerating(null); }
  };

  return (
    <div className="page">
      <div className="page__header">
        <div>
          <h2 className="page__title">Reportes BM (SUDEBIP)</h2>
          <p className="page__subtitle">Formularios oficiales para la Memoria y Cuenta</p>
        </div>
      </div>

      <div className="reportes-grid">
        {reportes.map(r => (
          <div key={r.id} className="reporte-card" style={{ '--reporte-color': r.color }}>
            <div className="reporte-card__header">
              <FileText size={28} />
              <span className="reporte-card__code">{r.code}</span>
            </div>
            <h3 className="reporte-card__title">{r.title}</h3>
            <p className="reporte-card__desc">{r.desc}</p>
            <button
              className="btn btn--primary btn--block"
              onClick={() => descargar(r.id)}
              disabled={generating === r.id}
            >
              {generating === r.id ? <><Loader className="spin" size={16} /> Generando...</> : <><Download size={16} /> Descargar PDF</>}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
