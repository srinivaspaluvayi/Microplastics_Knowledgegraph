import ollama
import json
import os

MODEL_NAME1 = "alibayram/medgemma"
MODEL_NAME2 = "llama3.2:latest" 


def get_entities():
  with open("../mappings/entities/entities.json", "r", encoding="utf-8") as f:
    raw_nodes = json.load(f)
  return raw_nodes

def get_relationships():
  with open("../mappings/relations/relations.json", "r", encoding="utf-8") as f:
    raw_relationships = json.load(f)
  return raw_relationships

def get_data():
  with open("../extraction/data_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)
  return data

def get_prompt(raw_nodes, raw_relationships, abstract):
  prompt = f"""
  As a scientific knowledge extraction specialist, your objective is to convert microplastics research data into a formal knowledge graph representation.

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
  1. Using ONLY evidence from the abstract, infer the most plausible, specific scientific instance(s) for each node template (e.g., "Polyethylene", "PET", "Spring Water").
  2. You MAY also create new nodes or relationship types if you find additional scientific entities or relations clearly described in the abstract, beyond the provided templates.
  3. For node features, fill in only those that are actually stated or can be confidently inferred from the abstract.
  
  Follow these instructions carefully:
    - Do NOT provide any greetings, explanations, or additional commentary.
    - Only output a single JSON object strictly following this format:

    {{
      "nodes": [
        {{"id": "...", "type": "...", "label": "...", "attributes": {{ ... }} }},
        ...
      ],
      "relationships": [
        {{"source": "...", "relation_type": "...", "target": "..."}},
        ...
      ]
    }}

  DO NOT invent nodes or relations without direct evidence in the abstract. DO NOT repeat the input—only provide the output JSON.
  """

  return prompt

def get_chunk_text(text, max_length=1000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        current_chunk.append(word)
        current_length += 1
        if current_length >= max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def write_output(response_text, index, MODEL_NAME):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script file
    directory = os.path.join(base_dir, "data_all",MODEL_NAME)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    output_filename = os.path.join(directory, f"output_{index+1}.txt")
    
    with open(output_filename, "w", encoding="utf-8", newline="\n") as f:
        f.write(response_text)


def execute_llm(prompt_chunks, MODEL_NAME):
  response_text = ""
  for chunk in prompt_chunks:
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=chunk,
        stream=False
    )
    response_text += response['response']
  return response_text

def process_data(MODEL_NAME):
  data = get_data()
  entities = get_entities()
  relationships = get_relationships()

  i=0
  for entry in data:
    title = entry.get("title", "")
    abstract = entry.get("abstract", "")
    prompt = get_prompt(entities, relationships, abstract)
    chunk_text = get_chunk_text(prompt)
    response_text = execute_llm(chunk_text, MODEL_NAME)
    write_output(response_text, i, MODEL_NAME)
    i+=1
    print(f"Processed entry {i}")

#process_data(MODEL_NAME1)
process_data(MODEL_NAME2)

