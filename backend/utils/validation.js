/**
 * Input validation utilities
 */

/**
 * Validates and sanitizes paperId parameter
 * @param {string|number} paperId - Paper ID to validate
 * @param {number} maxId - Maximum valid paper ID
 * @returns {number|null} Validated paper ID or null if invalid
 */
function validatePaperId(paperId, maxId) {
  // Convert to number
  const id = typeof paperId === 'string' ? parseInt(paperId, 10) : paperId;
  
  // Check if it's a valid number
  if (isNaN(id) || !isFinite(id)) {
    return null;
  }
  
  // Check if it's a positive integer
  if (id <= 0 || !Number.isInteger(id)) {
    return null;
  }
  
  // Check if it's within valid range
  if (maxId && id > maxId) {
    return null;
  }
  
  return id;
}

/**
 * Validates page number parameter
 * @param {string|number} page - Page number to validate
 * @param {number} maxPages - Maximum valid page number
 * @returns {number} Validated page number (defaults to 1)
 */
function validatePageNumber(page, maxPages) {
  const pageNum = typeof page === 'string' ? parseInt(page, 10) : page;
  
  if (isNaN(pageNum) || !isFinite(pageNum) || pageNum < 1 || !Number.isInteger(pageNum)) {
    return 1;
  }
  
  if (maxPages && pageNum > maxPages) {
    return maxPages;
  }
  
  return pageNum;
}

/**
 * Escapes HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
  if (typeof text !== 'string') {
    return String(text);
  }
  
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  
  return text.replace(/[&<>"']/g, m => map[m]);
}

module.exports = {
  validatePaperId,
  validatePageNumber,
  escapeHtml
};

