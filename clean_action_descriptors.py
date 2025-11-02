import json
import re

def clean_action_descriptors(text):
    """Remove all *action* patterns from text"""
    # Remove *action* patterns
    cleaned = re.sub(r'\*[^*]+\*', '', text)

    # Clean up extra whitespace and newlines
    lines = cleaned.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line:  # Keep non-empty lines
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def clean_dataset(file_path):
    """Clean a dataset file"""
    print(f"\n🔄 Đang xử lý: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    action_count = 0

    for item in data:
        # Clean conversations
        if 'conversations' in item:
            for conv in item['conversations']:
                if 'content' in conv:
                    original = conv['content']
                    cleaned = clean_action_descriptors(original)
                    if original != cleaned:
                        action_count += 1
                    conv['content'] = cleaned

        # Clean system prompt if has actions (unlikely but check)
        if 'system' in item and item['system']:
            original = item['system']
            cleaned = clean_action_descriptors(original)
            if original != cleaned:
                action_count += 1
            item['system'] = cleaned

    # Save cleaned data
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  ✅ Đã clean {action_count} messages có action descriptors")
    print(f"  📊 Tổng samples: {len(data)}")

    return action_count

# Clean all datasets
print("=" * 60)
print("🧹 BẮT ĐẦU CLEAN ACTION DESCRIPTORS")
print("=" * 60)

total_cleaned = 0

# Multi-turn datasets
datasets = [
    'dataset/multi-turn/01_daily_banter.json',
    'dataset/multi-turn/02_sensitive_topics.json',
    'dataset/multi-turn/03_roleplay.json'
]

for dataset in datasets:
    try:
        count = clean_dataset(dataset)
        total_cleaned += count
    except FileNotFoundError:
        print(f"  ⚠️  File không tồn tại: {dataset}")
    except Exception as e:
        print(f"  ❌ Lỗi: {e}")

print("\n" + "=" * 60)
print(f"✅ HOÀN THÀNH!")
print(f"📊 Tổng số messages đã clean: {total_cleaned}")
print("=" * 60)

print("\n💡 KẾT QUẢ:")
print("- Đã remove tất cả *action* descriptors")
print("- Giữ lại pure dialogue")
print("- Format cleaned và consistent")
print("- Model sẽ chat 100% natural như người thật")