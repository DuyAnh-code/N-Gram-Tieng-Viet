import re
import pandas as pd
from underthesea import word_tokenize
from tqdm import tqdm
import os

# Danh sách stopwords tiếng Việt phổ biến
STOPWORDS = {
    'và', 'của', 'có', 'được', 'cho', 'từ', 'với', 'theo', 'trong', 'là',
    'một', 'này', 'đã', 'để', 'các', 'những', 'tại', 'còn', 'như', 'khi',
    'đó', 'nên', 'nếu', 'hoặc', 'thì', 'mà', 'rất', 'cũng', 'vào', 'ra',
    'về', 'lại', 'lên', 'bị', 'sẽ', 'đang', 'bởi', 'nữa', 'hay',
    'nhiều', 'hơn', 'cả', 'sau', 'trước', 'giữa', 'do', 'nhưng', 'vì'
}

def preprocess_text(text, remove_stopwords=False, min_word_length=2):
    """Tiền xử lý văn bản tiếng Việt"""
    if not text or not isinstance(text, str):
        return []
    
    # Chuyển về chữ thường
    text = text.lower()
    
    # Loại bỏ ký tự đặc biệt, giữ lại chữ cái và khoảng trắng
    text = re.sub(r"[^\w\s]", " ", text)
    
    # Loại bỏ số
    text = re.sub(r"\d+", "", text)
    
    # Loại bỏ khoảng trắng thừa
    text = re.sub(r"\s+", " ", text).strip()
    
    # Tách từ tiếng Việt cấp độ Từ (Word-level), BẮT BUỘC giữ dấu _ để tránh lỗi khoảng trắng khi tính N-gram
    tokenized = word_tokenize(text, format="text")
    tokens = tokenized.split()
    
    # Lọc stopwords nếu được yêu cầu
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS]
    
    # Lọc từ quá ngắn
    tokens = [t for t in tokens if len(t) >= min_word_length]
    
    return tokens

def analyze_text_stats(df):
    """Phân tích thống kê về văn bản"""
    total_words = sum(df['tokens'].apply(len))
    avg_words = total_words / len(df)
    max_words = df['tokens'].apply(len).max()
    min_words = df['tokens'].apply(len).min()
    
    return {
        'total_articles': len(df),
        'total_words': total_words,
        'avg_words_per_article': avg_words,
        'max_words': max_words,
        'min_words': min_words
    }

