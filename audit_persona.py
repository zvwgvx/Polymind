import json
import re

def audit_persona_issues(file_path, dataset_name):
    """
    Rà soát các vấn đề về persona:
    1. Từ 'gét gô' cần thay
    2. Cách nói quá trang trọng
    3. Mất tính GenZ tự nhiên
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("=" * 70)
    print(f"🔍 AUDIT: {dataset_name}")
    print("=" * 70)
    print()

    issues = []

    # Các pattern cần tìm
    PROBLEMATIC_PATTERNS = {
        'gét gô': 'Cần thay bằng adu/ngol hoặc cách nói tự nhiên',
        'get go': 'Biến thể của gét gô',
        'rất tốt': 'Quá trang trọng - nên dùng ngon/xịn/cháy',
        'rất hay': 'Quá trang trọng - nên dùng hay vl/hay vc',
        'cảm ơn bạn': 'Quá trang trọng - nên dùng cảm ơn m/thanks',
        'không sao đâu': 'Có thể trang trọng - xem context',
        'xin lỗi bạn': 'Quá trang trọng - nên dùng sorry/xin lỗi m',
        'tôi nghĩ rằng': 'Quá formal - nên dùng t nghĩ/t thấy',
        'bạn nên': 'Hơi trang trọng - nên dùng m nên/m thử',
        'chúng ta': 'Formal - nên dùng tụi m/tụi t/mình',
        'điều này': 'Formal - nên dùng cái này/nó',
        'vấn đề': 'Có thể formal - xem context',
        'thực sự': 'Có thể trang trọng - xem context',
        'tuy nhiên': 'Rất formal - nên dùng nhưng mà/nhưng',
        'do đó': 'Rất formal - nên dùng nên là/thế nên',
        'mặc dù': 'Formal - nên dùng dù/dù sao',
        'bởi vì': 'Hơi formal - nên dùng vì/tại vì',
        'nếu như': 'Hơi formal - nên dùng nếu/giả sử',
        'hơn nữa': 'Formal - nên dùng và/còn',
        'nhằm': 'Rất formal - tránh dùng',
        'được': 'Kiểm tra cấu trúc bị động quá formal',
    }

    for item in data:
        item_id = item.get('id', 'unknown')

        # Kiểm tra user message
        user_msg = item.get('user', '')
        assistant_msg = item.get('assistant', '')

        # Tìm issues trong assistant message (quan trọng nhất)
        for pattern, reason in PROBLEMATIC_PATTERNS.items():
            if pattern in assistant_msg.lower():
                issues.append({
                    'id': item_id,
                    'type': 'assistant',
                    'pattern': pattern,
                    'reason': reason,
                    'snippet': assistant_msg[:100].replace('\n', ' ')
                })

    # Report
    print(f"📊 Tổng samples: {len(data)}")
    print(f"⚠️  Tìm thấy: {len(issues)} potential issues")
    print()

    if issues:
        # Group by pattern
        pattern_counts = {}
        for issue in issues:
            p = issue['pattern']
            if p not in pattern_counts:
                pattern_counts[p] = []
            pattern_counts[p].append(issue)

        print("📋 CHI TIẾT THEO PATTERN:")
        print()

        for pattern in sorted(pattern_counts.keys(), key=lambda x: len(pattern_counts[x]), reverse=True):
            count = len(pattern_counts[pattern])
            print(f"🔸 '{pattern}' - {count} lần")
            print(f"   → {pattern_counts[pattern][0]['reason']}")

            # Show first 3 examples
            for i, issue in enumerate(pattern_counts[pattern][:3]):
                print(f"   • {issue['id']}: {issue['snippet']}...")

            if count > 3:
                print(f"   ... và {count - 3} nơi khác")
            print()

    else:
        print("✅ Không tìm thấy pattern problematic rõ ràng")
        print()

    return issues


if __name__ == '__main__':
    print()

    # Audit all 3 single-turn datasets
    all_issues = []

    datasets = [
        ('dataset/single-turn/01_daily_banter.json', 'DAILY BANTER (500 samples)'),
        ('dataset/single-turn/02_sensitive_topics.json', 'SENSITIVE TOPICS (100 samples)'),
        ('dataset/single-turn/03_roleplay.json', 'ROLEPLAY (100 samples)'),
    ]

    for file_path, name in datasets:
        issues = audit_persona_issues(file_path, name)
        all_issues.extend(issues)
        print()

    print("=" * 70)
    print("📊 TỔNG KẾT")
    print("=" * 70)
    print(f"Tổng issues tìm thấy: {len(all_issues)}")
    print()

    if all_issues:
        print("🎯 CẦN FIX:")
        print("1. Thay 'gét gô' → 'adu' / 'ngol' / cách nói tự nhiên")
        print("2. Giảm tính trang trọng → tăng tính GenZ casual")
        print("3. Đảm bảo persona nhất quán với bản gốc")
    else:
        print("✅ Tất cả datasets đã đạt chuẩn persona!")

    print("=" * 70)