import pdfplumber
import xml.etree.ElementTree as ET
import os
import json

xml_folder = "../collection/"

def list_xml_files(folder_path):
    xml_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.xml')]
    return xml_files

def extract_title_abstract_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    abstract_text = ""
    # Find the first 'abstract' element anywhere in the XML tree
    for abstract in root.findall('.//abstract'):
        texts = [elem.text.strip() for elem in abstract.iter() if elem.text]
        abstract_text = " ".join(texts)
        break  # Only extract first abstract

    for article_title in root.findall('.//article-title'):
        texts = [elem.text.strip() for elem in article_title.iter() if elem.text]
        article_title_text = " ".join(texts)
        break  # Only extract first article-title
    
    return article_title_text, abstract_text

def extract_title_abstract():
    xml_file_list = list_xml_files(xml_folder)
    data = []
    for file in xml_file_list:
        file_path = os.path.join(xml_folder, file)
        title, abstract = extract_title_abstract_xml(file_path)
        data.append({
            "title": title,
            "abstract": abstract
        })
    return data

def execute_extraction():
    data = extract_title_abstract()
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Extraction completed and data saved to data.json")

execute_extraction()

        


