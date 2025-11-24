/**
 * Application constants and configuration
 */

module.exports = {
  // Server configuration
  SERVER: {
    PORT: process.env.PORT || 3000
  },

  // Pagination configuration
  PAGINATION: {
    PAPERS_PER_PAGE: 10
  },

  // Graph visualization configuration
  GRAPH: {
    // Node configuration
    NODE: {
      SIZE: 30,
      FONT_SIZE: 18,
      BORDER_WIDTH: 2
    },
    // Edge configuration
    EDGE: {
      WIDTH: 2.5,
      FONT_SIZE: 14,
      ARROW_SCALE: 1.2
    },
    // Physics configuration
    PHYSICS: {
      STABILIZATION_ITERATIONS: 250,
      SPRING_LENGTH: 200,
      GRAVITATIONAL_CONSTANT: -2000,
      CENTRAL_GRAVITY: 0.1,
      SPRING_CONSTANT: 0.03,
      DAMPING: 0.2,
      AVOID_OVERLAP: 1.2
    },
    // Layout configuration
    LAYOUT: {
      PADDING: 120,
      MIN_ZOOM: 0.1,
      MAX_ZOOM: 2
    }
  },

  // Color palette for node types
  COLOR_PALETTE: [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#8D6E63',
    '#607D8B', '#A1887F', '#90A4AE', '#CE93D8', '#81C784',
    '#FFB74D', '#64B5F6', '#F06292', '#BA68C8', '#4DB6AC'
  ],

  // Default colors
  COLORS: {
    DEFAULT_NODE: '#95A5A6',
    EDGE: '#848484',
    EDGE_HIGHLIGHT: '#0066cc'
  }
};

