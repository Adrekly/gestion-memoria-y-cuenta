import { useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import {
  LayoutDashboard, Package, ArrowLeftRight, XCircle,
  FileBarChart, Bot, Building2, Menu, X, ChevronRight
} from 'lucide-react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/inventario', icon: Package, label: 'Inventario' },
  { to: '/movimientos', icon: ArrowLeftRight, label: 'Movimientos' },
  { to: '/desincorporaciones', icon: XCircle, label: 'Desincorporaciones' },
  { to: '/reportes', icon: FileBarChart, label: 'Reportes BM' },
  { to: '/asistente', icon: Bot, label: 'Asistente IA' },
  { to: '/sedes', icon: Building2, label: 'Sedes' },
];

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

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
        <Outlet />
      </main>
    </div>
  );
}
