import os
import json

def merge_datasets():
    """
    Merges all .json files from the 'dataset' directory into a single 
    .json and a .jsonl file.
    """
    source_dir = 'dataset'
    output_json = 'merged_dataset.json'
    output_jsonl = 'merged_dataset.jsonl'
    
    merged_data = []

    print(f"Starting merge from directory: {source_dir}")

    if not os.path.isdir(source_dir):
        print(f"Error: Directory '{source_dir}' not found.")
        return

    # Recursively walk through the source directory
    for root, _, files in os.walk(source_dir):
        for filename in sorted(files):
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, source_dir)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            merged_data.extend(data)
                            print(f"- Successfully merged {len(data)} samples from {relative_path}")
                        else:
                            print(f"- Warning: {relative_path} does not contain a JSON list. Skipping.")
                except json.JSONDecodeError:
                    print(f"- Warning: Could not decode JSON from {relative_path}. Skipping.")
                except Exception as e:
                    print(f"- Error reading {relative_path}: {e}")

    print(f"\nTotal samples merged: {len(merged_data)}")

    # Write to .json file
    try:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully created merged file: {output_json}")
    except Exception as e:
        print(f"Error writing to {output_json}: {e}")

    # Write to .jsonl file
    try:
        with open(output_jsonl, 'w', encoding='utf-8') as f:
            for entry in merged_data:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        print(f"Successfully created merged file: {output_jsonl}")
    except Exception as e:
        print(f"Error writing to {output_jsonl}: {e}")

if __name__ == '__main__':
    merge_datasets()
