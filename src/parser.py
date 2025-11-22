import os

def get_text_files(folder_path):
    text_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith('.txt')]
    return text_files

def rename_file(folder_path):
    text_files = get_text_files(folder_path)
    for filename in text_files:
        os.rename(filename, filename.replace('.txt', '.json'))

rename_file('./data_all/gpt-4o-mini/')