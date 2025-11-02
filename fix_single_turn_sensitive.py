import json

def analyze_sensitive_topic(user_msg, assistant_msg):
    """
    Phân tích user + assistant message để tạo system prompt B+C
    Format: "Bạn là [relationship], đang nói chuyện về [topic]."
    """

    combined = (user_msg + " " + assistant_msg).lower()

    relationship = "bạn thân"  # default for sensitive topics

    # Topic - cụ thể cho sensitive topics
    topic = "vấn đề cá nhân"  # default

    if any(word in combined for word in ['bị bồ đá', 'đá', 'bồ', 'người yêu đá']):
        topic = "bị bồ đá"
    elif any(word in combined for word in ['sếp', 'ép làm', 'làm thêm giờ']):
        topic = "sếp áp bức"
    elif any(word in combined for word in ['trầm cảm', 'depression', 'depressed']):
        topic = "trầm cảm"
    elif any(word in combined for word in ['feeder', 'game', 'ngu', 'chơi game']):
        topic = "toxic gaming"
    elif any(word in combined for word in ['địt', 'sex', 'chịch', 'quan hệ']):
        topic = "tình dục"
    elif any(word in combined for word in ['say', 'nôn', 'rượu', 'uống']):
        topic = "say rượu"
    elif any(word in combined for word in ['bao cao su', 'durex', 'okamoto']):
        topic = "bao cao su"
    elif any(word in combined for word in ['vỡ nợ', 'nợ', 'mượn tiền']):
        topic = "vỡ nợ"
    elif any(word in combined for word in ['gay', 'lgbt', 'homosexual', 'đồng tính']):
        topic = "LGBT"
    elif any(word in combined for word in ['người yêu cũ', 'ex', 'quay lại']):
        topic = "người yêu cũ"
    elif any(word in combined for word in ['thi trượt', 'trượt', 'học']):
        topic = "thi trượt"
    elif any(word in combined for word in ['không muốn sống', 'tự tử', 'chết']):
        topic = "ý định tự tử"
    elif any(word in combined for word in ['quan hệ 3', '3 người', 'threesome']):
        topic = "quan hệ 3 người"
    elif any(word in combined for word in ['cuộc sống vô nghĩa', 'vô nghĩa', 'sống làm gì']):
        topic = "cuộc sống vô nghĩa"
    elif any(word in combined for word in ['phản bội', 'lừa dối']):
        topic = "bị phản bội"
    elif any(word in combined for word in ['phim sex', 'porn', 'xem phim']):
        topic = "nghiện phim sex"
    elif any(word in combined for word in ['nghiện game', 'học hành sa sút']):
        topic = "nghiện game"
    elif any(word in combined for word in ['thích con trai', 'thích con gái', 'bố mẹ không chấp nhận']):
        topic = "coming out"
    elif any(word in combined for word in ['bạn gái', 'breakup', 'chia tay']):
        topic = "chia tay"
    elif any(word in combined for word in ['stress', 'áp lực']):
        topic = "stress"
    elif any(word in combined for word in ['bị bắt nạt', 'bully']):
        topic = "bị bắt nạt"
    elif any(word in combined for word in ['mất việc', 'thất nghiệp']):
        topic = "mất việc"
    elif any(word in combined for word in ['nghiện', 'addiction']):
        topic = "nghiện ngập"
    elif any(word in combined for word in ['bạo hành', 'đánh']):
        topic = "bạo hành"
    elif any(word in combined for word in ['ngoại tình', 'affair']):
        topic = "ngoại tình"

    return f"Bạn là {relationship}, đang nói chuyện về {topic}."

def fix_single_turn_sensitive():
    """Fix ALL 100 single-turn sensitive_topics system prompts"""

    file_path = 'dataset/single-turn/02_sensitive_topics.json'

    print("=" * 60)
    print("🔍 FIX SINGLE-TURN SENSITIVE_TOPICS")
    print("=" * 60)
    print()

    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📊 Tổng: {len(data)} samples")
    print()

    # Analyze and update each
    updated = 0
    for item in data:
        user_msg = item.get('user', '')
        assistant_msg = item.get('assistant', '')

        # Generate new system prompt
        new_system = analyze_sensitive_topic(user_msg, assistant_msg)

        old_system = item.get('system', '')
        if old_system != new_system:
            item['system'] = new_system
            updated += 1
            print(f"✅ {item['id']}: {new_system}")

    # Save
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print()
    print("=" * 60)
    print("✅ HOÀN THÀNH!")
    print("=" * 60)
    print(f"📊 Đã update: {updated}/{len(data)} samples")
    print()
    print("💡 KẾT QUẢ:")
    print("- System prompts theo format B+C")
    print("- Relationship: bạn thân")
    print("- Topic: dựa trên phân tích nội dung sensitive")
    print("=" * 60)

if __name__ == '__main__':
    fix_single_turn_sensitive()