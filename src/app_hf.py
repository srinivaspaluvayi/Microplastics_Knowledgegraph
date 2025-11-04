import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "aaditya/Llama3-OpenBioLLM-8B"

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

def write_output(response_text, index, MODEL_NAME):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script file
    directory = os.path.join(base_dir, MODEL_NAME)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    output_filename = os.path.join(directory, f"output_{index+1}.txt")
    
    with open(output_filename, "w", encoding="utf-8", newline="\n") as f:
        f.write(response_text)

def chunk_text(text, tokenizer, max_tokens=7000):
  encoded = tokenizer.encode(text)
  chunks = []
  for i in range(0, len(encoded), max_tokens):
      chunk = encoded[i:i+max_tokens]
      decoded_chunk = tokenizer.decode(chunk)
      chunks.append(decoded_chunk)
  return chunks
    
def load_model_and_tokenizer():
  LOCAL_MODEL_PATH = "./local_model/llama_biolm"
  tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH)
  model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL_PATH)
  return model, tokenizer

def execute_llm(prompt_chunks, model, tokenizer, max_new_tokens=1024):
  response_text = ""
  for chunk in prompt_chunks:
    inputs = tokenizer(chunk, return_tensors="pt").to(model.device)
    output_ids = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        temperature=0,
    )
    generated = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    response_text += generated
  return response_text


def process_data(MODEL_NAME):
  data = get_data()
  entities = get_entities()
  relationships = get_relationships()
  model, tokenizer = load_model_and_tokenizer()

  i=0
  for entry in data:
    title = entry.get("title", "")
    abstract = entry.get("abstract", "")
    prompt = get_prompt(entities, relationships, abstract)
    prompt_chunks = chunk_text(prompt, tokenizer)
    response_text = execute_llm(prompt_chunks, model, tokenizer)
    write_output(response_text, i, MODEL_NAME)
    i+=1
    print(f"Processed entry {i}")

process_data(MODEL_NAME)

