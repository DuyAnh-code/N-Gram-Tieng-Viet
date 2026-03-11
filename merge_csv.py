"""
SCRIPT GỘP TẤT CẢ FILE CSV HIỆN CÓ
Gộp news.csv, news_large_dataset.csv và các file CSV khác thành 1 file duy nhất
"""

import pandas as pd
import os
from datetime import datetime

def merge_all_csv():
    """Gộp tất cả file CSV trong dataset"""
    
    print("=" * 80)
    print("🔄 GỘP TẤT CẢ FILE CSV HIỆN CÓ")
    print("=" * 80)
    
    dataset_dir = "dataset"
    
    # Danh sách các file CSV cần gộp (không bao gồm file đã xử lý)
    csv_files = [
        "news.csv",
        "news_large_dataset.csv",
    ]
    
    # Tìm tất cả file CSV trong thư mục (ngoại trừ processed và model)
    print("\n🔍 Đang tìm kiếm file CSV...")
    available_files = []
    
    for filename in os.listdir(dataset_dir):
        if filename.endswith('.csv'):
            # Bỏ qua file đã xử lý và file so sánh
            if 'processed' not in filename and 'comparison' not in filename:
                filepath = os.path.join(dataset_dir, filename)
                if os.path.exists(filepath):
                    file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
                    available_files.append({
                        'name': filename,
                        'path': filepath,
                        'size': file_size
                    })
                    print(f"  ✅ {filename:30s} ({file_size:.2f} MB)")
    
    if not available_files:
        print("\n❌ Không tìm thấy file CSV nào để gộp!")
        return
    
    print(f"\n📊 Tìm thấy {len(available_files)} file CSV")
    
    # Hỏi xác nhận
    confirm = input("\n⚠️ Gộp tất cả file này thành 1 file? (y/n, mặc định y): ").strip().lower() or "y"
    if confirm != 'y':
        print("❌ Hủy bỏ!")
        return
    
    # Đọc và gộp tất cả file
    print(f"\n🔄 Đang gộp {len(available_files)} file...")
    print("-" * 80)
    
    all_dfs = []
    total_articles = 0
    
    for file_info in available_files:
        try:
            print(f"\n📖 Đang đọc: {file_info['name']}")
            df = pd.read_csv(file_info['path'], encoding='utf-8-sig')
            print(f"  • Số bài: {len(df):,}")
            
            # Kiểm tra các cột cần thiết
            required_cols = ['title', 'content', 'url']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                print(f"  ⚠️ Thiếu cột: {missing_cols} - Bỏ qua file này")
                continue
            
            all_dfs.append(df)
            total_articles += len(df)
            print(f"  ✅ Đã đọc thành công")
            
        except Exception as e:
            print(f"  ❌ Lỗi: {e}")
            continue
    
    if not all_dfs:
        print("\n❌ Không thể đọc file CSV nào!")
        return
    
    # Gộp tất cả DataFrame
    print(f"\n{'='*80}")
    print("🔗 ĐANG GỘP DỮ LIỆU")
    print("=" * 80)
    
    df_merged = pd.concat(all_dfs, ignore_index=True)
    print(f"\n  • Tổng số bài sau gộp: {len(df_merged):,}")
    
    # Loại bỏ trùng lặp theo URL
    print(f"\n🔍 Đang loại bỏ trùng lặp...")
    original_count = len(df_merged)
    df_merged = df_merged.drop_duplicates(subset=['url'], keep='first')
    duplicate_count = original_count - len(df_merged)
    
    print(f"  • Số bài trùng lặp: {duplicate_count:,}")
    print(f"  • Số bài sau khi loại trùng: {len(df_merged):,}")
    
    # Sao lưu file cũ
    print(f"\n💾 ĐANG SAO LƯU VÀ LƯU FILE MỚI")
    print("=" * 80)
    
    output_file = os.path.join(dataset_dir, "news.csv")
    backup_dir = os.path.join(dataset_dir, "backup")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup các file cũ
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for file_info in available_files:
        backup_path = os.path.join(backup_dir, f"{os.path.splitext(file_info['name'])[0]}_{timestamp}.csv")
        try:
            # Copy file sang backup
            df_backup = pd.read_csv(file_info['path'], encoding='utf-8-sig')
            df_backup.to_csv(backup_path, index=False, encoding='utf-8-sig')
            print(f"  ✅ Đã sao lưu: {file_info['name']} → backup/")
        except Exception as e:
            print(f"  ⚠️ Không thể sao lưu {file_info['name']}: {e}")
    
    # Lưu file gộp
    df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"\n✅ ĐÃ GỘP THÀNH CÔNG!")
    print(f"  📁 File: {output_file}")
    print(f"  📊 Tổng số bài: {len(df_merged):,}")
    print(f"  💾 Kích thước: {file_size:.2f} MB")
    
    # Thống kê
    if 'source' in df_merged.columns:
        print(f"\n📊 THỐNG KÊ THEO NGUỒN:")
        print("-" * 60)
        for source, count in df_merged['source'].value_counts().items():
            print(f"  {source:20s}: {count:6,d} bài ({count/len(df_merged)*100:.1f}%)")
    
    # Hỏi có xóa file cũ không
    print(f"\n🗑️  XÓA FILE CŨ?")
    print("-" * 60)
    print(f"  Các file cũ đã được sao lưu vào thư mục: {backup_dir}")
    delete_old = input("  Xóa các file CSV cũ? (y/n, mặc định n): ").strip().lower()
    
    if delete_old == 'y':
        for file_info in available_files:
            if file_info['path'] != output_file:  # Không xóa file output
                try:
                    os.remove(file_info['path'])
                    print(f"  ✅ Đã xóa: {file_info['name']}")
                except Exception as e:
                    print(f"  ❌ Lỗi xóa {file_info['name']}: {e}")
    else:
        print("  💡 Giữ lại các file cũ (có thể xóa thủ công sau)")
    
    print(f"\n💡 BƯỚC TIẾP THEO:")
    print(f"  1. python crawler.py            # Crawl thêm dữ liệu (sẽ tự động gộp vào)")
    print(f"  2. python preprocess.py         # Tiền xử lý dữ liệu")
    print(f"  3. python build_ngram.py        # Xây dựng mô hình")
    
    print("\n" + "=" * 80)
    print("🎉 HOÀN THÀNH!")
    print("=" * 80)

if __name__ == "__main__":
    try:
        merge_all_csv()
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
