/**
 * API routes for JSON endpoints
 */

const { validatePaperId } = require('../utils/validation');
const { createRateLimiter } = require('../middleware/rateLimiter');

// Rate limiter for API endpoints (stricter than general routes)
const apiRateLimiter = createRateLimiter({
  windowMs: 15 * 60 * 1000, // 15 minutes
  maxRequests: 50 // 50 requests per 15 minutes
});

function createApiRoutes(app, { papers, entitiesFull, relationshipsFull, knowledgeGraphs }, { getNodeDisplayName }) {
  const maxPaperId = papers.length;
  
  // JSON API: Get entities for a paper
  app.get('/:paperId/entities', apiRateLimiter, (req, res) => {
    const paperId = validatePaperId(req.params.paperId, maxPaperId);
    if (!paperId) {
      return res.status(404).json({ error: 'Paper not found' });
    }
    
    const nodes = entitiesFull[paperId] || [];
    res.json(nodes.map(node => getNodeDisplayName(node, node.id)));
  });

  // JSON API: Get relationships for a paper
  app.get('/:paperId/relationships', apiRateLimiter, (req, res) => {
    const paperId = validatePaperId(req.params.paperId, maxPaperId);
    if (!paperId) {
      return res.status(404).json({ error: 'Paper not found' });
    }
    
    const rawRelationships = relationshipsFull[paperId] || [];
    const nodes = entitiesFull[paperId] || [];
    
    const readableRelationships = rawRelationships.map(rel => {
      const sourceLabel = getNodeDisplayName(nodes.find(n => n.id === rel.source), rel.source);
      const targetLabel = getNodeDisplayName(nodes.find(n => n.id === rel.target), rel.target);
      return `${rel.relation_type} ${sourceLabel} -> ${targetLabel}`;
    });
    
    res.json(readableRelationships);
  });

  // JSON API: Get knowledge graph for a paper
  app.get('/:paperId/knowledgegraph', apiRateLimiter, (req, res) => {
    const paperId = validatePaperId(req.params.paperId, maxPaperId);
    if (!paperId) {
      return res.status(404).json({ error: 'Paper not found' });
    }
    
    res.json(knowledgeGraphs[paperId] || { nodes: [], edges: [] });
  });
}

module.exports = { createApiRoutes };

