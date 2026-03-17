import LoadingSpinner from '../shared/LoadingSpinner';
import ErrorMessage from '../shared/ErrorMessage';
import styles from './CollectionList.module.css';

export default function CollectionList({ collections, promptCountMap = {}, onSelect, onDelete, loading, error }) {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!collections.length) {
    return (
      <div className={styles.emptyState}>
        <span className={styles.emptyIcon} aria-hidden="true">📁</span>
        <p className={styles.emptyText}>No collections yet. Create your first collection!</p>
      </div>
    );
  }

  const handleDelete = (e, id) => {
    e.stopPropagation();
    if (window.confirm('Delete this collection? Prompts in it will be unlinked.')) onDelete(id);
  };

  return (
    <div className={styles.grid} role="list" aria-label="Collections">
      {collections.map((c) => (
        <button
          key={c.id}
          className={styles.card}
          onClick={() => onSelect(c.id)}
          type="button"
          role="listitem"
          aria-label={`View collection: ${c.name}`}
        >
          <h3 className={styles.name}>{c.name}</h3>
          {c.description && <p className={styles.desc}>{c.description}</p>}
          <div className={styles.footer}>
            <span className={styles.count}>{promptCountMap[c.id] || 0} prompts</span>
            <span
              className={styles.deleteBtn}
              role="button"
              tabIndex={0}
              aria-label={`Delete ${c.name}`}
              onClick={(e) => handleDelete(e, c.id)}
              onKeyDown={(e) => { if (e.key === 'Enter') handleDelete(e, c.id); }}
            >
              ×
            </span>
          </div>
        </button>
      ))}
    </div>
  );
}
