import { get, post, put, del } from './client.js';

export function getCollections() {
  return get('/collections');
}

export function getCollection(id) {
  return get(`/collections/${id}`);
}

export function createCollection(data) {
  return post('/collections', data);
}

export function updateCollection(id, data) {
  return put(`/collections/${id}`, data);
}

export function deleteCollection(id) {
  return del(`/collections/${id}`);
}

export function getCollectionVersions(id) {
  return get(`/collections/${id}/versions`);
}

export function getCollectionVersion(id, version) {
  return get(`/collections/${id}/versions/${version}`);
}
