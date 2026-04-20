import pandas as pd
import ast
from collections import Counter
import json
import os
from build_ngram import build_ngrams_from_tokens, calculate_ngram_probability, find_collocations
from core.managers import build_manager

def run_ngram_builder(manager, n_values=[1, 2, 3, 4]):
    """
    Xây dựng mô hình N-gram chạy background.
    """
    manager.update(msg="🚀 Bắt đầu xây dựng mô hình N-gram...")
    input_file = "dataset/news_processed.csv"
    
    if not os.path.exists(input_file):
        manager.update(msg=f"❌ Không tìm thấy {input_file}")
        return
        
    manager.update(msg=f"📂 Đang đọc dữ liệu từ {input_file}...")
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        manager.update(msg=f"✅ Đã đọc {len(df)} bài báo")
    except Exception as e:
        manager.update(msg=f"❌ Lỗi đọc file: {e}")
        return
        
    all_models = {}
    total_tasks = len(n_values) * len(df)
    current_task = 0
    manager.update(total=total_tasks)
    
    for n in n_values:
        if manager.stop_event.is_set():
            manager.update(msg="⚠️ Đã dừng build N-gram!")
            return
            
        manager.update(msg=f"🔄 Đang xây dựng {n}-gram...")
        ngram_freq = Counter()
        total_ngrams_count = 0
        
        for idx, row in df.iterrows():
            if manager.stop_event.is_set():
                manager.update(msg="⚠️ Đã dừng build N-gram!")
                return
                
            tokens = ast.literal_eval(row['tokens']) if isinstance(row['tokens'], str) else row['tokens']
            doc_ngrams = build_ngrams_from_tokens(tokens, n)
            ngram_freq.update(doc_ngrams)
            total_ngrams_count += len(doc_ngrams)
            
            current_task += 1
            if current_task % 500 == 0:
                manager.update(progress=current_task)
                
        manager.update(msg=f"✅ Đã tạo {total_ngrams_count} {n}-grams, số duy nhất: {len(ngram_freq)}")
        
        ngram_prob = calculate_ngram_probability(ngram_freq, n)
        
        output_file = f"dataset/{n}gram_model.json"
        
        if n == 1:
            ngram_dict = {str(k): v for k, v in ngram_freq.items()}
            ngram_prob_dict = {str(k): v for k, v in ngram_prob.items()}
        else:
            ngram_dict = {" ".join(k): v for k, v in ngram_freq.items()}
            ngram_prob_dict = {" ".join(k): v for k, v in ngram_prob.items()}
            
        model_data = {
            "n": n,
            "total_ngrams": total_ngrams_count,
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
        
        if n == 2:
            collocations = find_collocations(ngram_freq, min_freq=5)
            model_data["collocations"] = {
                " ".join(k): v for k, v in sorted(collocations.items(), key=lambda x: x[1], reverse=True)[:50]
            }
            manager.update(msg=f"🔗 Tìm thấy {len(collocations)} collocations cho 2-gram")
            
        manager.update(msg=f"💾 Đang lưu {n}-gram vào {output_file} (dung lượng lớn có thể tốn tgian)...")    
        
        # Save async-like (can block, but acceptable)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, ensure_ascii=False, indent=2)
            
        manager.update(msg=f"💾 Đã lưu mô hình {n}-gram.")
        all_models[n] = {
            "total": total_ngrams_count,
            "unique": len(ngram_freq),
            "file": output_file
        }
        
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
            
    manager.update(progress=total_tasks, msg="🎉 Hoàn thành xây dựng toàn bộ mô hình N-gram!")
