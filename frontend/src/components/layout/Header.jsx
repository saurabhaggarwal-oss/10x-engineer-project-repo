import { useTheme } from '../../context/ThemeContext';
import styles from './Header.module.css';

export default function Header({ onToggleSidebar }) {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <button
          className={styles.menuBtn}
          onClick={onToggleSidebar}
          aria-label="Toggle sidebar"
          type="button"
        >
          ☰
        </button>
        <span className={styles.logo}>PromptLab</span>
      </div>
      <button
        className={styles.themeBtn}
        onClick={toggleTheme}
        aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        type="button"
      >
        {theme === 'light' ? '🌙' : '☀️'}
      </button>
    </header>
  );
}
