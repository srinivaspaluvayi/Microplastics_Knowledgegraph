import json
import os

def get_data(filepath):
  with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)
  return data

def list_json_files(folder_path):
    json_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith('.json')]
    return json_files

def preprocess_data(data, nodes_all, nodes_all_nums, relations_all):
    entities = data.get("nodes", [])
    relations = data.get("relationships", [])
    node_mappings = {}
    new_entities = []
    new_relations = []

    for entity in entities:
        flag = entity.copy()
        entity_type = entity.get("type", [])

        if entity_type in nodes_all_nums:
            nodes_all_nums[entity_type] += 1
            entity_num = nodes_all_nums[entity_type]
            flag["id"] = f"{entity_type}_{entity_num}"
            node_mappings[entity["id"]] = flag["id"]
            new_entities.append(flag)
        else:
            nodes_all_nums[entity_type] = 1
            flag["id"] = f"{entity_type}_{1}"
            node_mappings[entity["id"]] = flag["id"]
            new_entities.append(flag)
    
    for relation in relations:
        flag = relation.copy()
        source_id = relation["source"]
        target_id = relation["target"]
        flag["source"] = node_mappings[source_id]
        flag["target"] = node_mappings[target_id]
        new_relations.append(flag)
            
    for entity in new_entities:
        entity_type = entity.get("type", [])
        if entity_type not in nodes_all:
            nodes_all[entity_type] = [entity]
        else:
            nodes_all[entity_type].append(entity)
    
    relations_all.extend(new_relations)

def saved_data(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def process_data(folder_path, output_filename):
    json_files = list_json_files(folder_path)

    nodes_all = {}
    nodes_all_nums = {}
    relations_all = []

    for file in json_files:
        data = get_data(file)
        preprocess_data(data, nodes_all, nodes_all_nums, relations_all)
    
    saved_data({"nodes": nodes_all, "relationships": relations_all}, output_filename)

process_data("./data_all/gpt-4o-mini", "gpt-4o-mini.json")

