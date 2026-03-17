import { useState } from 'react';
import Header from './Header';
import styles from './Layout.module.css';

export default function Layout({ children, sidebar }) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className={styles.layout}>
      <Header
        onToggleSidebar={() => {
          // mobile: toggle overlay, desktop: collapse
          if (window.innerWidth <= 768) {
            setMobileOpen((v) => !v);
          } else {
            setCollapsed((v) => !v);
          }
        }}
      />
      <div className={styles.body}>
        <aside className={`${styles.sidebar} ${collapsed ? styles.collapsed : ''} ${mobileOpen ? styles.mobileOpen : ''}`}>
          {sidebar}
        </aside>
        {mobileOpen && (
          <div
            className={styles.overlay}
            onClick={() => setMobileOpen(false)}
            aria-hidden="true"
          />
        )}
        <main className={styles.main}>{children}</main>
      </div>
    </div>
  );
}
