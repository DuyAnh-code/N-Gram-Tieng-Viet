import os
import pandas as pd
from collections import Counter
from preprocess import preprocess_text, analyze_text_stats, STOPWORDS
from core.managers import preprocess_manager

def run_preprocessor(manager, remove_stopwords=False, field_choice="1"):
    """
    Tiền xử lý toàn bộ bài viết trong dataset/news.csv, cập nhật background progress.
    """
    manager.update(msg="🚀 Bắt đầu tiền xử lý dữ liệu...")
    
    input_file = "dataset/news.csv"
    output_file = "dataset/news_processed.csv"
    
    if not os.path.exists(input_file):
        manager.update(msg=f"❌ Không tìm thấy file {input_file}")
        return
        
    manager.update(msg=f"📂 Đang đọc dữ liệu từ {input_file}...")
    try:
        df_raw = pd.read_csv(input_file, encoding='utf-8-sig')
        manager.update(msg=f"✅ Đã đọc {len(df_raw)} bài từ file gốc")
    except Exception as e:
        manager.update(msg=f"❌ Lỗi đọc file: {e}")
        return

    df_new = df_raw.copy()
    
    # Kết hợp các trường
    if field_choice == "2":
        df_new['text_to_process'] = df_new['title'].fillna('') + ' ' + df_new['content'].fillna('')
        manager.update(msg="✅ Sẽ xử lý: Tiêu đề + Nội dung")
    elif field_choice == "3" and 'description' in df_new.columns:
        df_new['text_to_process'] = df_new['description'].fillna('') + ' ' + df_new['content'].fillna('')
        manager.update(msg="✅ Sẽ xử lý: Mô tả + Nội dung")
    else:
        df_new['text_to_process'] = df_new['content'].fillna('')
        manager.update(msg="✅ Sẽ xử lý: Chỉ nội dung")

    # Xử lý
    total_articles = len(df_new)
    manager.update(total=total_articles, msg=f"🔄 Đang tiền xử lý {total_articles} bài...")
    
    tokens_list = []
    
    for i, row in df_new.iterrows():
        if manager.stop_event.is_set():
            manager.update(msg="⚠️ Đã nhận lệnh dừng tiền xử lý!")
            return
            
        text = row['text_to_process']
        tokens = preprocess_text(text, remove_stopwords=remove_stopwords)
        tokens_list.append(tokens)
        
        # Cập nhật progress mỗi 100 bài
        if (i + 1) % 100 == 0 or i == total_articles - 1:
            manager.update(progress=i + 1)
            
    df_new['tokens'] = tokens_list
    
    # Lọc bỏ các bài không có token
    original_count = len(df_new)
    df_new = df_new[df_new['tokens'].apply(len) > 0]
    removed_count = original_count - len(df_new)
    
    if removed_count > 0:
        manager.update(msg=f"⚠️ Đã loại bỏ {removed_count} bài trống.")
        
    df_new = df_new.drop(columns=['text_to_process'])
    
    manager.update(msg="💾 Đang lưu kết quả vào CSV...")
    df_new.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    # Lưu file stats giống bản cũ
    stats = analyze_text_stats(df_new)
    all_tokens = []
    for tokens in df_new['tokens']:
        all_tokens.extend(tokens)
    top_words = Counter(all_tokens).most_common(20)
    
    stats_file = "dataset/preprocessing_stats.txt"
    try:
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write("THỐNG KÊ TIỀN XỬ LÝ DỮ LIỆU\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Tổng số bài: {stats['total_articles']:,}\n")
            f.write(f"Tổng số từ: {stats['total_words']:,}\n")
            f.write(f"Trung bình: {stats['avg_words_per_article']:.1f} từ/bài\n")
            f.write(f"Loại bỏ stopwords: {'Có' if remove_stopwords else 'Không'}\n\n")
            f.write("TOP 20 TỪ XUẤT HIỆN NHIỀU NHẤT:\n")
            f.write("-" * 80 + "\n")
            for i, (word, count) in enumerate(top_words, 1):
                f.write(f"{i:2d}. {word:20s} | {count:6,d} lần\n")
    except Exception as e:
        manager.update(msg=f"⚠️ Lỗi lưu stats: {e}")

    manager.update(msg=f"🎉 Hoàn thành! Đã lưu {len(df_new)} bài vào {output_file}.")
