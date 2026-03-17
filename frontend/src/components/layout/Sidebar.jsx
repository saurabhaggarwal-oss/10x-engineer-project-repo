import styles from './Sidebar.module.css';

export default function Sidebar({ activePage, onNavigate }) {
  return (
    <nav className={styles.sidebar} aria-label="Main navigation">
      <ul className={styles.list}>
        <li>
          <button
            className={`${styles.item} ${activePage === 'collections' ? styles.active : ''}`}
            onClick={() => onNavigate('collections')}
            aria-current={activePage === 'collections' ? 'page' : undefined}
            title="Collections"
          >
            <span className={styles.icon}>📁</span>
            <span className={styles.label}>Collections</span>
          </button>
        </li>
        <li>
          <button
            className={`${styles.item} ${activePage === 'prompts' ? styles.active : ''}`}
            onClick={() => onNavigate('prompts')}
            aria-current={activePage === 'prompts' ? 'page' : undefined}
            title="Prompts"
          >
            <span className={styles.icon}>📝</span>
            <span className={styles.label}>Prompts</span>
          </button>
        </li>
      </ul>
    </nav>
  );
}
