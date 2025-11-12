import pandas as pd
import json

# Read columns from Excel
df = pd.read_excel('../collection/project_papers.xlsx', usecols=['Title', 'Abstract Note'])

# Build list of dicts as needed for your JSON
records = []
for _, row in df.iterrows():
    # Handle missing/NaN gracefully
    title = str(row['Title']) if not pd.isna(row['Title']) else ""
    abstract = str(row['Abstract Note']) if not pd.isna(row['Abstract Note']) else ""
    if title and abstract:
        records.append({'title': title, 'abstract': abstract})

# Write to JSON file (pretty-printed)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=4, ensure_ascii=False)

print('JSON saved!')