def main():
    """Xử lý dữ liệu từ CSV - CHỈ XỬ LÝ BÀI MỚI"""
    print("=" * 80)
    print("🔧 TIỀN XỬ LÝ DỮ LIỆU - PHIÊN BẢN THÔNG MINH")
    print("=" * 80)
    print("💡 Chỉ xử lý những bài mới chưa được xử lý")
    print("=" * 80)
    
    # File paths
    input_file = "dataset/news.csv"
    output_file = "dataset/news_processed.csv"
    
    # Bước 1: Đọc dữ liệu gốc
    print(f"\n📂 Đang đọc dữ liệu từ {input_file}...")
    
    try:
        df_raw = pd.read_csv(input_file, encoding='utf-8-sig')
        print(f"✅ Đã đọc {len(df_raw):,} bài từ file gốc")
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {input_file}")
        print("💡 Hãy chạy 'python crawler.py' trước để crawl dữ liệu!")
        return
    
    # Bước 2: Kiểm tra file đã xử lý
    print(f"\n🔍 Kiểm tra dữ liệu đã xử lý...")
    
    if os.path.exists(output_file):
        try:
            df_processed = pd.read_csv(output_file, encoding='utf-8-sig')
            print(f"✅ Tìm thấy {len(df_processed):,} bài đã xử lý")
            
            # Tìm các bài MỚI chưa xử lý (dựa vào URL)
            processed_urls = set(df_processed['url'].values)
            df_new = df_raw[~df_raw['url'].isin(processed_urls)]
            
            print(f"📊 Phát hiện {len(df_new):,} bài MỚI cần xử lý")
            
            if len(df_new) == 0:
                print("\n✅ TẤT CẢ DỮ LIỆU ĐÃ ĐƯỢC XỬ LÝ!")
                print("💡 Không có bài mới nào cần xử lý")
                return
            
        except Exception as e:
            print(f"⚠️ Lỗi đọc file đã xử lý: {e}")
            print("→ Sẽ xử lý toàn bộ dữ liệu")
            df_new = df_raw
            df_processed = None
    else:
        print("💡 Chưa có file đã xử lý, sẽ xử lý toàn bộ")
        df_new = df_raw
        df_processed = None
    
    # Bước 3: Tùy chọn xử lý
    print("\n🔧 TÙY CHỌN TIỀN XỬ LÝ:")
    print("1. Giữ nguyên tất cả từ")
    print("2. Loại bỏ stopwords (từ dừng)")
    choice = input("Nhập lựa chọn (mặc định 1): ").strip() or "1"
    remove_stopwords = (choice == "2")
    
    if remove_stopwords:
        print(f"✅ Sẽ loại bỏ {len(STOPWORDS)} stopwords")
    
    # Chọn trường cần xử lý
    print("\n📝 CHỌN TRƯỜNG CẦN XỬ LÝ:")
    print("1. Chỉ nội dung (content)")
    print("2. Tiêu đề + Nội dung (title + content)")
    print("3. Mô tả + Nội dung (description + content)")
    field_choice = input("Nhập lựa chọn (mặc định 1): ").strip() or "1"
    
    # Kết hợp các trường
    if field_choice == "2":
        df_new['text_to_process'] = df_new['title'].fillna('') + ' ' + df_new['content'].fillna('')
        print("✅ Sẽ xử lý: Tiêu đề + Nội dung")
    elif field_choice == "3" and 'description' in df_new.columns:
        df_new['text_to_process'] = df_new['description'].fillna('') + ' ' + df_new['content'].fillna('')
        print("✅ Sẽ xử lý: Mô tả + Nội dung")
    else:
        df_new['text_to_process'] = df_new['content'].fillna('')
        print("✅ Sẽ xử lý: Chỉ nội dung")
    
    # Bước 4: Tiền xử lý CHỈ NHỮNG BÀI MỚI
    print(f"\n🔄 Đang tiền xử lý {len(df_new):,} bài MỚI...")
    print("⏰ Thời gian ước tính:", f"~{len(df_new) * 0.5 / 60:.1f} phút" if len(df_new) > 100 else "< 1 phút")
    
    tqdm.pandas(desc="Processing")
    df_new['tokens'] = df_new['text_to_process'].progress_apply(
        lambda x: preprocess_text(x, remove_stopwords=remove_stopwords)
    )
    
    # Lọc bỏ các bài không có token
    original_count = len(df_new)
    df_new = df_new[df_new['tokens'].apply(len) > 0]
    removed_count = original_count - len(df_new)
    
    if removed_count > 0:
        print(f"⚠️ Đã loại bỏ {removed_count} bài không có nội dung")
    
    # Bước 5: GỘP VỚI DỮ LIỆU CŨ
    print(f"\n🔗 Đang gộp với dữ liệu đã xử lý...")
    
    # Xóa cột tạm
    df_new = df_new.drop(columns=['text_to_process'])
    
    if df_processed is not None and len(df_processed) > 0:
        df_final = pd.concat([df_processed, df_new], ignore_index=True)
        print(f"  • Dữ liệu cũ: {len(df_processed):,} bài")
        print(f"  • Dữ liệu mới: {len(df_new):,} bài")
        print(f"  • Tổng cộng: {len(df_final):,} bài")
    else:
        df_final = df_new
        print(f"  • Tổng cộng: {len(df_final):,} bài")
    
    # Bước 6: Phân tích thống kê
    print("\n📊 THỐNG KÊ DỮ LIỆU (SAU KHI XỬ LÝ):")
    print("-" * 80)
    stats = analyze_text_stats(df_final)
    print(f"  • Tổng số bài: {stats['total_articles']:,}")
    print(f"  • Tổng số từ: {stats['total_words']:,}")
    print(f"  • Trung bình: {stats['avg_words_per_article']:.1f} từ/bài")
    print(f"  • Bài ngắn nhất: {stats['min_words']} từ")
    print(f"  • Bài dài nhất: {stats['max_words']} từ")
    
    # Thống kê riêng cho dữ liệu mới
    if len(df_new) > 0:
        print(f"\n📊 THỐNG KÊ DỮ LIỆU MỚI (VỪA XỬ LÝ):")
        print("-" * 80)
        stats_new = analyze_text_stats(df_new)
        print(f"  • Số bài mới: {stats_new['total_articles']:,}")
        print(f"  • Tổng số từ: {stats_new['total_words']:,}")
        print(f"  • Trung bình: {stats_new['avg_words_per_article']:.1f} từ/bài")
    
    # Từ xuất hiện nhiều nhất (trong toàn bộ dữ liệu)
    from collections import Counter
    all_tokens = []
    for tokens in df_final['tokens']:
        all_tokens.extend(tokens)
    
    top_words = Counter(all_tokens).most_common(20)
    print(f"\n📈 TOP 20 TỪ XUẤT HIỆN NHIỀU NHẤT (TOÀN BỘ):")
    print("-" * 80)
    for i, (word, count) in enumerate(top_words, 1):
        print(f"  {i:2d}. {word:20s} | {count:6,d} lần")
    
    # Bước 7: Lưu kết quả
    print(f"\n💾 Đang lưu kết quả...")
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"✅ Đã lưu {len(df_final):,} bài vào {output_file}")
    print(f"💾 Kích thước file: {file_size:.2f} MB")
    
    # Lưu thống kê
    stats_file = "dataset/preprocessing_stats.txt"
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("THỐNG KÊ TIỀN XỬ LÝ DỮ LIỆU\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Tổng số bài: {stats['total_articles']:,}\n")
        f.write(f"Tổng số từ: {stats['total_words']:,}\n")
        f.write(f"Trung bình: {stats['avg_words_per_article']:.1f} từ/bài\n")
        f.write(f"Loại bỏ stopwords: {'Có' if remove_stopwords else 'Không'}\n\n")
        
        if len(df_new) > 0:
            f.write(f"Số bài MỚI vừa xử lý: {len(df_new):,}\n")
            f.write(f"Số bài CŨ: {len(df_processed) if df_processed is not None else 0:,}\n\n")
        
        f.write("TOP 20 TỪ XUẤT HIỆN NHIỀU NHẤT:\n")
        f.write("-" * 80 + "\n")
        for i, (word, count) in enumerate(top_words, 1):
            f.write(f"{i:2d}. {word:20s} | {count:6,d} lần\n")
    
    print(f"📄 Đã lưu thống kê vào {stats_file}")
    
    print("\n" + "=" * 80)
    print("🎉 HOÀN THÀNH!")
    print("=" * 80)
    
    # Tóm tắt
    print(f"\n📋 TÓM TẮT:")
    if df_processed is not None:
        print(f"  ✅ Đã xử lý {len(df_new):,} bài MỚI")
        print(f"  ✅ Giữ lại {len(df_processed):,} bài CŨ")
        print(f"  ✅ Tổng cộng: {len(df_final):,} bài trong file")
    else:
        print(f"  ✅ Đã xử lý {len(df_final):,} bài")
    
    print(f"\n💡 Bước tiếp theo: python build_ngram.py")
    print("=" * 80)

if __name__ == "__main__":
    main()