import json
import os
from dotenv import load_dotenv
from openai import OpenAI

MODEL_NAME1 = "gpt-4o-mini"
load_dotenv(override=True)


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

def get_prompt(raw_nodes, raw_relationships, data):
  system_prompt = f"""
  As a scientific knowledge extraction specialist, your objective is to convert microplastics research data into a formal knowledge graph representation.

  Example 1:
  Given:convert the following scientific data into a knowledge graph representation.
  - Scientific data:
  'Polyethylene and polystyrene microplastics have been detected in Mediterranean Sea water. European seabass (Dicentrarchus labrax) is known to ingest these microplastics.'

  Output JSON:
  {{
    "nodes": [
      {{"id": "polymer_1", "type": "Polymer", "label": "Polyethylene", "attributes": {{"chemical_structure": "[-CH2-CH2-]n"}}}},
      {{"id": "organism_1", "type": "Organism", "label": "European seabass", "attributes": {{"species_name": "Dicentrarchus labrax"}}}},
      {{"id": "polymer_2", "type": "Polymer", "label": "Polystyrene"}},
      {{"id": "environment_1", "type": "Environment", "label": "Mediterranean Sea"}}
    ],
    "relationships": [
      {{"source": "organism_1", "relation_type": "ingests", "target": "polymer_1"}},
      {{"source": "organism_1", "relation_type": "ingests", "target": "polymer_2"}},
      {{"source": "polymer_1", "relation_type": "found_in", "target": "environment_1"}},
      {{"source": "polymer_2", "relation_type": "found_in", "target": "environment_1"}}
    ]
  }}

  Instructions:
  1. Using ONLY evidence from the scientific data provided by the user, infer the most plausible, specific scientific instance(s) for each node template (e.g., "Polyethylene", "PET", "Spring Water").
  2. You MAY also create new nodes or relationship types if you find additional scientific entities or relations clearly described in the scientific data, beyond the provided templates.
  3. For node features, fill in only those that are actually stated or can be confidently inferred from the scientific data.
  4. DO invent nodes or relations only with direct evidence in the data. 

  Follow these instructions carefully:
    - Do NOT provide any greetings, explanations, or additional commentary.
    - Only output a single JSON object strictly following this format:

    {{
      "nodes": [
        {{"id": "...", "type": "...", "label": "...", "attributes": {{ ... }} }},
      ],
      "relationships": [
        {{"source": "...", "relation_type": "...", "target": "..."}},
      ]
    }}

  """

  user_prompt = f"""  Now you are given the following input and Using the nodes and relationships templates below, convert the following scientific data into a knowledge graph representation:
  - Node types and feature templates:
  {json.dumps(raw_nodes, separators=(',', ':'))}

  - Relationship templates:
  {json.dumps(raw_relationships, separators=(',', ':'))}
  - Scientific data:
  {json.dumps(data, separators=(',', ':'))}
  """

  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
    ]
  return messages

def write_output(response_text, index, MODEL_NAME):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script file
    directory = os.path.join(base_dir, "data_all",MODEL_NAME)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    output_filename = os.path.join(directory, f"output_{index+1}.json")


    with open(os.path.join(directory, f"output_{index+1}.txt"), "w", encoding="utf-8", newline="\n") as f:
      f.write(response_text)

def execute_llm(client, messages, MODEL_NAME):
  response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
    temperature=0,
    max_tokens=4096
  )
  return response.choices[0].message.content


def process_data(MODEL_NAME):
  data = get_data()
  entities = get_entities()
  relationships = get_relationships()
  client = OpenAI()
  i=0
  for entry in data:
    messages = get_prompt(entities, relationships, entry)
    response_text = execute_llm(client, messages, MODEL_NAME)
    write_output(response_text, i, MODEL_NAME)
    i+=1
    print(f"Processed entry {i}")

process_data(MODEL_NAME1)

