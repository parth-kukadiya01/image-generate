/**
 * src/api/index.js
 * ────────────────
 * Single import point for all API modules.
 *
 * Usage:
 *   import { fetchCategories, generateImages, startBulkGeneration, getBulkStatus } from './api';
 */
export { fetchCategories }                               from './categories';
export { generateImages }                                from './generate';
export { startBulkGeneration, getBulkStatus }            from './bulk';
export { downloadSessionZip, downloadBulkZip }           from './download';
export { fetchComboFlows, generateCombo }                from './combo';
export { default as apiClient, API_BASE }                from './client';
