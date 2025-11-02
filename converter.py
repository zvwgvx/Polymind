
import json
import sys

def convert_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)

        # Check if the data is already in the new format to avoid re-converting
        if original_data and isinstance(original_data[0], dict) and "messages" in original_data[0]:
            print(f"File already in ChatML format: {file_path}")
            return

        new_data = []
        for item in original_data:
            new_item = {
                "messages": [
                    {"role": "system", "content": item.get("system", "")},
                    {"role": "user", "content": item.get("user", "")},
                    {"role": "assistant", "content": item.get("assistant", "")}
                ]
            }
            new_data.append(new_item)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully converted and pretty-printed: {file_path}")

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred with {file_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file_path in sys.argv[1:]:
            convert_file(file_path)
    else:
        print("Usage: python converter.py <file_path1> <file_path2> ...", file=sys.stderr)
