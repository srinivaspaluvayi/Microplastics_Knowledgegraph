const fs = require('fs');
const path = require('path');

/**
 * Loads and transforms papers data from JSON file
 * @returns {Object} Object containing papers, entitiesFull, relationshipsFull, and knowledgeGraphs
 */
function loadPapersData() {
  const dataPath = path.join(__dirname, '..', 'data', 'papers_data.json');
  let papersData = [];

  try {
    const rawData = fs.readFileSync(dataPath, 'utf8');
    papersData = JSON.parse(rawData);
  } catch (error) {
    console.error('Error loading papers data:', error.message);
    papersData = [];
  }

  // Transform JSON data to match application structure
  const papers = papersData.map((paper, index) => ({
    id: index + 1,
    title: paper.Title || `Paper ${index + 1}`
  }));

  const entitiesFull = {}; // Full node data for detailed views
  const relationshipsFull = {}; // Raw relationship data for table view
  const knowledgeGraphs = {};

  papersData.forEach((paper, index) => {
    const paperId = index + 1;
    
    // Store full node data
    entitiesFull[paperId] = paper.nodes;
    
    // Store raw relationship data
    relationshipsFull[paperId] = paper.relationships;
    
    // Transform nodes and relationships to knowledge graph format
    knowledgeGraphs[paperId] = {
      nodes: paper.nodes.map(node => ({
        id: node.id,
        type: node.type
      })),
      edges: paper.relationships.map(rel => ({
        from: rel.source,
        to: rel.target,
        label: rel.relation_type
      }))
    };
  });

  return {
    papers,
    entitiesFull,
    relationshipsFull,
    knowledgeGraphs
  };
}

module.exports = { loadPapersData };

