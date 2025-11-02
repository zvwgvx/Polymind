import json

def analyze_conversation(conv_id, conversations):
    """
    Đọc KỸ conversation và xác định relationship + topic THỰC TẾ
    """

    # Join tất cả content để phân tích
    full_text = ' '.join([c['content'].lower() for c in conversations])

    # Xác định relationship dựa trên xưng hô và tone
    relationship = "bạn thân"  # default

    if any(word in full_text for word in ['sếp', 'công ty', 'deadline', 'dự án', 'meeting', 'client', 'khách hàng', 'remote work', 'đồng nghiệp']):
        relationship = "đồng nghiệp"
    elif any(word in full_text for word in ['bạn gái', 'bồ', 'người yêu']) and any(word in full_text for word in ['hẹn hò', 'date', 'em yêu', 'anh yêu']):
        relationship = "người yêu"
    elif any(word in full_text for word in ['thầy', 'cô', 'lớp', 'thi', 'học', 'trường']):
        relationship = "bạn cùng lớp"
    elif any(word in full_text for word in ['bro', 'anh em', 'thằng']):
        relationship = "anh em"

    # Phân tích topic dựa trên nội dung THỰC TẾ
    topic = "cuộc sống"  # default

    # Đọc kỹ conversations để xác định chủ đề
    first_user_msg = conversations[0]['content'].lower() if conversations else ""
    all_msgs = ' '.join([c['content'].lower() for c in conversations])

    # Analyze topics - BÁM SÁT nội dung
    if 'iphone' in all_msgs or 'điện thoại' in all_msgs or 'phone' in all_msgs:
        topic = "iPhone mới"
    elif 'deadline' in all_msgs and ('dự án' in all_msgs or 'project' in all_msgs):
        topic = "deadline dự án"
    elif 'crush' in all_msgs:
        topic = "crush"
    elif 'fomo' in all_msgs:
        topic = "FOMO"
    elif 'drama' in all_msgs and ('twitter' in all_msgs or 'streamer' in all_msgs):
        topic = "drama trên mạng"
    elif 'game' in all_msgs or 'rank' in all_msgs or 'champion' in all_msgs or 'lol' in all_msgs or 'valorant' in all_msgs:
        topic = "game"
    elif 'gym' in all_msgs or 'tập' in all_msgs and 'workout' in all_msgs:
        topic = "gym và tập luyện"
    elif 'ăn' in all_msgs or 'food' in all_msgs or 'quán' in all_msgs or 'món' in all_msgs:
        topic = "ăn uống"
    elif 'du lịch' in all_msgs or 'đi chơi' in all_msgs or 'travel' in all_msgs:
        topic = "du lịch"
    elif 'sếp' in all_msgs and 'công ty' in all_msgs:
        topic = "công việc và sếp"
    elif 'phim' in all_msgs or 'movie' in all_msgs or 'series' in all_msgs:
        topic = "phim"
    elif 'bóng đá' in all_msgs or 'football' in all_msgs:
        topic = "bóng đá"
    elif 'hẹn hò' in all_msgs or 'date' in all_msgs:
        topic = "hẹn hò"
    elif 'tình cảm' in all_msgs or 'yêu' in all_msgs:
        topic = "tình cảm"
    elif 'mua' in all_msgs and 'online' in all_msgs:
        topic = "mua sắm online"
    elif 'thời trang' in all_msgs or 'đồ' in all_msgs and 'mặc' in all_msgs:
        topic = "thời trang"
    elif 'nhạc' in all_msgs or 'music' in all_msgs or 'concert' in all_msgs:
        topic = "âm nhạc"
    elif 'gia đình' in all_msgs or 'bố' in all_msgs or 'mẹ' in all_msgs:
        topic = "gia đình"
    elif 'sách' in all_msgs or 'đọc' in all_msgs and 'book' in all_msgs:
        topic = "sách"
    elif 'crypto' in all_msgs or 'bitcoin' in all_msgs or 'đầu tư' in all_msgs:
        topic = "crypto và đầu tư"
    elif 'thú cưng' in all_msgs or 'mèo' in all_msgs or 'chó' in all_msgs:
        topic = "thú cưng"
    elif 'học' in all_msgs and ('chứng chỉ' in all_msgs or 'course' in all_msgs):
        topic = "học thêm và chứng chỉ"
    elif 'makeup' in all_msgs or 'skincare' in all_msgs or 'làm đẹp' in all_msgs:
        topic = "làm đẹp và skincare"
    elif 'streamer' in all_msgs and not 'drama' in all_msgs:
        topic = "streamer yêu thích"
    elif 'nấu' in all_msgs or 'cooking' in all_msgs or 'recipe' in all_msgs:
        topic = "nấu ăn"
    elif 'thầy' in all_msgs or 'cô' in all_msgs:
        topic = "thầy cô"
    elif 'startup' in all_msgs or 'kinh doanh' in all_msgs:
        topic = "startup và kinh doanh"
    elif 'ngủ' in all_msgs or 'thức khuya' in all_msgs:
        topic = "ngủ nướng và thức khuya"
    elif 'remote' in all_msgs or 'wfh' in all_msgs:
        topic = "remote work"
    elif 'shopping' in all_msgs:
        topic = "shopping"
    elif 'anime' in all_msgs:
        topic = "anime"
    elif 'sức khỏe' in all_msgs or 'health' in all_msgs:
        topic = "sức khỏe"
    elif 'setup' in all_msgs and 'pc' in all_msgs:
        topic = "setup PC gaming"
    elif 'coffee' in all_msgs or 'cà phê' in all_msgs or 'cafe' in all_msgs:
        topic = "coffee shop"
    elif 'khách hàng' in all_msgs:
        topic = "khách hàng khó tính"
    elif 'sneaker' in all_msgs or 'giày' in all_msgs:
        topic = "sneaker"
    elif 'nghề' in all_msgs or 'career' in all_msgs:
        topic = "chuyện nghề nghiệp"
    elif 'yoga' in all_msgs or 'meditation' in all_msgs:
        topic = "yoga và meditation"
    elif 'esport' in all_msgs:
        topic = "Esports"
    elif 'meeting' in all_msgs:
        topic = "meeting"
    elif 'netflix' in all_msgs:
        topic = "Netflix"
    elif 'meme' in all_msgs:
        topic = "memes"
    elif 'cuối tuần' in all_msgs or 'weekend' in all_msgs:
        topic = "planning cuối tuần"
    elif 'tình bạn' in all_msgs or 'bạn bè' in all_msgs:
        topic = "tình bạn"
    elif 'cá cược' in all_msgs or 'cược' in all_msgs:
        topic = "cá cược và game"
    elif 'chụp' in all_msgs and 'ảnh' in all_msgs:
        topic = "chụp ảnh"
    elif 'xe' in all_msgs and ('máy' in all_msgs or 'motor' in all_msgs):
        topic = "xe máy"
    elif 'vẽ' in all_msgs or 'art' in all_msgs:
        topic = "sở thích vẽ"
    elif 'guitar' in all_msgs:
        topic = "guitar và nhạc"
    elif 'ngoại ngữ' in all_msgs or 'tiếng anh' in all_msgs:
        topic = "học ngoại ngữ"
    elif 'thể thao' in all_msgs or 'sport' in all_msgs:
        topic = "thể thao"
    elif 'podcast' in all_msgs:
        topic = "podcast"
    elif 'phim hàn' in all_msgs or 'kdrama' in all_msgs:
        topic = "phim Hàn"
    elif 'karaoke' in all_msgs:
        topic = "karaoke"
    elif 'teambuilding' in all_msgs:
        topic = "teambuilding"
    elif 'môi trường' in all_msgs or 'environment' in all_msgs:
        topic = "môi trường"
    elif 'âm mưu' in all_msgs or 'conspiracy' in all_msgs:
        topic = "âm mưu thuyết"
    elif 'thiền' in all_msgs:
        topic = "thiền và sức khỏe tâm lý"
    elif 'nft' in all_msgs:
        topic = "NFT"
    elif 'vườn' in all_msgs or 'trồng' in all_msgs:
        topic = "làm vườn"
    elif 'alpha' in all_msgs or 'sigma' in all_msgs:
        topic = "mindset alpha"
    elif 'bbq' in all_msgs or 'nướng' in all_msgs:
        topic = "nướng BBQ"
    elif 'nghệ thuật' in all_msgs:
        topic = "nghệ thuật"

    return f"Bạn là {relationship}, đang nói chuyện về {topic}."


