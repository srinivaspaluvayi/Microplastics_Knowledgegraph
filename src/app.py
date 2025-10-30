import ollama
import json
import re

MODEL_NAME = "llama3.2:latest" 


def get_entities():
  with open("../mappings/entities/entities.json", "r", encoding="utf-8") as f:
    raw_nodes = json.load(f)
  return raw_nodes

def get_relationships():
  with open("../mappings/relations/relations.json", "r", encoding="utf-8") as f:
    raw_relationships = json.load(f)
  return raw_relationships

def get_data():
  with open("../extraction/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
  return data

def get_prompt(raw_nodes, raw_relationships, abstract):
  prompt = f"""
    You are helping build a microplastics knowledge graph from scientific data.

    Example 1:
    Given:
    - Node types and feature templates:
    {json.dumps(raw_nodes, indent=2)}
    - Relationship templates:
    {json.dumps(raw_relationships, indent=2)}
    - Scientific abstract:
    'Polyethylene and polystyrene microplastics have been detected in Mediterranean Sea water. European seabass (Dicentrarchus labrax) is known to ingest these microplastics.'

    Output JSON:
    {{
    "nodes": [
    {{"id": "polymer_1", "type": "Polymer", "label": "Polyethylene", "attributes": {{"chemical_structure": "[-CH2-CH2-]n"}}}},
    {{"id": "polymer_2", "type": "Polymer", "label": "Polystyrene", "attributes": {{"chemical_structure": "[-CH2-CH(C6H5)-]n"}}}},
    {{"id": "environment_1", "type": "Environment", "label": "Mediterranean Sea", "attributes": {{"location_name": "Mediterranean Sea"}}}},
    {{"id": "organism_1", "type": "Organism", "label": "European seabass", "attributes": {{"species_name": "Dicentrarchus labrax"}}}}
    ],
    "relationships": [
    {{"source": "organism_1", "relation_type": "ingests", "target": "polymer_1"}},
    {{"source": "organism_1", "relation_type": "ingests", "target": "polymer_2"}},
    {{"source": "polymer_1", "relation_type": "found_in", "target": "environment_1"}},
    {{"source": "polymer_2", "relation_type": "found_in", "target": "environment_1"}}
    ]
    }}

    Example 2:
    Given:
    - Node types and feature templates:
    {json.dumps(raw_nodes, indent=2)}
    - Relationship templates:
    {json.dumps(raw_relationships, indent=2)}
    - Scientific abstract:
    'Microplastics, including PET and PVC, have bioaccumulated in freshwater fish species in the Rhine River.'

    Output JSON:
    {{
    "nodes": [
    {{"id": "polymer_1", "type": "Polymer", "label": "PET", "attributes": {{}}}},
    {{"id": "polymer_2", "type": "Polymer", "label": "PVC", "attributes": {{}}}},
    {{"id": "organism_1", "type": "Organism", "label": "Freshwater fish", "attributes": {{}}}},
    {{"id": "environment_1", "type": "Environment", "label": "Rhine River", "attributes": {{}}}}
    ],
    "relationships": [
    {{"source": "organism_1", "relation_type": "bioaccumulates", "target": "polymer_1"}},
    {{"source": "organism_1", "relation_type": "bioaccumulates", "target": "polymer_2"}},
    {{"source": "polymer_1", "relation_type": "found_in", "target": "environment_1"}},
    {{"source": "polymer_2", "relation_type": "found_in", "target": "environment_1"}}
    ]
    }}

    Now you are given the following input:

    - Node types and feature templates:
    {json.dumps(raw_nodes, indent=2)}

    - Relationship templates:
    {json.dumps(raw_relationships, indent=2)}

    - Scientific abstract:
    {abstract}

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
  return prompt

def write_output(response_text, index):
  output_filename = f"output/output_{index+1}.txt"
  with open(output_filename, "w", encoding="utf-8", newline="\n") as f:
    f.write(response_text)

def execute_llm(prompt):
  response = ollama.generate(
    model=MODEL_NAME,
    prompt=prompt,
    stream=False)
  response_text = response['response']
  return response_text

def process_data():
  data = get_data()
  entities = get_entities()
  relationships = get_relationships()

  i=0
  for entry in data:
    title = entry.get("title", "")
    abstract = entry.get("abstract", "")
    prompt = get_prompt(entities, relationships, abstract)
    response_text = execute_llm(prompt)
    write_output(response_text, i)
    i+=1
    print(f"Processed entry {i}")

process_data()

