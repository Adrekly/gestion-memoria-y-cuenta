import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Inventario from './pages/Inventario';
import Movimientos from './pages/Movimientos';
import Desincorporaciones from './pages/Desincorporaciones';
import Reportes from './pages/Reportes';
import Asistente from './pages/Asistente';
import Sedes from './pages/Sedes';

export default function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" toastOptions={{
        style: { background: '#1a1d23', color: '#fff', borderRadius: '10px', border: '1px solid #2a2d35' },
        success: { iconTheme: { primary: '#2ECC71', secondary: '#fff' } },
        error: { iconTheme: { primary: '#E74C3C', secondary: '#fff' } },
      }} />
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="/inventario" element={<Inventario />} />
          <Route path="/movimientos" element={<Movimientos />} />
          <Route path="/desincorporaciones" element={<Desincorporaciones />} />
          <Route path="/reportes" element={<Reportes />} />
          <Route path="/asistente" element={<Asistente />} />
          <Route path="/sedes" element={<Sedes />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}