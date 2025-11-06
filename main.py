import json
import tiktoken
from pathlib import Path

# ANSI Color Codes for Dark Theme
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Dark theme colors
    BLACK = '\033[30m'
    GRAY = '\033[90m'
    WHITE = '\033[37m'
    BRIGHT_WHITE = '\033[97m'

    # Accent colors (muted for dark theme)
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'

def count_tokens(text, encoding):
    """Count tokens in text"""
    return len(encoding.encode(text))

def count_tokens_in_item(item, encoding):
    """Count total tokens in one item (multi-turn or single-turn)"""
    total = 0

    # System prompt
    if 'system' in item:
        total += count_tokens(item['system'], encoding)

    # Multi-turn conversations (format: conversations array with role/content)
    if 'conversations' in item:
        for conv in item['conversations']:
            total += count_tokens(conv['content'], encoding)

    # Single-turn user/assistant (format: user/assistant fields)
    if 'user' in item:
        total += count_tokens(item['user'], encoding)
    if 'assistant' in item:
        total += count_tokens(item['assistant'], encoding)

    # New format: messages array (role/content format used in single-turn datasets)
    if 'messages' in item:
        for message in item['messages']:
            total += count_tokens(message['content'], encoding)

    return total

def load_dataset(file_path):
    """Load JSON dataset with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                # Get context around the error
                lines = content.split('\n')
                start = max(0, e.lineno - 3)
                end = min(len(lines), e.lineno + 3)
                context = '\n'.join(f"{i+1}: {line}" for i, line in enumerate(lines[start:end], start))
                print(f"\nJSON Error near line {e.lineno}, column {e.colno}:")
                print(context)
                print("\nTrying to fix common JSON issues...")

                # Try fixing common JSON issues
                # 1. Remove trailing commas
                fixed = content.replace(',]', ']').replace(',}', '}')
                # 2. Add missing closing brackets/braces
                if content.count('[') > content.count(']'):
                    fixed += ']' * (content.count('[') - content.count(']'))
                if content.count('{') > content.count('}'):
                    fixed += '}' * (content.count('{') - content.count('}'))

                try:
                    return json.loads(fixed)
                except:
                    raise Exception(f"Failed to parse JSON in {file_path}. Original error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading {file_path}: {str(e)}")

def main():
    # Initialize tiktoken with o200k_base encoding
    encoding = tiktoken.get_encoding('o200k_base')
    c = Colors  # Shorthand

    print(f"{c.GRAY}{'█' * 60}{c.RESET}")
    print(f"{c.BRIGHT_WHITE}{c.BOLD}  DATASET TOKEN COUNTER & MERGER{c.RESET}")
    print(f"{c.GRAY}{'█' * 60}{c.RESET}")
    print(f"{c.GRAY}  Encoding: {c.WHITE}o200k_base{c.RESET}")
    print()

    # Define datasets
    multi_turn_datasets = [
        ('dataset/multi-turn/01_daily_banter.json', 'Multi-turn Daily Banter'),
        ('dataset/multi-turn/02_sensitive_topics.json', 'Multi-turn Sensitive Topics'),
        ('dataset/multi-turn/03_roleplay.json', 'Multi-turn Roleplay'),
    ]

    single_turn_datasets = [
        ('dataset/single-turn/01_daily_banter.json', 'Single-turn Daily Banter'),
        ('dataset/single-turn/02_sensitive_topics.json', 'Single-turn Sensitive Topics'),
        ('dataset/single-turn/03_roleplay.json', 'Single-turn Roleplay'),
    ]

    # Statistics
    all_data = []
    stats = {}

    # Process Multi-turn datasets
    print(f"{c.CYAN}{c.BOLD}[MULTI-TURN DATASETS]{c.RESET}")
    print(f"{c.GRAY}{'─' * 70}{c.RESET}")

    multi_turn_total_tokens = 0
    multi_turn_total_items = 0

    for file_path, name in multi_turn_datasets:
        data = load_dataset(file_path)
        tokens = sum(count_tokens_in_item(item, encoding) for item in data)

        stats[name] = {
            'items': len(data),
            'tokens': tokens,
            'source_file': file_path
        }

        # Add to merged data with source info
        for item in data:
            item_copy = item.copy()
            item_copy['_source'] = name
            all_data.append(item_copy)

        multi_turn_total_tokens += tokens
        multi_turn_total_items += len(data)

        print(f"{c.GREEN}[✓]{c.RESET} {c.WHITE}{name}{c.RESET}")
        print(f"{c.GRAY}    Items:       {c.RESET}{len(data):,}")
        print(f"{c.GRAY}    Tokens:      {c.RESET}{tokens:,}")
        print(f"{c.GRAY}    Avg/item:    {c.RESET}{tokens/len(data):.1f}")
        print()

    print(f"{c.GRAY}[SUMMARY]{c.RESET} Multi-turn: {c.WHITE}{multi_turn_total_items:,}{c.RESET} samples, {c.WHITE}{multi_turn_total_tokens:,}{c.RESET} tokens")
    print()

    # Process Single-turn datasets
    print(f"{c.CYAN}{c.BOLD}[SINGLE-TURN DATASETS]{c.RESET}")
    print(f"{c.GRAY}{'─' * 70}{c.RESET}")

    single_turn_total_tokens = 0
    single_turn_total_items = 0

    for file_path, name in single_turn_datasets:
        data = load_dataset(file_path)
        tokens = sum(count_tokens_in_item(item, encoding) for item in data)

        stats[name] = {
            'items': len(data),
            'tokens': tokens,
            'source_file': file_path
        }

        # Add to merged data with source info
        for item in data:
            item_copy = item.copy()
            item_copy['_source'] = name
            all_data.append(item_copy)

        single_turn_total_tokens += tokens
        single_turn_total_items += len(data)

        print(f"{c.GREEN}[✓]{c.RESET} {c.WHITE}{name}{c.RESET}")
        print(f"{c.GRAY}    Items:       {c.RESET}{len(data):,}")
        print(f"{c.GRAY}    Tokens:      {c.RESET}{tokens:,}")
        print(f"{c.GRAY}    Avg/item:    {c.RESET}{tokens/len(data):.1f}")
        print()

    print(f"{c.GRAY}[SUMMARY]{c.RESET} Single-turn: {c.WHITE}{single_turn_total_items:,}{c.RESET} samples, {c.WHITE}{single_turn_total_tokens:,}{c.RESET} tokens")
    print()

    # Overall statistics
    print(f"{c.GRAY}{'█' * 60}{c.RESET}")
    print(f"{c.BRIGHT_WHITE}{c.BOLD}  OVERALL SUMMARY{c.RESET}")
    print(f"{c.GRAY}{'█' * 60}{c.RESET}")
    total_items = multi_turn_total_items + single_turn_total_items
    total_tokens = multi_turn_total_tokens + single_turn_total_tokens

    print(f"{c.GRAY}  Multi-turn:  {c.RESET}{c.WHITE}{multi_turn_total_items:,}{c.RESET} samples ({c.WHITE}{multi_turn_total_tokens:,}{c.RESET} tokens)")
    print(f"{c.GRAY}  Single-turn: {c.RESET}{c.WHITE}{single_turn_total_items:,}{c.RESET} samples ({c.WHITE}{single_turn_total_tokens:,}{c.RESET} tokens)")
    print(f"{c.GRAY}  TOTAL:       {c.RESET}{c.BRIGHT_WHITE}{c.BOLD}{total_items:,}{c.RESET} samples ({c.BRIGHT_WHITE}{c.BOLD}{total_tokens:,}{c.RESET} tokens)")
    print(f"{c.GRAY}  Average:     {c.RESET}{total_tokens/total_items:.1f} tokens/sample")
    print()

    # Renumber IDs and create merged dataset
    print(f"{c.GRAY}{'█' * 60}{c.RESET}")
    print(f"{c.BRIGHT_WHITE}{c.BOLD}  MERGING DATASETS{c.RESET}")
    print(f"{c.GRAY}{'█' * 60}{c.RESET}")
    print()

    merged_data = []
    current_id = 1
    id_ranges = []

    # Process in order: multi-turn first, then single-turn
    all_datasets = multi_turn_datasets + single_turn_datasets

    for file_path, name in all_datasets:
        data = load_dataset(file_path)
        start_id = current_id

        for item in data:
            new_item = item.copy()
            # Store original ID if exists
            if 'id' in item:
                new_item['_original_id'] = item['id']
            # Renumber ID
            new_item['id'] = f"{current_id:04d}"
            new_item['_source'] = name
            merged_data.append(new_item)
            current_id += 1

        end_id = current_id - 1
        id_ranges.append({
            'name': name,
            'start': start_id,
            'end': end_id,
            'count': len(data)
        })

        print(f"{c.GREEN}[✓]{c.RESET} {c.WHITE}{name}{c.RESET}")
        print(f"{c.GRAY}    ID range:    {c.RESET}{start_id:04d} - {end_id:04d} ({len(data)} samples)")
        print()

    # Save merged dataset
    output_file = 'dataset.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    # Save merged dataset in JSONL format
    output_jsonl_file = 'dataset.jsonl'
    with open(output_jsonl_file, 'w', encoding='utf-8') as f:
        for item in merged_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"{c.GRAY}{'█' * 60}{c.RESET}")
    print(f"{c.GREEN}  [✓] Saved merged dataset to: {c.WHITE}{output_file}{c.RESET}")
    print(f"{c.GRAY}      Total: {c.RESET}{c.WHITE}{len(merged_data):,}{c.RESET} samples")
    print(f"{c.GREEN}  [✓] Saved merged dataset to: {c.WHITE}{output_jsonl_file}{c.RESET}")
    print(f"{c.GRAY}      Total: {c.RESET}{c.WHITE}{len(merged_data):,}{c.RESET} samples")
    print(f"{c.GRAY}{'█' * 60}{c.RESET}")
    print()

    # Print ID mapping summary
    print(f"{c.CYAN}{c.BOLD}[ID MAPPING SUMMARY]{c.RESET}")
    print(f"{c.GRAY}{'─' * 70}{c.RESET}")
    for range_info in id_ranges:
        print(f"{c.WHITE}{range_info['name']:40s}{c.RESET} {c.GRAY}→{c.RESET} IDs {c.WHITE}{range_info['start']:04d}{c.RESET}-{c.WHITE}{range_info['end']:04d}{c.RESET}")
    print(f"{c.GRAY}{'█' * 60}{c.RESET}")

    # Save statistics to file
    stats_output = {
        'encoding': 'o200k_base',
        'summary': {
            'total_samples': total_items,
            'total_tokens': total_tokens,
            'multi_turn_samples': multi_turn_total_items,
            'multi_turn_tokens': multi_turn_total_tokens,
            'single_turn_samples': single_turn_total_items,
            'single_turn_tokens': single_turn_total_tokens,
            'avg_tokens_per_sample': total_tokens / total_items
        },
        'datasets': stats,
        'id_ranges': id_ranges
    }

    with open('dataset_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats_output, f, ensure_ascii=False, indent=2)

    print()
    print(f"{c.GREEN}[✓] Saved statistics to: {c.WHITE}dataset_stats.json{c.RESET}")
    print()

if __name__ == '__main__':
    main()