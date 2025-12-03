import pdfplumber
import xml.etree.ElementTree as ET
from io import StringIO
import os
import json
import re

xml_folder = "../collection/"

def list_xml_files(folder_path):
    xml_files = [file for file in os.listdir(folder_path) if file.lower().endswith('.xml')]
    return xml_files

def get_full_text(elem):
    """ Recursively extract all text, including tail texts, from an element """
    text = (elem.text or '')
    for child in elem:
        text += get_full_text(child)
        text += (child.tail or '')
    return text

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace undefined entities with their Unicode equivalent or remove them
    content = content.replace('&copy;', '©')

    # Parse the cleaned XML string
    tree = ET.parse(StringIO(content))
    return tree

def extract_sections(file_path, sections):
    """
    Extracts the specified sections text from the XML root.
    :param xml_root: Parsed XML root element
    :param sections: List of section tags or partial titles to search for
    :return: Dictionary with section title as key and extracted text as value
    """
    tree = parse_file(file_path)
    xml_root = tree.getroot()
    extracted_data = {}

    # This example assumes sections are identified by <sec> tags or <title> tags inside the XML.
    # Modify xpath and logic according to your XML schemas.

    # Searching all section titles and matching against requested names
    for sec in xml_root.findall('.//sec'):
        title_element = sec.find('title')
        section_title = title_element.text.lower() if title_element is not None else ""
        for sec_name in sections:
            if sec_name.lower() in section_title:
                # Replace tabs/newlines/multiple spaces with single space, then strip
                cleaned = re.sub(r'[\t\n]+', ' ', get_full_text(sec).strip())
                cleaned = re.sub(r' +', ' ', cleaned)
                cleaned = cleaned.replace('\"', '').replace('“', '').replace('”', '')
                extracted_data[section_title] = cleaned
                break

    # Some XML formats store abstract in a separate tag, so extract separately if needed
    abstract_element = xml_root.find('.//abstract')
    if abstract_element is not None and 'Abstract' in sections:
        texts = [elem.text.strip() for elem in abstract_element.iter() if elem.text]
        extracted_data['Abstract'] = " ".join(texts)
    
    article_title_element = xml_root.find('.//article-title')
    if article_title_element is not None and 'Title' in sections:
        texts = [elem.text.strip() for elem in article_title_element.iter() if elem.text]
        extracted_data['Title'] = " ".join(texts)

    return extracted_data

def extract_all():
    xml_file_list = list_xml_files(xml_folder)
    data = []
    # Sections to extract, adjust names as per your XML files
    sections_to_extract = ['Abstract', 'Introduction', 'Method', 'Methodology', 'Results', 'Conclusion', 'Title', 'Effects']
    for file in xml_file_list:
        file_path = os.path.join(xml_folder, file)
        extracted_content = extract_sections(file_path, sections_to_extract)
        if not extracted_content:
            print(file_path)
        else:
            data.append(extracted_content)
    return data

def execute_extraction_all():
    data = extract_all()
    with open('data_all.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Extraction completed and data saved to data.json")

execute_extraction_all()

        


