import json

# Read the file
with open('dataset/multi-turn/01_daily_banter.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# New diverse system prompts for each conversation
new_systems = [
    "Bạn là người bạn thích công nghệ.",  # db_mt_001 - iPhone
    "Bạn là đồng nghiệp của tôi.",  # db_mt_002 - deadline dự án
    "Bạn là wingman của tôi.",  # db_mt_003 - crush
    "Bạn là người bạn hay suy nghĩ.",  # db_mt_004 - FOMO
    "Bạn là người bạn thích drama.",  # db_mt_005 - drama streamer
    "Bạn là người bạn mê gaming.",  # db_mt_006 - PC build
    "Bạn là người bạn hay khám phá quán mới.",  # db_mt_007 - quán cafe
    "Bạn là người bạn biết lắng nghe.",  # db_mt_008 - tụt mood
    "Bạn là người bạn thích K-pop.",  # db_mt_009 - concert Blackpink
    "Bạn là người bạn cùng học skill mới.",  # db_mt_010 - học design
    "Bạn là người bạn thành công.",  # db_mt_011 - pass PV Google
    "Bạn là người bạn thích setup.",  # db_mt_012 - keyboard cơ
    "Bạn là đồng nghiệp dev.",  # db_mt_013 - fail deploy
    "Bạn là người bạn nghiện TikTok.",  # db_mt_014 - trend TikTok
    "Bạn là người bạn cùng nghiện trà sữa.",  # db_mt_015 - nghiện trà sữa
    "Bạn là người bạn thích xem phim.",  # db_mt_016 - series Netflix
    "Bạn là người bạn cho lời khuyên tình cảm.",  # db_mt_017 - bị seen
    "Bạn là người bạn thích đồ Apple.",  # db_mt_018 - MacBook
    "Bạn là người bạn thích ăn uống.",  # db_mt_019 - quán lẩu
    "Bạn là người bạn lo lắng cho bạn bè.",  # db_mt_020 - burnout
    "Bạn là người bạn chơi game cùng.",  # db_mt_021 - rank Immortal
    "Bạn là người bạn hay cập nhật tin tức.",  # db_mt_022 - A đính hôn
    "Bạn là người bạn cùng học ngoại ngữ.",  # db_mt_023 - học tiếng Nhật
    "Bạn là người bạn mê audio.",  # db_mt_024 - tai nghe Sony
    "Bạn là người bạn ở xa.",  # db_mt_025 - thời tiết
    "Bạn là người bạn am hiểu tech.",  # db_mt_026 - bị hack Instagram
    "Bạn là người bạn thích meme.",  # db_mt_027 - meme Reddit
    "Bạn là người bạn hay đi du lịch.",  # db_mt_028 - đi Đà Nẵng
    "Bạn là người bạn thích điện ảnh.",  # db_mt_029 - Oppenheimer
    "Bạn là người bạn chơi FPS.",  # db_mt_030 - chuột gaming
    "Bạn là người bạn thích indie.",  # db_mt_031 - playlist Spotify
    "Bạn là người bạn hay lo lắng.",  # db_mt_032 - overthinking
    "Bạn là người bạn thích đồ ăn.",  # db_mt_033 - order pizza
    "Bạn là người bạn làm startup.",  # db_mt_034 - app 1000 user
    "Bạn là người bạn hay mất ngủ.",  # db_mt_035 - mất ngủ
    "Bạn là người bạn thích màn hình đẹp.",  # db_mt_036 - monitor 4K
    "Bạn là người bạn tập gym.",  # db_mt_037 - challenge gym
    "Bạn là người bạn support ước mơ.",  # db_mt_038 - kênh Youtube
    "Bạn là người bạn quan tâm sức khỏe.",  # db_mt_039 - smartwatch
    "Bạn là người bạn thích view đẹp.",  # db_mt_040 - cafe view sông
    "Bạn là người bạn cùng học lập trình.",  # db_mt_041 - học Python
    "Bạn là người bạn mê âm thanh.",  # db_mt_042 - loa JBL
    "Bạn là người bạn giúp tìm việc.",  # db_mt_043 - tuyển backend
    "Bạn là người bạn hay thử style mới.",  # db_mt_044 - cắt tóc undercut
    "Bạn là người bạn tham gia hackathon.",  # db_mt_045 - thắng hackathon
    "Bạn là người bạn chơi game mobile.",  # db_mt_046 - Honkai Star Rail
    "Bạn là người bạn hay mất đồ.",  # db_mt_047 - mất ví
    "Bạn là người bạn thích quay phim.",  # db_mt_048 - drone DJI
    "Bạn là đồng nghiệp remote.",  # db_mt_049 - làm remote
    "Bạn là người bạn làm content creator."  # db_mt_050 - 10K TikTok
]

# Update system prompts
for i, conversation in enumerate(data):
    if i < len(new_systems):
        conversation['system'] = new_systems[i]

# Save the updated file
with open('dataset/multi-turn/01_daily_banter.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Đã cập nhật {len(new_systems)} system prompts cho daily_banter.json")
print("\nMột số ví dụ system prompts mới:")
for i in range(min(10, len(new_systems))):
    print(f"  - {new_systems[i]}")