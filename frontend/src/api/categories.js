/**
 * Categories API
 * GET /api/categories
 * Returns all jewelry categories and creative/social scenes.
 */
import apiClient from './client';

/**
 * @returns {{ categories: object, social_scenes: Array }}
 */
export async function fetchCategories() {
  const res = await apiClient.get('/api/categories');
  return res.data;
}
