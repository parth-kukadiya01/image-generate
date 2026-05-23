/**
 * Bulk API
 * POST /api/bulk-generate  — start a bulk job
 * GET  /api/bulk-status/{jobId} — poll job status
 */
import apiClient from './client';

/**
 * Start a bulk image-generation job.
 *
 * @param {object} params
 * @param {string}      params.category  - Default jewelry category for rows that have none
 * @param {File|null}   params.file      - Excel / CSV file
 * @param {string|null} params.url       - Google Sheets URL  or  direct image URL
 *
 * @returns {{ status: string, job_id: string, message: string }}
 */
export async function startBulkGeneration({ category, file, url }) {
  const fd = new FormData();
  fd.append('category', category);
  if (file) fd.append('file', file);
  if (url)  fd.append('url', url);

  const res = await apiClient.post('/api/bulk-generate', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}

/**
 * Poll the status of a running bulk job.
 *
 * @param {string} jobId
 * @returns {{ status: string, progress: string, results: Array, error: string }}
 */
export async function getBulkStatus(jobId) {
  const res = await apiClient.get(`/api/bulk-status/${jobId}`);
  return res.data;
}
