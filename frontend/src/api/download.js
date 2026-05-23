/**
 * Download API
 * GET /api/download-zip/{sessionId}      — single session ZIP
 * GET /api/download-zip-bulk/{jobId}     — full bulk-job ZIP
 */
import { API_BASE } from './client';

/**
 * Trigger a browser ZIP download for a single-session (Studio / Social mode).
 * @param {string} sessionId  - product_id / folder name
 * @param {string} [filename] - suggested filename (without .zip)
 */
export function downloadSessionZip(sessionId, filename) {
  const name = filename || sessionId;
  const url  = `${API_BASE}/api/download-zip/${encodeURIComponent(sessionId)}`;
  _triggerDownload(url, `${name}.zip`);
}

/**
 * Trigger a browser ZIP download for an entire bulk job.
 * @param {string} jobId
 */
export function downloadBulkZip(jobId) {
  const url = `${API_BASE}/api/download-zip-bulk/${encodeURIComponent(jobId)}`;
  _triggerDownload(url, `bulk_${jobId}.zip`);
}

/** Create a temporary <a> tag and click it to trigger the download. */
function _triggerDownload(url, filename) {
  const a      = document.createElement('a');
  a.href       = url;
  a.download   = filename;
  a.target     = '_blank';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
