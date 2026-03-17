import { useState, useEffect } from 'react';
import { getPromptVersions } from '../../api/prompts';
import Button from '../shared/Button';
import VersionHistory from '../shared/VersionHistory';
import styles from './PromptDetail.module.css';

export default function PromptDetail({ prompt, collectionName, onEdit, onDelete, onBack }) {
  const [versions, setVersions] = useState([]);
  const [selectedVersion, setSelectedVersion] = useState(prompt.current_version || 1);
  const [viewData, setViewData] = useState(prompt);

  useEffect(() => {
    getPromptVersions(prompt.id)
      .then((data) => setVersions(data.versions))
      .catch(() => {});
  }, [prompt.id]);

  useEffect(() => {
    if (selectedVersion === prompt.current_version) {
      setViewData(prompt);
    } else {
      const v = versions.find((ver) => ver.version === selectedVersion);
      if (v) setViewData(v);
    }
  }, [selectedVersion, versions, prompt]);

  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${prompt.title}"? This cannot be undone.`)) {
      onDelete();
    }
  };

  const isOldVersion = selectedVersion !== prompt.current_version;
  const tags = viewData.tags || prompt.tags || [];

  return (
    <div className={styles.page}>
      {/* Top bar */}
      <div className={styles.topBar}>
        <button className={styles.backBtn} onClick={onBack} type="button">
          <span className={styles.backIcon}>←</span> Back
        </button>
        {!isOldVersion && (
          <div className={styles.actions}>
            <Button size="sm" onClick={onEdit}>✏️ Edit</Button>
            <Button variant="danger" size="sm" onClick={handleDelete}>🗑 Delete</Button>
          </div>
        )}
      </div>

      {isOldVersion && (
        <div className={styles.versionBanner}>
          <span className={styles.bannerIcon}>⏳</span>
          <span>Viewing version {selectedVersion} — this is a historical snapshot.</span>
          <button className={styles.versionLink} onClick={() => setSelectedVersion(prompt.current_version)}>
            Switch to current (v{prompt.current_version})
          </button>
        </div>
      )}

      {/* Hero card */}
      <div className={styles.heroCard}>
        <div className={styles.heroTop}>
          <div className={styles.heroIcon}>📝</div>
          <div className={styles.heroInfo}>
            <h1 className={styles.title}>{viewData.title}</h1>
            {viewData.description && (
              <p className={styles.subtitle}>{viewData.description}</p>
            )}
          </div>
        </div>

        <div className={styles.metaGrid}>
          {collectionName && (
            <div className={styles.metaItem}>
              <span className={styles.metaLabel}>Collection</span>
              <span className={styles.badge}>{collectionName}</span>
            </div>
          )}
          <div className={styles.metaItem}>
            <span className={styles.metaLabel}>Version</span>
            <span className={styles.metaValue}>v{selectedVersion}{isOldVersion ? '' : ' (latest)'}</span>
          </div>
          <div className={styles.metaItem}>
            <span className={styles.metaLabel}>Created</span>
            <span className={styles.metaValue}>
              {new Date(prompt.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
            </span>
          </div>
          {!isOldVersion && prompt.updated_at && (
            <div className={styles.metaItem}>
              <span className={styles.metaLabel}>Last updated</span>
              <span className={styles.metaValue}>
                {new Date(prompt.updated_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
              </span>
            </div>
          )}
          {tags.length > 0 && (
            <div className={styles.metaItem}>
              <span className={styles.metaLabel}>Tags</span>
              <div className={styles.tagList}>
                {tags.map((t) => <span key={t} className={styles.tag}>{t}</span>)}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Content card */}
      <div className={styles.contentCard}>
        <div className={styles.cardHeader}>
          <span className={styles.cardIcon}>💬</span>
          <h2 className={styles.cardTitle}>Prompt Content</h2>
        </div>
        <div className={styles.contentBody}>{viewData.content}</div>
      </div>

      {/* Version history */}
      <VersionHistory
        versions={versions}
        currentVersion={prompt.current_version}
        selectedVersion={selectedVersion}
        onSelectVersion={setSelectedVersion}
      />
    </div>
  );
}
