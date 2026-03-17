import { useState, useEffect } from 'react';
import { getCollectionVersions } from '../../api/collections';
import Button from '../shared/Button';
import VersionHistory from '../shared/VersionHistory';
import styles from './CollectionDetail.module.css';

export default function CollectionDetail({ collection, promptCount, onEdit, onDelete, onViewPrompts, onBack }) {
  const [versions, setVersions] = useState([]);
  const [selectedVersion, setSelectedVersion] = useState(collection.current_version || 1);
  const [viewData, setViewData] = useState(collection);

  useEffect(() => {
    getCollectionVersions(collection.id)
      .then((data) => setVersions(data.versions))
      .catch(() => {});
  }, [collection.id]);

  useEffect(() => {
    if (selectedVersion === collection.current_version) {
      setViewData(collection);
    } else {
      const v = versions.find((ver) => ver.version === selectedVersion);
      if (v) setViewData(v);
    }
  }, [selectedVersion, versions, collection]);

  const handleDelete = () => {
    if (window.confirm(`Delete "${collection.name}"? Prompts will be unlinked.`)) {
      onDelete();
    }
  };

  const isOldVersion = selectedVersion !== collection.current_version;

  return (
    <div className={styles.page}>
      {/* Top bar */}
      <div className={styles.topBar}>
        <button className={styles.backBtn} onClick={onBack} type="button">
          <span className={styles.backIcon}>←</span> Back
        </button>
        {!isOldVersion && (
          <div className={styles.actions}>
            <Button size="sm" onClick={onViewPrompts}>📄 View Prompts</Button>
            <Button size="sm" onClick={onEdit}>✏️ Edit</Button>
            <Button variant="danger" size="sm" onClick={handleDelete}>🗑 Delete</Button>
          </div>
        )}
      </div>

      {isOldVersion && (
        <div className={styles.versionBanner}>
          <span className={styles.bannerIcon}>⏳</span>
          <span>Viewing version {selectedVersion} — this is a historical snapshot.</span>
          <button className={styles.versionLink} onClick={() => setSelectedVersion(collection.current_version)}>
            Switch to current (v{collection.current_version})
          </button>
        </div>
      )}

      {/* Hero card */}
      <div className={styles.heroCard}>
        <div className={styles.heroTop}>
          <div className={styles.heroIcon}>📁</div>
          <div className={styles.heroInfo}>
            <h1 className={styles.title}>{viewData.name}</h1>
            {viewData.description && (
              <p className={styles.subtitle}>{viewData.description}</p>
            )}
          </div>
        </div>

        <div className={styles.statsRow}>
          <div className={styles.statCard}>
            <span className={styles.statValue}>{promptCount}</span>
            <span className={styles.statLabel}>Prompts</span>
          </div>
          <div className={styles.statCard}>
            <span className={styles.statValue}>v{selectedVersion}</span>
            <span className={styles.statLabel}>{isOldVersion ? 'Viewing' : 'Current'}</span>
          </div>
          <div className={styles.statCard}>
            <span className={styles.statValue}>
              {new Date(collection.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            </span>
            <span className={styles.statLabel}>Created</span>
          </div>
        </div>
      </div>

      {/* Description card (if exists and non-empty) */}
      {viewData.description && (
        <div className={styles.descCard}>
          <div className={styles.cardHeader}>
            <span className={styles.cardIcon}>📋</span>
            <h2 className={styles.cardTitle}>Description</h2>
          </div>
          <div className={styles.descBody}>{viewData.description}</div>
        </div>
      )}

      {/* Quick action */}
      {!isOldVersion && (
        <button className={styles.promptsLink} onClick={onViewPrompts} type="button">
          <div className={styles.promptsLinkInner}>
            <span className={styles.promptsLinkIcon}>→</span>
            <div>
              <span className={styles.promptsLinkTitle}>Browse {promptCount} prompt{promptCount !== 1 ? 's' : ''}</span>
              <span className={styles.promptsLinkSub}>View and manage prompts in this collection</span>
            </div>
          </div>
        </button>
      )}

      {/* Version history */}
      <VersionHistory
        versions={versions}
        currentVersion={collection.current_version}
        selectedVersion={selectedVersion}
        onSelectVersion={setSelectedVersion}
      />
    </div>
  );
}
