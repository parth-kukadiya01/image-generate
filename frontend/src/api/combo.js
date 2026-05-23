/**
 * Combo Flow API
 * GET  /api/combo-flows              — available preset flows
 * POST /api/combo-generate           — generate all pieces in a combo
 */
import apiClient from './client';

/**
 * Fetch the list of available combo flow presets from the server.
 */
export async function fetchComboFlows() {
  const { data } = await apiClient.get('/api/combo-flows');
  return data; // { flows: { bridal_trio: {...}, classic_set: {...} } }
}

/**
 * Run a full combo-flow generation.
 *
 * @param {object} opts
 * @param {string}   opts.flowId      - 'bridal_trio' | 'classic_set'
 * @param {string}   [opts.productId] - optional folder/session name
 * @param {File[]}   opts.files       - reference image for each piece (in order)
 */
export async function generateCombo({ flowId, productId, files }) {
  const fd = new FormData();
  fd.append('flow_id', flowId);
  if (productId) fd.append('product_id', productId);

  // Attach each file as file_0, file_1, file_2
  files.forEach((file, i) => {
    if (file) fd.append(`file_${i}`, file);
  });

  const { data } = await apiClient.post('/api/combo-generate', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 600_000, // 10 min — each piece takes ~3 min, 3 pieces in parallel
  });
  return data;
}
