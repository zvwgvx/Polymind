import json
import glob
from pathlib import Path

def format_compact_conversations(data):
    """
    Convert JSON dataset to format where each conversation/message entry is on a single line.
    Top-level structure remains pretty-printed.
    """
    output_lines = []

    if isinstance(data, list):
        # Array of items
        output_lines.append('[')
        for idx, item in enumerate(data):
            output_lines.extend(format_item(item, is_last=(idx == len(data) - 1)))
        output_lines.append(']')
    else:
        # Single object
        output_lines.extend(format_item(data, is_last=True))

    return '\n'.join(output_lines)

def format_item(item, is_last=False, indent=1):
    """Format a single dataset item"""
    lines = []
    ind = '  ' * indent

    lines.append(ind + '{')

    keys = list(item.keys())
    for key_idx, key in enumerate(keys):
        value = item[key]
        is_last_key = (key_idx == len(keys) - 1)

        if key == 'conversations' and isinstance(value, list):
            # Format conversations array with each entry on one line
            lines.append(ind + '  "conversations": [')
            for conv_idx, conv in enumerate(value):
                conv_str = json.dumps(conv, ensure_ascii=False, separators=(',', ': '))
                comma = '' if conv_idx == len(value) - 1 else ','
                lines.append(ind + '    ' + conv_str + comma)
            comma = '' if is_last_key else ','
            lines.append(ind + '  ]' + comma)

        elif key == 'messages' and isinstance(value, list):
            # Format messages array with each entry on one line (for single-turn)
            lines.append(ind + '  "messages": [')
            for msg_idx, msg in enumerate(value):
                msg_str = json.dumps(msg, ensure_ascii=False, separators=(',', ': '))
                comma = '' if msg_idx == len(value) - 1 else ','
                lines.append(ind + '    ' + msg_str + comma)
            comma = '' if is_last_key else ','
            lines.append(ind + '  ]' + comma)

        else:
            # Regular field
            value_str = json.dumps(value, ensure_ascii=False)
            comma = '' if is_last_key else ','
            lines.append(ind + f'  "{key}": {value_str}{comma}')

    comma = '' if is_last else ','
    lines.append(ind + '}' + comma)

    return lines

def convert_file(file_path):
    """Convert a single JSON file to compact conversation format"""
    print(f"Converting: {file_path}")

    # Load JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Format with compact conversations
    formatted_content = format_compact_conversations(data)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(formatted_content)
        f.write('\n')  # Add final newline

    print(f"  ✓ Done: {len(data)} items")

def main():
    print("=" * 70)
    print("JSON FORMAT CONVERTER")
    print("Converting conversations to single-line format")
    print("=" * 70)
    print()

    # Get all JSON files
    multi_turn_files = glob.glob('dataset/multi-turn/*.json')
    single_turn_files = glob.glob('dataset/single-turn/*.json')

    all_files = multi_turn_files + single_turn_files

    if not all_files:
        print("No JSON files found!")
        return

    print(f"Found {len(all_files)} files to convert")
    print()

    # Convert each file
    for file_path in all_files:
        try:
            convert_file(file_path)
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print()
    print("=" * 70)
    print(f"✓ Conversion complete! Processed {len(all_files)} files")
    print("=" * 70)

if __name__ == '__main__':
    main()
