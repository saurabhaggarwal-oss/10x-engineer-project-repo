import { useState } from 'react';
import Button from '../shared/Button';
import styles from './CollectionForm.module.css';

export default function CollectionForm({ collection, onSubmit, onCancel, saving }) {
  const [name, setName] = useState(collection?.name || '');
  const [description, setDescription] = useState(collection?.description || '');
  const [error, setError] = useState('');

  const isEdit = Boolean(collection);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) { setError('Name is required.'); return; }
    setError('');
    onSubmit({ name: name.trim(), description: description.trim() || undefined });
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit} noValidate>
      {isEdit && <h2 className={styles.heading}>Edit Collection</h2>}
      {error && <p className={styles.error} role="alert">{error}</p>}
      <div className={styles.field}>
        <label htmlFor="col-name">Name <span className={styles.required}>*</span></label>
        <input
          id="col-name"
          value={name}
          onChange={(e) => { setName(e.target.value); if (error) setError(''); }}
          className={error ? styles.inputError : undefined}
          aria-invalid={error ? 'true' : undefined}
        />
      </div>
      <div className={styles.field}>
        <label htmlFor="col-desc">Description</label>
        <textarea id="col-desc" rows={3} value={description} onChange={(e) => setDescription(e.target.value)} />
      </div>
      <div className={styles.actions}>
        <Button type="submit" disabled={saving}>{saving ? 'Saving...' : isEdit ? 'Save Changes' : 'Create'}</Button>
        <Button variant="secondary" onClick={onCancel} disabled={saving}>Cancel</Button>
      </div>
    </form>
  );
}
