import { useState, useEffect } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Package, ArrowLeftRight, XCircle,
  FileBarChart, Bot, Building2, Menu, X, ChevronRight, Shield, Search, Moon, Sun
} from 'lucide-react';
import { bienesAPI } from '../services/api';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/inventario', icon: Package, label: 'Inventario' },
  { to: '/movimientos', icon: ArrowLeftRight, label: 'Movimientos' },
  { to: '/desincorporaciones', icon: XCircle, label: 'Desincorporaciones' },
  { to: '/reportes', icon: FileBarChart, label: 'Reportes BM' },
  { to: '/asistente', icon: Bot, label: 'Asistente IA' },
  { to: '/sedes', icon: Building2, label: 'Sedes' },
  { to: '/auditoria', icon: Shield, label: 'Auditoria' },
];

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const handleSearch = async (q) => {
    setSearchQuery(q);
    if (q.length < 2) { setSuggestions([]); return; }
    try {
      const res = await bienesAPI.buscarCodigo(q);
      setSuggestions(res);
    } catch { setSuggestions([]); }
  };

  const handleSelect = (bien) => {
    setSearchQuery('');
    setSuggestions([]);
    navigate(`/inventario/${bien.codigo_inventario}`);
  };

  return (
    <div className="layout-container">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'sidebar--open' : 'sidebar--closed'}`}>
        <div className="sidebar__header">
          {sidebarOpen && (
            <div className="sidebar__brand">
              <div className="sidebar__logo">MYC</div>
              <div>
                <h1 className="sidebar__title">Memoria y Cuenta</h1>
                <p className="sidebar__subtitle">UNEG</p>
              </div>
            </div>
          )}
          <button
            className="sidebar__toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle sidebar"
          >
            {sidebarOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>

        <nav className="sidebar__nav">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `sidebar__link ${isActive ? 'sidebar__link--active' : ''}`
              }
              title={label}
            >
              <Icon size={20} />
              {sidebarOpen && <span>{label}</span>}
              {sidebarOpen && <ChevronRight size={14} className="sidebar__link-arrow" />}
            </NavLink>
          ))}
        </nav>

        {sidebarOpen && (
          <div className="sidebar__footer">
            <p>SUDEBIP Compliance</p>
            <div className="sidebar__status">
              <span className="sidebar__dot"></span>
              Sistema Operativo
            </div>
          </div>
        )}
      </aside>

      {/* Main Content */}
      <main className={`main-content ${sidebarOpen ? '' : 'main-content--expanded'}`}>
        <div className="top-bar">
          <div className="top-bar__search">
            <Search size={16} />
            <input 
              type="text" 
              placeholder="Buscar bien por código o descripción..." 
              value={searchQuery}
              onChange={e => handleSearch(e.target.value)}
            />
            {suggestions.length > 0 && (
              <ul className="autocomplete-list" style={{ top: '40px', left: 0, width: '100%', maxWidth: '400px' }}>
                {suggestions.map(s => (
                  <li key={s.codigo_inventario} className="autocomplete-item" onClick={() => handleSelect(s)}>
                    <strong>{s.codigo_inventario}</strong>
                    <span>{s.descripcion}</span>
                    <small>{s.sede}</small>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <button className="btn-icon" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')} title="Alternar tema">
            {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </div>
        <Outlet />
      </main>
    </div>
  );
}
