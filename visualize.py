import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from collections import Counter
import ast
import os
import glob

# Cấu hình font và style cho tiếng Việt
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
sns.set_palette("husl")

def clean_old_visualizations():
    """Xóa tất cả biểu đồ cũ trong thư mục dataset"""
    print("\n🗑️  Đang xóa các biểu đồ cũ...")
    png_files = glob.glob("dataset/*.png")
    
    if png_files:
        for file in png_files:
            try:
                os.remove(file)
                print(f"  ✅ Đã xóa: {os.path.basename(file)}")
            except Exception as e:
                print(f"  ⚠️ Không thể xóa {os.path.basename(file)}: {e}")
        print(f"✅ Đã xóa {len(png_files)} biểu đồ cũ\n")
    else:
        print("  💡 Không có biểu đồ cũ nào\n")

def create_model_comparison_chart():
    """Tạo biểu đồ so sánh hiệu suất các mô hình N-gram - TỈ MỈ & CHI TIẾT"""
    print("=" * 80)
    print("📊 BIỂU ĐỒ 1: SO SÁNH HIỆU SUẤT MÔ HÌNH N-GRAM")
    print("=" * 80)
    
    # Đọc dữ liệu từ các mô hình
    models_data = []
    
    for n in [1, 2, 3, 4]:
        model_file = f"dataset/{n}gram_model.json"
        try:
            with open(model_file, 'r', encoding='utf-8') as f:
                model = json.load(f)
                
            models_data.append({
                'model': f'{n}-gram',
                'n': n,
                'vocab_size': model.get('vocab_size', len(model.get('ngrams', {}))),
                'total_ngrams': len(model.get('ngrams', {})),
            })
            print(f"  ✅ Đã tải mô hình {n}-gram")
        except FileNotFoundError:
            print(f"  ⚠️ Không tìm thấy {model_file}")
    
    if not models_data:
        print("❌ Không tìm thấy mô hình nào!")
        return
    
    # Tạo biểu đồ với 2 subplot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    fig.suptitle('SO SÁNH HIỆU SUẤT CÁC MÔ HÌNH N-GRAM', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Subplot 1: Kích thước từ vựng
    models = [d['model'] for d in models_data]
    vocab_sizes = [d['vocab_size'] for d in models_data]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    bars1 = ax1.bar(models, vocab_sizes, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax1.set_ylabel('Kích thước từ vựng', fontsize=13, fontweight='bold')
    ax1.set_title('Kích thước từ vựng theo mô hình', fontsize=14, fontweight='bold', pad=15)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Thêm giá trị trên mỗi cột
    for i, (bar, val) in enumerate(zip(bars1, vocab_sizes)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:,}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Subplot 2: Tổng số N-gram
    total_ngrams = [d['total_ngrams'] for d in models_data]
    bars2 = ax2.bar(models, total_ngrams, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax2.set_ylabel('Số lượng N-gram duy nhất', fontsize=13, fontweight='bold')
    ax2.set_title('Số lượng N-gram duy nhất theo mô hình', fontsize=14, fontweight='bold', pad=15)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Thêm giá trị trên mỗi cột
    for i, (bar, val) in enumerate(zip(bars2, total_ngrams)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:,}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Thêm chú thích
    fig.text(0.5, 0.02, '💡 Mô hình N-gram càng cao thì càng nắm bắt được ngữ cảnh tốt hơn', 
             ha='center', fontsize=11, style='italic', color='gray')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    save_path = "dataset/model_comparison_detailed.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✅ Đã lưu vào {save_path}")
    plt.close()
    
    return models_data

def create_vocabulary_analysis_chart():
    """Tạo biểu đồ phân tích từ vựng - TỈ MỈ & CHI TIẾT"""
    print("\n" + "=" * 80)
    print("📊 BIỂU ĐỒ 2: PHÂN TÍCH TỪ VỰNG VÀ N-GRAM PHỔ BIẾN")
    print("=" * 80)
    
    csv_file = "dataset/news_processed.csv"
    
    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        print(f"  ✅ Đã đọc {len(df):,} bài báo")
    except FileNotFoundError:
        print(f"  ❌ Không tìm thấy {csv_file}")
        return
    
    # Chuẩn bị dữ liệu
    all_tokens = []
    for tokens in df['tokens']:
        if isinstance(tokens, str):
            tokens = ast.literal_eval(tokens)
        all_tokens.extend(tokens)
    
    words_freq = Counter(all_tokens)
    print(f"  📊 Tổng số từ: {len(all_tokens):,}")
    print(f"  📊 Số từ duy nhất: {len(words_freq):,}")
    
    # Tạo biểu đồ với 2 subplot
    fig = plt.figure(figsize=(18, 8))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1], hspace=0.3, wspace=0.3)
    
    fig.suptitle('PHÂN TÍCH TỪ VỰNG VÀ N-GRAM PHỔ BIẾN', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Subplot 1: Top 20 từ phổ biến nhất (chiếm 2 cột)
    ax1 = fig.add_subplot(gs[0, :])
    top_words = words_freq.most_common(20)
    words = [str(w).replace('_', ' ') for w, _ in top_words]
    counts = [c for _, c in top_words]
    
    colors_gradient = plt.cm.viridis(range(len(words)))
    bars = ax1.barh(range(len(words)), counts, color=colors_gradient, 
                    alpha=0.85, edgecolor='black', linewidth=1.2)
    
    ax1.set_yticks(range(len(words)))
    ax1.set_yticklabels(words, fontsize=11)
    ax1.set_xlabel('Tần suất xuất hiện', fontsize=12, fontweight='bold')
    ax1.set_title('Top 20 từ xuất hiện nhiều nhất trong corpus', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.invert_yaxis()
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Thêm giá trị
    for i, (word, count) in enumerate(top_words):
        ax1.text(count, i, f'  {count:,}', va='center', fontsize=10, fontweight='bold')
    
    # Subplot 2: Phân phối tần suất từ (Log scale)
    ax2 = fig.add_subplot(gs[1, 0])
    frequencies = list(words_freq.values())
    ax2.hist(frequencies, bins=50, color='#4ECDC4', edgecolor='black', alpha=0.7, linewidth=1)
    ax2.set_xlabel('Tần suất', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Số lượng từ', fontsize=11, fontweight='bold')
    ax2.set_title('Phân phối tần suất từ (Log scale)', fontsize=12, fontweight='bold', pad=10)
    ax2.set_yscale('log')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Subplot 3: Top 10 Bigram phổ biến
    ax3 = fig.add_subplot(gs[1, 1])
    
    try:
        with open('dataset/2gram_model.json', 'r', encoding='utf-8') as f:
            bigram_model = json.load(f)
        
        bigrams = bigram_model.get('ngrams', {})
        top_bigrams = sorted(bigrams.items(), key=lambda x: x[1], reverse=True)[:10]
        
        bigram_labels = [k.replace('_', ' ') for k, _ in top_bigrams]
        
        bigram_counts = [v for _, v in top_bigrams]
        
        colors_bigram = plt.cm.plasma(range(len(bigram_labels)))
        bars3 = ax3.barh(range(len(bigram_labels)), bigram_counts, 
                        color=colors_bigram, alpha=0.85, edgecolor='black', linewidth=1.2)
        
        ax3.set_yticks(range(len(bigram_labels)))
        ax3.set_yticklabels(bigram_labels, fontsize=9)
        ax3.set_xlabel('Tần suất', fontsize=11, fontweight='bold')
        ax3.set_title('Top 10 Bigram phổ biến nhất', fontsize=12, fontweight='bold', pad=10)
        ax3.invert_yaxis()
        ax3.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Thêm giá trị
        for i, count in enumerate(bigram_counts):
            ax3.text(count, i, f'  {count:,}', va='center', fontsize=9, fontweight='bold')
            
    except FileNotFoundError:
        ax3.text(0.5, 0.5, 'Chưa có dữ liệu Bigram\nChạy build_ngram.py trước', 
                ha='center', va='center', fontsize=12, style='italic')
        ax3.axis('off')
    except Exception as e:
        ax3.text(0.5, 0.5, f'Lỗi khi tải Bigram:\n{str(e)}', 
                ha='center', va='center', fontsize=10, style='italic', color='red')
        ax3.axis('off')
    
    # Thêm chú thích tổng quan
    stats_text = f"""
    📈 THỐNG KÊ TỔNG QUAN:
    • Tổng số từ: {len(all_tokens):,}
    • Số từ duy nhất: {len(words_freq):,}
    • Từ phổ biến nhất: "{top_words[0][0]}" ({top_words[0][1]:,} lần)
    • Tỷ lệ từ duy nhất: {len(words_freq)/len(all_tokens)*100:.2f}%
    """
    
    fig.text(0.5, 0.01, stats_text, ha='center', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout(rect=[0, 0.06, 1, 0.96])
    save_path = "dataset/vocabulary_analysis.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✅ Đã lưu vào {save_path}")
    plt.close()

def main():
    """Chương trình chính - Chỉ tạo 2 biểu đồ chất lượng cao"""
    print("=" * 80)
    print("📊 TRỰC QUAN HÓA DỮ LIỆU N-GRAM - PHIÊN BẢN TỈ MỈ")
    print("=" * 80)
    print("💡 Chỉ tạo 2 biểu đồ chất lượng cao, xóa biểu đồ cũ")
    print("=" * 80)
    
    # Bước 1: Xóa tất cả biểu đồ cũ
    clean_old_visualizations()
    
    # Bước 2: Tạo biểu đồ 1 - So sánh mô hình
    models_data = create_model_comparison_chart()
    
    # Bước 3: Tạo biểu đồ 2 - Phân tích từ vựng
    create_vocabulary_analysis_chart()
    
    # Tổng kết
    print("\n" + "=" * 80)
    print("🎉 HOÀN THÀNH!")
    print("=" * 80)
    print("\n📁 CÁC FILE ĐÃ TẠO:")
    print("  1️⃣ dataset/model_comparison_detailed.png")
    print("     → So sánh hiệu suất các mô hình N-gram")
    print("\n  2️⃣ dataset/vocabulary_analysis_detailed.png")
    print("     → Phân tích từ vựng và N-gram phổ biến")
    print("\n💡 2 biểu đồ chất lượng cao, độ phân giải 300 DPI")
    print("💡 Sẵn sàng sử dụng trong báo cáo/bài thuyết trình!")
    print("=" * 80)

if __name__ == "__main__":
    main()
