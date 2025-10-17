## Workflow for Building a Microplastics Knowledge Graph with Neo4j

- **Collect research papers and raw scientific sources.**
- **Extract key information** (entities and relationships) using:
  - Large Language Models (LLMs) or domain-adapted NLP
  - Manual expert curation (if needed)
- **Map each extracted item** to the predefined ontology:
  - Entities become nodes (e.g., Polymer, Sample, Observation, Method)
  - Relationships become edges (e.g., "Sample collected_from EnvironmentalCompartment")
- **Format the structured data** for Neo4j import:
  - Use CSV files (node and edge lists), JSON, or a loading script
- **Import the data into Neo4j** using its bulk loader or Cypher queries
- **Query and analyze your graph** in Neo4j to discover patterns, answer scientific questions, and visualize results

