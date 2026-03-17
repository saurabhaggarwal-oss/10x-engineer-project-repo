import { useState, useEffect, useCallback } from 'react';
import { getPrompts, getPrompt, createPrompt, updatePrompt, deletePrompt } from './api/prompts';
import { getCollections, getCollection, createCollection, updateCollection, deleteCollection } from './api/collections';
import Layout from './components/layout/Layout';
import Sidebar from './components/layout/Sidebar';
import SearchBar from './components/shared/SearchBar';
import Modal from './components/shared/Modal';
import Button from './components/shared/Button';
import PromptList from './components/prompts/PromptList';
import PromptDetail from './components/prompts/PromptDetail';
import PromptForm from './components/prompts/PromptForm';
import CollectionList from './components/collections/CollectionList';
import CollectionDetail from './components/collections/CollectionDetail';
import CollectionForm from './components/collections/CollectionForm';
import styles from './App.module.css';

export default function App() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [promptsLoading, setPromptsLoading] = useState(true);
  const [promptsError, setPromptsError] = useState(null);
  const [collectionsLoading, setCollectionsLoading] = useState(true);
  const [collectionsError, setCollectionsError] = useState(null);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [selectedCollection, setSelectedCollection] = useState(null);
  const [activeCollectionId, setActiveCollectionId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [saving, setSaving] = useState(false);
  const [collectionSearch, setCollectionSearch] = useState('');
  const [allPrompts, setAllPrompts] = useState([]);

  // pages: prompts, collections, prompt-detail, prompt-create, prompt-edit,
  //        collection-detail, collection-edit, collection-prompts
  const [page, setPage] = useState('prompts');
  const [showCollectionForm, setShowCollectionForm] = useState(false);

  const fetchPrompts = useCallback(async (collectionId) => {
    setPromptsLoading(true);
    setPromptsError(null);
    try {
      const params = {};
      if (collectionId) params.collection_id = collectionId;
      if (searchQuery) params.search = searchQuery;
      const data = await getPrompts(params);
      setPrompts(data.prompts);
    } catch (err) {
      setPromptsError(err.message);
    } finally {
      setPromptsLoading(false);
    }
  }, [searchQuery]);

  const fetchCollections = useCallback(async () => {
    setCollectionsLoading(true);
    setCollectionsError(null);
    try {
      const data = await getCollections();
      setCollections(data.collections);
    } catch (err) {
      setCollectionsError(err.message);
    } finally {
      setCollectionsLoading(false);
    }
  }, []);

  const fetchAllPrompts = useCallback(async () => {
    try {
      const data = await getPrompts({});
      setAllPrompts(data.prompts);
    } catch { /* ignore */ }
  }, []);

  useEffect(() => { fetchCollections(); }, [fetchCollections]);
  useEffect(() => { fetchAllPrompts(); }, [fetchAllPrompts]);

  useEffect(() => {
    if (page === 'prompts') fetchPrompts(null);
    if (page === 'collection-prompts' && activeCollectionId) fetchPrompts(activeCollectionId);
  }, [page, activeCollectionId, fetchPrompts]);

  const handleNavigate = (target) => {
    setSearchQuery('');
    setCollectionSearch('');
    setSelectedPrompt(null);
    setSelectedCollection(null);
    setActiveCollectionId(null);
    setPage(target);
  };

  const handleSelectCollection = async (id) => {
    try {
      const data = await getCollection(id);
      setSelectedCollection(data);
      setActiveCollectionId(id);
      setPage('collection-detail');
    } catch (err) {
      setCollectionsError(err.message);
    }
  };

  const handleViewCollectionPrompts = () => {
    setPage('collection-prompts');
    fetchPrompts(activeCollectionId);
  };

  const handleSelectPrompt = async (id) => {
    try {
      const data = await getPrompt(id);
      setSelectedPrompt(data);
      setPage('prompt-detail');
    } catch (err) {
      setPromptsError(err.message);
    }
  };

  const handleCreatePrompt = async (formData) => {
    setSaving(true);
    try {
      await createPrompt(formData);
      setPage(activeCollectionId ? 'collection-prompts' : 'prompts');
      fetchPrompts(activeCollectionId);
      fetchAllPrompts();
    } catch (err) {
      setPromptsError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleUpdatePrompt = async (formData) => {
    setSaving(true);
    try {
      const updated = await updatePrompt(selectedPrompt.id, formData);
      setSelectedPrompt(updated);
      setPage('prompt-detail');
      fetchPrompts(activeCollectionId);
      fetchAllPrompts();
    } catch (err) {
      setPromptsError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDeletePrompt = async () => {
    try {
      await deletePrompt(selectedPrompt.id);
      setPage(activeCollectionId ? 'collection-prompts' : 'prompts');
      setSelectedPrompt(null);
      fetchPrompts(activeCollectionId);
      fetchAllPrompts();
    } catch (err) {
      setPromptsError(err.message);
    }
  };

  const handleCreateCollection = async (formData) => {
    setSaving(true);
    try {
      await createCollection(formData);
      setShowCollectionForm(false);
      fetchCollections();
    } catch (err) {
      setCollectionsError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleUpdateCollection = async (formData) => {
    setSaving(true);
    try {
      const updated = await updateCollection(selectedCollection.id, formData);
      setSelectedCollection(updated);
      setPage('collection-detail');
      fetchCollections();
    } catch (err) {
      setCollectionsError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteCollection = async (id) => {
    try {
      await deleteCollection(id);
      if (page === 'collection-detail') {
        setSelectedCollection(null);
        setActiveCollectionId(null);
        setPage('collections');
      }
      fetchCollections();
      fetchAllPrompts();
    } catch (err) {
      setCollectionsError(err.message);
    }
  };

  const collectionName = (id) => collections.find((c) => c.id === id)?.name;

  const promptCountMap = allPrompts.reduce((acc, p) => {
    if (p.collection_id) acc[p.collection_id] = (acc[p.collection_id] || 0) + 1;
    return acc;
  }, {});

  const filteredCollections = collectionSearch
    ? collections.filter((c) => c.name.toLowerCase().includes(collectionSearch.toLowerCase()))
    : collections;

  const sidebarActivePage = ['collections', 'collection-detail', 'collection-edit', 'collection-prompts'].includes(page)
    ? 'collections' : 'prompts';

  const sidebar = (
    <Sidebar activePage={sidebarActivePage} onNavigate={handleNavigate} />
  );

  return (
    <Layout sidebar={sidebar}>
      {/* Collections list */}
      {page === 'collections' && (
        <>
          <div className={styles.pageHeader}>
            <h1 className={styles.pageTitle}>Collections</h1>
            <Button onClick={() => setShowCollectionForm(true)}>+ New Collection</Button>
          </div>
          <div className={styles.searchRow}>
            <SearchBar value={collectionSearch} onChange={setCollectionSearch} />
          </div>
          <CollectionList
            collections={filteredCollections}
            promptCountMap={promptCountMap}
            onSelect={handleSelectCollection}
            onDelete={handleDeleteCollection}
            loading={collectionsLoading}
            error={collectionsError}
          />
        </>
      )}

      {/* Collection detail */}
      {page === 'collection-detail' && selectedCollection && (
        <CollectionDetail
          collection={selectedCollection}
          promptCount={promptCountMap[selectedCollection.id] || 0}
          onEdit={() => setPage('collection-edit')}
          onDelete={() => handleDeleteCollection(selectedCollection.id)}
          onViewPrompts={handleViewCollectionPrompts}
          onBack={() => setPage('collections')}
        />
      )}

      {/* Collection edit */}
      {page === 'collection-edit' && selectedCollection && (
        <CollectionForm
          collection={selectedCollection}
          onSubmit={handleUpdateCollection}
          onCancel={() => setPage('collection-detail')}
          saving={saving}
        />
      )}

      {/* Collection prompts */}
      {page === 'collection-prompts' && (
        <>
          <div className={styles.pageHeader}>
            <div>
              <button className={styles.backLink} onClick={() => setPage('collection-detail')}>← {collectionName(activeCollectionId) || 'Collection'}</button>
              <h1 className={styles.pageTitle}>Prompts</h1>
            </div>
            <Button onClick={() => setPage('prompt-create')}>+ New Prompt</Button>
          </div>
          <div className={styles.searchRow}>
            <SearchBar value={searchQuery} onChange={setSearchQuery} />
          </div>
          <PromptList
            prompts={prompts}
            collections={collections}
            onSelectPrompt={handleSelectPrompt}
            loading={promptsLoading}
            error={promptsError}
            onRetry={() => fetchPrompts(activeCollectionId)}
            emptyMessage="No prompts in this collection yet."
          />
        </>
      )}

      {/* Prompts list */}
      {page === 'prompts' && (
        <>
          <div className={styles.pageHeader}>
            <h1 className={styles.pageTitle}>Prompts</h1>
            <Button onClick={() => setPage('prompt-create')}>+ New Prompt</Button>
          </div>
          <div className={styles.searchRow}>
            <SearchBar value={searchQuery} onChange={setSearchQuery} />
          </div>
          <PromptList
            prompts={prompts}
            collections={collections}
            onSelectPrompt={handleSelectPrompt}
            loading={promptsLoading}
            error={promptsError}
            onRetry={() => fetchPrompts(null)}
            emptyMessage={
              searchQuery
                ? `No prompts matching "${searchQuery}".`
                : 'No prompts yet. Create your first prompt!'
            }
          />
        </>
      )}

      {/* Prompt detail */}
      {page === 'prompt-detail' && selectedPrompt && (
        <PromptDetail
          prompt={selectedPrompt}
          collectionName={collectionName(selectedPrompt.collection_id)}
          onEdit={() => setPage('prompt-edit')}
          onDelete={handleDeletePrompt}
          onBack={() => setPage(activeCollectionId ? 'collection-prompts' : 'prompts')}
        />
      )}

      {/* Create prompt */}
      {page === 'prompt-create' && (
        <PromptForm
          collections={collections}
          onSubmit={handleCreatePrompt}
          onCancel={() => setPage(activeCollectionId ? 'collection-prompts' : 'prompts')}
          saving={saving}
        />
      )}

      {/* Edit prompt */}
      {page === 'prompt-edit' && selectedPrompt && (
        <PromptForm
          prompt={selectedPrompt}
          collections={collections}
          onSubmit={handleUpdatePrompt}
          onCancel={() => setPage('prompt-detail')}
          saving={saving}
        />
      )}

      <Modal isOpen={showCollectionForm} onClose={() => setShowCollectionForm(false)} title="New Collection">
        <CollectionForm
          onSubmit={handleCreateCollection}
          onCancel={() => setShowCollectionForm(false)}
          saving={saving}
        />
      </Modal>
    </Layout>
  );
}
