/**
 * Servicio API — Comunicación con el backend FastAPI.
 */
const API_BASE = 'http://localhost:8000/api';

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  };

  const res = await fetch(url, config);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Error del servidor' }));
    let errorMessage = `Error ${res.status}`;
    
    if (Array.isArray(err.detail)) {
      // Formatear errores de validación de Pydantic (FastAPI 422)
      errorMessage = err.detail.map(e => `${e.loc.join('.')}: ${e.msg}`).join('\n');
    } else if (typeof err.detail === 'string') {
      errorMessage = err.detail;
    } else if (err.detail) {
      errorMessage = JSON.stringify(err.detail);
    }
    
    throw new Error(errorMessage);
  }

  // Si es PDF o Excel, retornar blob
  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/pdf') || contentType.includes('spreadsheetml')) {
    return res.blob();
  }
  return res.json();
}

// === BIENES ===
export const bienesAPI = {
  listar: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/bienes?${qs}`);
  },
  obtener: (id) => request(`/bienes/${id}`),
  obtenerHistorial: (id) => request(`/bienes/${id}/historial`),
  crear: (data) => request('/bienes', { method: 'POST', body: JSON.stringify(data) }),
  actualizar: (id, data) => request(`/bienes/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  cambiarEstado: (id, data) => request(`/bienes/${id}/estado`, { method: 'PATCH', body: JSON.stringify(data) }),
  estadisticas: () => request('/bienes/estadisticas'),
  buscarCodigo: (q) => request(`/bienes/buscar-codigo?q=${encodeURIComponent(q)}`),
};

// === MOVIMIENTOS ===
export const movimientosAPI = {
  listar: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/movimientos?${qs}`);
  },
  crear: (data) => request('/movimientos', { method: 'POST', body: JSON.stringify(data) }),
};

// === DESINCORPORACIONES ===
export const desincorporacionesAPI = {
  listar: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/desincorporaciones?${qs}`);
  },
  crear: (data) => request('/desincorporaciones', { method: 'POST', body: JSON.stringify(data) }),
  cambiarEstado: (id, data) => request(`/desincorporaciones/${id}/estado`, { method: 'PATCH', body: JSON.stringify(data) }),
};

// === SEDES ===
export const sedesAPI = {
  listar: () => request('/sedes'),
  crear: (data) => request('/sedes', { method: 'POST', body: JSON.stringify(data) }),
};

// === CLASIFICADOR ===
export const clasificadorAPI = {
  buscar: (q) => request(`/clasificador/buscar?q=${encodeURIComponent(q)}`),
  obtener: (codigo) => request(`/clasificador/${codigo}`),
};

// === CHAT ===
export const chatAPI = {
  consultar: (pregunta, historial = []) => request('/chat', { method: 'POST', body: JSON.stringify({ pregunta, historial }) }),
};

// === REPORTES ===
export const reportesAPI = {
  bm1: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/reportes/bm1?${qs}`);
  },
  bm1Excel: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/reportes/bm1/excel?${qs}`);
  },
  bm2: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/reportes/bm2?${qs}`);
  },
  bm3: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/reportes/bm3?${qs}`);
  },
  bm4: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/reportes/bm4?${qs}`);
  },
};

// === AUDITORIA ===
export const auditoriaAPI = {
  listar: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/auditoria?${qs}`);
  },
};
