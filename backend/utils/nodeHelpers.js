/**
 * Utility functions for working with nodes
 */

/**
 * Gets display name from node (checks name, label, or fields with 'label'/'class' in key)
 * @param {Object} node - The node object
 * @param {string} fallbackId - Fallback ID if no name/label found
 * @returns {string} Display name for the node
 */
function getNodeDisplayName(node, fallbackId) {
  if (!node) return fallbackId;
  
  // First check for 'name' field
  if (node.name !== undefined && node.name !== null) {
    return node.name;
  }
  
  // Then check for 'label' field
  if (node.label !== undefined && node.label !== null) {
    return node.label;
  }
  
  // Check for any field that has 'label' in its key name (e.g., 'pathway_label')
  for (const key in node) {
    if (key.includes('label') && node[key] !== undefined && node[key] !== null) {
      return node[key];
    }
  }
  
  // Check for any field that has 'class' in its key name (e.g., 'method_class')
  for (const key in node) {
    if (key.includes('class') && node[key] !== undefined && node[key] !== null) {
      return node[key];
    }
  }
  
  return fallbackId;
}

module.exports = { getNodeDisplayName };

