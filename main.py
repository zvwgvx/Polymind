import json
import tiktoken
from pathlib import Path

def count_tokens(text, encoding):
    """Đếm số token trong text"""
    return len(encoding.encode(text))

def count_tokens_in_item(item, encoding):
    """Đếm tổng số token trong 1 item (multi-turn hoặc single-turn)"""
    total = 0

    # System prompt
    if 'system' in item:
        total += count_tokens(item['system'], encoding)

    # Multi-turn conversations
    if 'conversations' in item:
        for conv in item['conversations']:
            total += count_tokens(conv['content'], encoding)

    # Single-turn user/assistant
    if 'user' in item:
        total += count_tokens(item['user'], encoding)
    if 'assistant' in item:
        total += count_tokens(item['assistant'], encoding)

    return total

def load_dataset(file_path):
    """Load JSON dataset"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # Initialize tiktoken with o200k_base encoding
    encoding = tiktoken.get_encoding('o200k_base')

    print("=" * 70)
    print("📊 DATASET TOKEN COUNTER & MERGER")
    print("=" * 70)
    print(f"🔧 Encoding: o200k_base")
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
    print("📁 MULTI-TURN DATASETS")
    print("-" * 70)

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

        print(f"✓ {name}")
        print(f"  Items: {len(data):,}")
        print(f"  Tokens: {tokens:,}")
        print(f"  Avg tokens/item: {tokens/len(data):.1f}")
        print()

    print(f"📊 Multi-turn TOTAL: {multi_turn_total_items:,} items, {multi_turn_total_tokens:,} tokens")
    print()

    # Process Single-turn datasets
    print("📁 SINGLE-TURN DATASETS")
    print("-" * 70)

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

        print(f"✓ {name}")
        print(f"  Items: {len(data):,}")
        print(f"  Tokens: {tokens:,}")
        print(f"  Avg tokens/item: {tokens/len(data):.1f}")
        print()

    print(f"📊 Single-turn TOTAL: {single_turn_total_items:,} items, {single_turn_total_tokens:,} tokens")
    print()

    # Overall statistics
    print("=" * 70)
    print("📊 TỔNG KẾT")
    print("=" * 70)
    total_items = multi_turn_total_items + single_turn_total_items
    total_tokens = multi_turn_total_tokens + single_turn_total_tokens

    print(f"Multi-turn:   {multi_turn_total_items:,} items ({multi_turn_total_tokens:,} tokens)")
    print(f"Single-turn:  {single_turn_total_items:,} items ({single_turn_total_tokens:,} tokens)")
    print(f"TOTAL:        {total_items:,} items ({total_tokens:,} tokens)")
    print(f"Average:      {total_tokens/total_items:.1f} tokens/item")
    print()

    # Renumber IDs and create merged dataset
    print("=" * 70)
    print("🔀 MERGING DATASETS")
    print("=" * 70)
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

        print(f"✓ {name}")
        print(f"  ID range: {start_id:04d} - {end_id:04d} ({len(data)} items)")
        print()

    # Save merged dataset
    output_file = 'dataset.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print("=" * 70)
    print(f"✅ Đã lưu merged dataset vào: {output_file}")
    print(f"📊 Tổng cộng: {len(merged_data):,} items")
    print("=" * 70)
    print()

    # Print ID mapping summary
    print("📋 ID MAPPING SUMMARY:")
    print("-" * 70)
    for range_info in id_ranges:
        print(f"{range_info['name']:40s} → IDs {range_info['start']:04d}-{range_info['end']:04d}")
    print("=" * 70)

    # Save statistics to file
    stats_output = {
        'encoding': 'o200k_base',
        'summary': {
            'total_items': total_items,
            'total_tokens': total_tokens,
            'multi_turn_items': multi_turn_total_items,
            'multi_turn_tokens': multi_turn_total_tokens,
            'single_turn_items': single_turn_total_items,
            'single_turn_tokens': single_turn_total_tokens,
            'avg_tokens_per_item': total_tokens / total_items
        },
        'datasets': stats,
        'id_ranges': id_ranges
    }

    with open('dataset_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats_output, f, ensure_ascii=False, indent=2)

    print()
    print("✅ Đã lưu thống kê vào: dataset_stats.json")
    print()

if __name__ == '__main__':
    main()