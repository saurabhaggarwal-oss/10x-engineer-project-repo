import styles from './VersionHistory.module.css';

export default function VersionHistory({ versions, currentVersion, onSelectVersion, selectedVersion }) {
  if (!versions || versions.length <= 1) return null;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <span className={styles.headerIcon}>🕐</span>
        <h3 className={styles.heading}>Version History</h3>
        <span className={styles.count}>{versions.length} versions</span>
      </div>
      <div className={styles.timeline}>
        {versions.slice().reverse().map((v, i) => (
          <button
            key={v.version}
            className={`${styles.item} ${v.version === selectedVersion ? styles.active : ''}`}
            onClick={() => onSelectVersion(v.version)}
            type="button"
          >
            <div className={styles.dot}>
              <span className={`${styles.dotInner} ${v.version === currentVersion ? styles.dotCurrent : ''}`} />
              {i < versions.length - 1 && <span className={styles.line} />}
            </div>
            <div className={styles.itemContent}>
              <div className={styles.itemTop}>
                <span className={styles.versionNum}>Version {v.version}</span>
                {v.version === currentVersion && <span className={styles.badge}>Current</span>}
              </div>
              <time className={styles.date} dateTime={v.created_at}>
                {new Date(v.created_at).toLocaleString('en-US', {
                  month: 'short', day: 'numeric', year: 'numeric',
                  hour: 'numeric', minute: '2-digit',
                })}
              </time>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
