/**
 * Generate API
 * POST /api/generate
 * Single-product image generation (Studio & Social modes).
 */
import apiClient from './client';

/**
 * Generate jewelry images for a single product.
 *
 * @param {object} params
 * @param {string}        params.category       - Jewelry category key (ring, necklace, …)
 * @param {File|null}     params.file           - Reference image file
 * @param {string|null}   params.imageUrl       - Direct URL to a reference image
 * @param {string}        [params.productId]    - Product / session ID (used as output folder)
 * @param {string[]}      [params.selectedShots]- Shot keys to force specific angles
 * @param {string}        [params.mode]         - "standard" | "social"
 *
 * @returns {{ status: string, product_id: string, session_id: string, images: Array }}
 */
export async function generateImages({
  category,
  file,
  imageUrl,
  productId,
  selectedShots = [],
  mode = 'standard',
}) {
  const fd = new FormData();
  fd.append('category', category);
  fd.append('mode', mode);

  if (file)           fd.append('file', file);
  if (imageUrl)       fd.append('image_url', imageUrl);
  if (productId)      fd.append('product_id', productId);
  if (selectedShots.length > 0) fd.append('selected_shots', selectedShots.join(','));

  const res = await apiClient.post('/api/generate', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}
