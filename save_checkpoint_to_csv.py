"""
Script để chuyển checkpoint thành CSV khi dừng crawl giữa chừng
"""
import json
import pandas as pd
import os

def save_checkpoint_to_csv():
    """Chuyển checkpoint thành CSV"""
    
    print("=" * 60)
    print("💾 CHUYỂN CHECKPOINT THÀNH CSV")
    print("=" * 60)
    
    # Kiểm tra các file checkpoint
    checkpoints = {
        "1": ("dataset/checkpoint.json", "dataset/news.csv"),
        "2": ("dataset/checkpoint_multi.json", "dataset/news_multi_source.csv")
    }
    
    print("\nFile checkpoint có sẵn:")
    available = []
    for key, (checkpoint_file, csv_file) in checkpoints.items():
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"  {key}. {checkpoint_file} - {len(data)} bài")
            available.append(key)
    
    if not available:
        print("\n❌ Không tìm thấy file checkpoint nào!")
        print("💡 Checkpoint được tạo tự động khi crawl với main.py hoặc multi_source_crawler.py")
        return
    
    # Chọn checkpoint
    choice = input(f"\nChọn checkpoint để chuyển thành CSV ({'/'.join(available)}): ").strip()
    
    if choice not in available:
        print("❌ Lựa chọn không hợp lệ!")
        return
    
    checkpoint_file, csv_file = checkpoints[choice]
    
    # Đọc checkpoint
    print(f"\n📖 Đang đọc {checkpoint_file}...")
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    if not articles:
        print("❌ Checkpoint rỗng!")
        return
    
    # Chuyển thành DataFrame
    df = pd.DataFrame(articles)
    
    # Loại bỏ trùng lặp
    original_count = len(df)
    df = df.drop_duplicates(subset=['url'], keep='first')
    duplicate_count = original_count - len(df)
    
    # Lưu CSV
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ ĐÃ LƯU THÀNH CÔNG!")
    print(f"  📁 File: {csv_file}")
    print(f"  📊 Tổng số bài: {len(df)}")
    if duplicate_count > 0:
        print(f"  🗑️  Đã loại bỏ {duplicate_count} bài trùng lặp")
    
    # Thống kê
    if 'source' in df.columns:
        print(f"\n📊 THỐNG KÊ THEO NGUỒN:")
        print("-" * 60)
        for source, count in df['source'].value_counts().items():
            print(f"  {source:20s}: {count:4d} bài")
    
    if 'category' in df.columns:
        print(f"\n📊 THỐNG KÊ THEO CHỦ ĐỀ (TOP 10):")
        print("-" * 60)
        for cat, count in df['category'].value_counts().head(10).items():
            print(f"  {cat:30s}: {count:4d} bài")
    
    # Hỏi có xóa checkpoint không
    print("\n" + "=" * 60)
    delete = input("Xóa file checkpoint? (y/n, mặc định n): ").strip().lower()
    if delete == 'y':
        os.remove(checkpoint_file)
        print(f"✅ Đã xóa {checkpoint_file}")
    else:
        print(f"💡 Giữ lại {checkpoint_file} để có thể tiếp tục crawl")
    
    print("\n🎉 HOÀN THÀNH!")
    print("\n💡 Bước tiếp theo:")
    print("  1. Chạy: python preprocess.py")
    print("  2. Chạy: python build_ngram.py")

if __name__ == "__main__":
    save_checkpoint_to_csv()
