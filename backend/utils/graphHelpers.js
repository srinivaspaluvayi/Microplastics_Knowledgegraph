/**
 * Utility functions for knowledge graph visualization
 */

const { COLOR_PALETTE } = require('../config/constants');

/**
 * Generates a color from a string using hash function
 * @param {string} str - String to generate color from
 * @returns {string} HSL color string
 */
function generateColorFromString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash) % 360;
  return `hsl(${hue}, 65%, 60%)`;
}

/**
 * Assigns colors to node types dynamically
 * @param {Array<string>} nodeTypes - Array of unique node types
 * @returns {Object} Object mapping node types to colors
 */
function assignNodeTypeColors(nodeTypes) {
  const typeColors = {};
  const sortedTypes = Array.from(nodeTypes).sort();
  
  sortedTypes.forEach((nodeType, index) => {
    typeColors[nodeType] = index < COLOR_PALETTE.length 
      ? COLOR_PALETTE[index] 
      : generateColorFromString(nodeType);
  });
  
  return typeColors;
}

/**
 * Formats edge label for display
 * @param {string} label - Raw edge label
 * @returns {string} Formatted label
 */
function formatEdgeLabel(label) {
  let formatted = label.replace(/_/g, ' ');
  formatted = formatted.charAt(0).toUpperCase() + formatted.slice(1);
  return formatted;
}

module.exports = {
  generateColorFromString,
  assignNodeTypeColors,
  formatEdgeLabel
};

