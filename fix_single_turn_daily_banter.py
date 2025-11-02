import json

def analyze_and_create_system_prompt(user_msg, assistant_msg):
    """
    Phân tích user + assistant message để tạo system prompt B+C
    Format: "Bạn là [relationship], đang nói chuyện về [topic]."
    """

    # Combine để phân tích
    combined = (user_msg + " " + assistant_msg).lower()

    # Relationship - hầu hết single-turn daily banter là bạn thân
    relationship = "bạn thân"

    # Topic - dựa trên nội dung
    topic = "cuộc sống"  # default

    # Analyze topic based on keywords
    if any(word in combined for word in ['wren evans', 'bài hát', 'nhạc', 'ca sĩ', 'rapper', 'concert', 'westlife', 'piano']):
        topic = "âm nhạc"
    elif any(word in combined for word in ['xăm', 'tattoo', 'hình xăm']):
        topic = "xăm mình"
    elif any(word in combined for word in ['làm', 'nghỉ việc', 'công ty', 'deadline', 'pressing', 'off']):
        topic = "công việc"
    elif any(word in combined for word in ['tóp tóp', 'tiktok', 'video', 'trend', 'biến hình']):
        topic = "TikTok"
    elif any(word in combined for word in ['cà phê', 'cafe', 'quán', 'coffee']):
        topic = "quán café"
    elif any(word in combined for word in ['béo', 'gầy', 'cân nặng', 'ăn ít']):
        topic = "cân nặng"
    elif any(word in combined for word in ['crush', 'rep story', 'thả thính']):
        topic = "crush"
    elif any(word in combined for word in ['drama', 'phốt', 'hóng', 'showbiz']):
        topic = "drama"
    elif any(word in combined for word in ['điện thoại', 'pin', 'sạc']):
        topic = "điện thoại"
    elif any(word in combined for word in ['game', 'chơi game']):
        topic = "game"
    elif any(word in combined for word in ['card màn hình', 'pc', 'build']):
        topic = "PC gaming"
    elif any(word in combined for word in ['bố mẹ', 'mắng', 'gia đình']):
        topic = "gia đình"
    elif any(word in combined for word in ['nhuộm tóc', 'tóc', 'màu khói']):
        topic = "tóc"
    elif any(word in combined for word in ['buffet', 'ăn']):
        topic = "ăn uống"
    elif any(word in combined for word in ['simp', 'xinh']):
        topic = "simp"
    elif any(word in combined for word in ['vé máy bay', 'thái', 'du lịch']):
        topic = "du lịch"
    elif any(word in combined for word in ['outfit', 'ăn mặc', 'vibe']):
        topic = "thời trang"
    elif any(word in combined for word in ['overthinking', 'nghĩ nhiều']):
        topic = "overthinking"
    elif any(word in combined for word in ['phim ma', 'xem phim']):
        topic = "phim"
    elif any(word in combined for word in ['fomo', 'sợ bị tối cổ', 'lướt mạng']):
        topic = "FOMO"
    elif any(word in combined for word in ['nhạc cụ', 'piano', 'học']):
        topic = "học nhạc cụ"
    elif any(word in combined for word in ['tụt mood', 'buồn', 'trời mưa']):
        topic = "tâm trạng"
    elif any(word in combined for word in ['seen tin nhắn', 'tin nhắn']):
        topic = "tin nhắn"

    return f"Bạn là {relationship}, đang nói chuyện về {topic}."

def fix_single_turn_daily_banter():
    """Fix ALL 500 single-turn daily_banter system prompts"""

    file_path = 'dataset/single-turn/01_daily_banter.json'

    print("=" * 60)
    print("🔍 FIX SINGLE-TURN DAILY_BANTER")
    print("=" * 60)
    print()

    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📊 Tổng: {len(data)} samples")
    print()

    # Analyze and update each
    updated = 0
    samples_shown = 0
    max_show = 50  # Only show first 50 to avoid too much output

    for item in data:
        user_msg = item.get('user', '')
        assistant_msg = item.get('assistant', '')

        # Generate new system prompt
        new_system = analyze_and_create_system_prompt(user_msg, assistant_msg)

        old_system = item.get('system', '')
        if old_system != new_system:
            item['system'] = new_system
            updated += 1

            # Show first few
            if samples_shown < max_show:
                print(f"✅ {item['id']}: {new_system}")
                if samples_shown < 10:  # Show user msg for first 10
                    print(f"   User: {user_msg[:60]}...")
                samples_shown += 1

    if updated > max_show:
        print(f"... và {updated - max_show} samples khác")

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
    print("- Relationship: bạn thân (phù hợp với single-turn casual)")
    print("- Topic: dựa trên phân tích nội dung")
    print("=" * 60)

if __name__ == '__main__':
    fix_single_turn_daily_banter()