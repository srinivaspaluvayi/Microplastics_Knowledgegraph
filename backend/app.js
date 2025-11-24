const express = require('express');
const { loadPapersData } = require('./services/dataLoader');
const { getNodeDisplayName } = require('./utils/nodeHelpers');
const { assignNodeTypeColors, formatEdgeLabel } = require('./utils/graphHelpers');
const { createPaperRoutes } = require('./routes/paperRoutes');
const { createApiRoutes } = require('./routes/apiRoutes');
const { SERVER, PAGINATION } = require('./config/constants');
const { securityHeaders, errorHandler } = require('./middleware/security');

const app = express();

// Load and transform papers data
const data = loadPapersData();

// Security middleware - must be before routes
app.use(securityHeaders);

// Configure Express
app.set('view engine', 'ejs');
app.use(express.static('public'));

// Disable X-Powered-By header
app.disable('x-powered-by');

// Home route with pagination
app.get('/', (req, res) => {
  const { validatePageNumber } = require('./utils/validation');
  const totalPapers = data.papers.length;
  const totalPages = Math.ceil(totalPapers / PAGINATION.PAPERS_PER_PAGE);
  const currentPage = validatePageNumber(req.query.page, totalPages);
  
  const startIndex = (currentPage - 1) * PAGINATION.PAPERS_PER_PAGE;
  const endIndex = startIndex + PAGINATION.PAPERS_PER_PAGE;
  const papersForPage = data.papers.slice(startIndex, endIndex);
  
  res.render('index', { 
    papers: papersForPage,
    currentPage,
    totalPages,
    totalPapers,
    papersPerPage: PAGINATION.PAPERS_PER_PAGE
  });
});

// Register routes
createPaperRoutes(app, data, { getNodeDisplayName }, { assignNodeTypeColors, formatEdgeLabel });
createApiRoutes(app, data, { getNodeDisplayName });

// Error handler (must be last)
app.use(errorHandler);

app.listen(SERVER.PORT, () => {
  console.log(`Server running at http://localhost:${SERVER.PORT}`);
});
