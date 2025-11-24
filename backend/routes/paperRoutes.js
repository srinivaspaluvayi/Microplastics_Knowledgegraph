/**
 * Routes for paper-related pages
 */

const { GRAPH, COLORS } = require('../config/constants');
const { validatePaperId } = require('../utils/validation');

function createPaperRoutes(app, data, { getNodeDisplayName }, { assignNodeTypeColors, formatEdgeLabel }) {
  const { papers, entitiesFull, relationshipsFull, knowledgeGraphs } = data;
  const maxPaperId = papers.length;
  
  // Helper function to find paper by ID
  const findPaper = (paperId) => papers.find(p => p.id === paperId);
  
  // Helper function to validate paper exists
  const validatePaper = (paperId, res) => {
    const validatedId = validatePaperId(paperId, maxPaperId);
    if (!validatedId) {
      res.status(404).send('Paper not found');
      return null;
    }
    
    const paper = findPaper(validatedId);
    if (!paper) {
      res.status(404).send('Paper not found');
      return null;
    }
    return { paper, paperId: validatedId };
  };
  
  // Paper detail page
  app.get('/paper/:paperId', (req, res) => {
    const result = validatePaper(req.params.paperId, res);
    if (!result) return;
    
    const { paper, paperId } = result;
    
    res.render('paper', { 
      paper, 
      paperId,
      hasEntities: entitiesFull[paperId]?.length > 0,
      hasRelationships: relationshipsFull[paperId]?.length > 0,
      hasKnowledgeGraph: knowledgeGraphs[paperId]?.nodes.length > 0
    });
  });

  // Entities view
  app.get('/paper/:paperId/entities', (req, res) => {
    const result = validatePaper(req.params.paperId, res);
    if (!result) return;
    
    const { paper, paperId } = result;
    
    res.render('entities', { 
      paper, 
      paperId,
      nodes: entitiesFull[paperId] || []
    });
  });

  // Relationships view
  app.get('/paper/:paperId/relationships', (req, res) => {
    const result = validatePaper(req.params.paperId, res);
    if (!result) return;
    
    const { paper, paperId } = result;
    
    const rawRelationships = relationshipsFull[paperId] || [];
    const nodes = entitiesFull[paperId] || [];
    
    const relationshipsWithLabels = rawRelationships.map(rel => ({
      source: rel.source,
      sourceLabel: getNodeDisplayName(nodes.find(n => n.id === rel.source), rel.source),
      relationType: rel.relation_type,
      target: rel.target,
      targetLabel: getNodeDisplayName(nodes.find(n => n.id === rel.target), rel.target)
    }));
    
    res.render('relationships', { 
      paper, 
      paperId,
      relationships: relationshipsWithLabels
    });
  });

  // Knowledge graph view
  app.get('/paper/:paperId/knowledgegraph', (req, res) => {
    const result = validatePaper(req.params.paperId, res);
    if (!result) return;
    
    const { paper, paperId } = result;
    
    const graphData = knowledgeGraphs[paperId] || { nodes: [], edges: [] };
    const nodes = entitiesFull[paperId] || [];
    
    // Get unique node types
    const uniqueNodeTypes = new Set(nodes.filter(n => n.type).map(n => n.type));
    const typeColors = assignNodeTypeColors(uniqueNodeTypes);
    
    // Transform nodes for vis-network
    const visNodes = graphData.nodes.map(node => {
      const fullNode = nodes.find(n => n.id === node.id) || node;
      return {
        id: node.id,
        label: getNodeDisplayName(fullNode, node.id),
        type: fullNode.type || node.type,
        color: typeColors[fullNode.type || node.type] || COLORS.DEFAULT_NODE
      };
    });
    
    // Create node data map for tooltips
    const nodeDataMap = Object.fromEntries(nodes.map(node => [node.id, node]));
    
    // Transform edges for vis-network
    const visEdges = graphData.edges.map(edge => ({
      from: edge.from,
      to: edge.to,
      label: formatEdgeLabel(edge.label),
      arrows: {
        to: {
          enabled: true,
          scaleFactor: GRAPH.EDGE.ARROW_SCALE,
          type: 'arrow'
        }
      },
      color: { color: COLORS.EDGE, highlight: COLORS.EDGE_HIGHLIGHT },
      width: GRAPH.EDGE.WIDTH
    }));
    
    res.render('knowledgegraph', {
      paper,
      paperId,
      nodes: visNodes,
      edges: visEdges,
      nodeDataMap,
      nodeTypesList: Array.from(uniqueNodeTypes).sort(),
      typeColors
    });
  });
}

module.exports = { createPaperRoutes };

