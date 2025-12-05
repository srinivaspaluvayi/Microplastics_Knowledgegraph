const fs = require('fs');
const path = require('path');

/**
 * Loads and transforms papers data from JSON file
 * @returns {Object} Object containing papers, entitiesFull, relationshipsFull, and knowledgeGraphs
 */
function loadPapersData() {
  const dataPath = path.join(__dirname, '..', 'data', 'papers_data.json');
  let papersDataObj = {};

  try {
    const rawData = fs.readFileSync(dataPath, 'utf8');
    papersDataObj = JSON.parse(rawData);
  } catch (error) {
    console.error('Error loading papers data:', error.message);
    papersDataObj = {};
  }

  // Convert object to array of [title, paperData] entries
  const papersEntries = Object.entries(papersDataObj);

  // Transform JSON data to match application structure
  const papers = papersEntries.map(([title, paper], index) => ({
    id: index + 1,
    title: title || `Paper ${index + 1}`
  }));

  const entitiesFull = {}; // Full node data for detailed views
  const relationshipsFull = {}; // Raw relationship data for table view
  const knowledgeGraphs = {};

  papersEntries.forEach(([title, paper], index) => {
    const paperId = index + 1;
    
    // Store full node data
    entitiesFull[paperId] = paper.nodes || [];
    
    // Store raw relationship data
    relationshipsFull[paperId] = paper.relationships || [];
    
    // Transform nodes and relationships to knowledge graph format
    knowledgeGraphs[paperId] = {
      nodes: (paper.nodes || []).map(node => ({
        id: node.id,
        type: node.type
      })),
      edges: (paper.relationships || []).map(rel => ({
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

