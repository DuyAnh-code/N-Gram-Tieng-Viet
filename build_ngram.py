import pandas as pd
import ast
from nltk.util import ngrams
from collections import Counter
import json

def build_ngrams_from_tokens(tokens, n=2):
    """Xây dựng N-gram từ danh sách tokens"""
    if not tokens or len(tokens) < n:
        return []
    
    # Đặc biệt xử lý cho unigram (n=1)
    if n == 1:
        return tokens
    
    return list(ngrams(tokens, n))

def calculate_ngram_probability(ngram_freq, n):
    """Tính xác suất xuất hiện của N-gram"""
    total = sum(ngram_freq.values())
    ngram_prob = {k: v/total for k, v in ngram_freq.items()}
    return ngram_prob

def find_collocations(bigrams, min_freq=5):
    """Tìm các cặp từ thường xuất hiện cùng nhau (collocations)"""
    return {k: v for k, v in bigrams.items() if v >= min_freq}

def main():
    """Xây dựng mô hình N-gram từ dữ liệu đã xử lý"""
    print("=" * 60)
    print("📊 XÂY DỰNG MÔ HÌNH N-GRAM - PHIÊN BẢN MỞ RỘNG")
    print("=" * 60)
    
    # Đọc dữ liệu đã xử lý
    input_file = "dataset/news_processed.csv"
    print(f"\n📂 Đang đọc dữ liệu từ {input_file}...")
    
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        print(f"✅ Đã đọc {len(df)} bài báo")
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {input_file}")
        print("💡 Hãy chạy 'python preprocess.py' trước để tiền xử lý dữ liệu!")
        return
    
    # Chọn loại N-gram
    print("\n🔧 Chọn loại N-gram:")
    print("1. Unigram (1 từ)")
    print("2. Bigram (2 từ)")
    print("3. Trigram (3 từ)")
    print("4. 4-gram (4 từ)")
    print("5. Tất cả (1-4 gram)")
    n_choice = input("Nhập lựa chọn (mặc định 2 - Bigram): ").strip() or "2"
    
    # Xác định các loại N-gram cần xây dựng
    if n_choice == "5":
        n_values = [1, 2, 3, 4]
        print("✅ Sẽ xây dựng tất cả: Unigram, Bigram, Trigram, 4-gram")
    else:
        n_values = [int(n_choice)]
        names = {1: "Unigram", 2: "Bigram", 3: "Trigram", 4: "4-gram"}
        print(f"✅ Sẽ xây dựng: {names.get(n_values[0], f'{n_values[0]}-gram')}")
    
    # Xây dựng N-gram cho mỗi giá trị n
    all_models = {}
    
    for n in n_values:
        print(f"\n{'='*60}")
        print(f"🔄 Đang xây dựng {n}-gram...")
        print(f"{'='*60}")
        
        all_ngrams = []
        
        for idx, row in df.iterrows():
            # Chuyển string về list (vì CSV lưu list dưới dạng string)
            tokens = ast.literal_eval(row['tokens']) if isinstance(row['tokens'], str) else row['tokens']
            
            # Tạo N-gram
            doc_ngrams = build_ngrams_from_tokens(tokens, n)
            all_ngrams.extend(doc_ngrams)
        
        # Đếm tần suất
        ngram_freq = Counter(all_ngrams)
        
        print(f"✅ Đã tạo {len(all_ngrams):,} {n}-grams")
        print(f"✅ Số {n}-gram duy nhất: {len(ngram_freq):,}")
        
        # Hiển thị top N-gram phổ biến nhất
        top_n = 30
        print(f"\n📈 TOP {top_n} {n}-gram phổ biến nhất:")
        print("-" * 60)
        for i, (gram, count) in enumerate(ngram_freq.most_common(top_n), 1):
            # Xử lý hiển thị cho cả unigram và n-gram
            if n == 1:
                gram_str = str(gram)
            else:
                gram_str = " + ".join(gram)
            print(f"{i:2d}. {gram_str:40s} | {count:6,d} lần")
        
        # Tính xác suất
        ngram_prob = calculate_ngram_probability(ngram_freq, n)
        
        # Lưu kết quả
        output_file = f"dataset/{n}gram_model.json"
        
        # Chuyển đổi key cho JSON
        if n == 1:
            ngram_dict = {str(k): v for k, v in ngram_freq.items()}
            ngram_prob_dict = {str(k): v for k, v in ngram_prob.items()}
        else:
            ngram_dict = {" ".join(k): v for k, v in ngram_freq.items()}
            ngram_prob_dict = {" ".join(k): v for k, v in ngram_prob.items()}
        
        model_data = {
            "n": n,
            "total_ngrams": len(all_ngrams),
            "unique_ngrams": len(ngram_freq),
            "ngrams": ngram_dict,
            "probabilities": ngram_prob_dict,
            "top_30": [
                {
                    "ngram": str(k) if n == 1 else " ".join(k),
                    "count": v,
                    "probability": ngram_prob[k]
                }
                for k, v in ngram_freq.most_common(30)
            ]
        }
        
        # Thêm collocations cho bigram
        if n == 2:
            collocations = find_collocations(ngram_freq, min_freq=5)
            model_data["collocations"] = {
                " ".join(k): v for k, v in sorted(collocations.items(), key=lambda x: x[1], reverse=True)[:50]
            }
            print(f"\n🔗 Tìm thấy {len(collocations)} collocations (xuất hiện >= 5 lần)")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Đã lưu mô hình {n}-gram vào {output_file}")
        
        all_models[n] = {
            "total": len(all_ngrams),
            "unique": len(ngram_freq),
            "file": output_file
        }
    
    # Tạo báo cáo tổng hợp
    print(f"\n{'='*60}")
    print(f"📋 TẠO BÁO CÁO TỔNG HỢP")
    print(f"{'='*60}")
    
    report_file = "dataset/ngram_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("BÁO CÁO MÔ HÌNH N-GRAM\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Tổng số bài báo: {len(df)}\n\n")
        
        for n, info in all_models.items():
            f.write(f"\n{n}-GRAM:\n")
            f.write("-" * 60 + "\n")
            f.write(f"Tổng số {n}-gram: {info['total']:,}\n")
            f.write(f"Số {n}-gram duy nhất: {info['unique']:,}\n")
            f.write(f"File: {info['file']}\n")
    
    print(f"✅ Đã lưu báo cáo vào {report_file}")
    
    # Thống kê cuối cùng
    print(f"\n{'='*60}")
    print("🎉 HOÀN THÀNH!")
    print(f"{'='*60}")
    print(f"\n📊 TỔNG KẾT:")
    for n, info in all_models.items():
        print(f"  • {n}-gram: {info['total']:,} total, {info['unique']:,} unique")
    
    print(f"\n📁 CÁC FILE ĐÃ TẠO:")
    for n in all_models.keys():
        print(f"  • dataset/{n}gram_model.json")
    print(f"  • {report_file}")
    
    print(f"\n💡 BẠN CÓ THỂ:")
    print(f"  1. Xem file JSON để phân tích N-gram")
    print(f"  2. Sử dụng mô hình để dự đoán từ tiếp theo")
    print(f"  3. Tìm kiếm các cụm từ thường gặp (collocations)")

if __name__ == "__main__":
    main()