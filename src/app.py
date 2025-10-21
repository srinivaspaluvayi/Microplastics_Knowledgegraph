import ollama
import json
import re

MODEL_NAME = "llama3.2:latest" 

# --- Example input: general node and relationship specs ---


with open("../mappings/entities/entities.json", "r", encoding="utf-8") as f:
    raw_nodes = json.load(f)

with open("../mappings/relations/relations.json", "r", encoding="utf-8") as f:
    raw_relationships = json.load(f)

with open("../extraction//data.txt", "r", encoding="utf-8") as f:
  abstract = f.read()

prompt = f"""
You are helping build a microplastics knowledge graph from scientific data.
Given:
- Node types and feature templates: {json.dumps(raw_nodes, indent=2)}
- Relationship templates: {json.dumps(raw_relationships, indent=2)}
- Scientific abstract: {abstract}

Instructions:
1. Using ONLY evidence from the abstract, infer the most plausible, specific scientific instance(s) for each node (e.g. "Polyethylene", "PET", "Spring Water").
2. For node features, fill in only those that are actually stated or can be confidently inferred from the abstract.
3. Expand any relationship template into a real, explicit relationship between actual named entities in the abstract.
4. Your output must be a single JSON object in the format:
{{
  "nodes": [
    {{"id": "...", "type": "...", "label": "...", "attributes": {{ ...only concrete features from the abstract... }} }},
    ...
  ],
  "relationships": [
    {{"source": "...", "relation_type": "...", "target": "..."}}
    ...
  ]
}}
DO NOT invent nodes or relations without evidence in the abstract. DO NOT repeat the input—only give the single output JSON.
"""
response = ollama.generate(
    model=MODEL_NAME,
    prompt=prompt,
    stream=False
)

response_text = response['response']

with open("output.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write(response_text)