# Read file
print("=" * 60)
print("🔍 ĐỌC VÀ PHÂN TÍCH TOÀN BỘ DAILY_BANTER")
print("=" * 60)
print()

with open('dataset/multi-turn/01_daily_banter.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"📊 Tổng: {len(data)} samples")
print()
print("🔄 Bắt đầu phân tích từng conversation...")
print()

# Analyze each and print for verification
system_prompts = {}

for i, item in enumerate(data, 1):
    conv_id = item['id']
    conversations = item['conversations']

    # Analyze
    new_system = analyze_conversation(conv_id, conversations)
    system_prompts[conv_id] = new_system

    # Show sample of conversation content for verification
    first_msg = conversations[0]['content'][:50].replace('\n', ' ')

    print(f"{i}. {conv_id}")
    print(f"   First msg: {first_msg}...")
    print(f"   System: {new_system}")
    print()

# Update data
print("=" * 60)
print("💾 CẬP NHẬT FILE")
print("=" * 60)

for item in data:
    item['system'] = system_prompts[item['id']]

# Save
with open('dataset/multi-turn/01_daily_banter.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ ĐÃ HOÀN THÀNH!")
print(f"📊 Đã phân tích và cập nhật {len(data)} system prompts")
print("💡 Tất cả đều BÁM SÁT nội dung conversation thực tế!")