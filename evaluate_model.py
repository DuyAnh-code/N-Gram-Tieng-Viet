import json
import pandas as pd
import ast
import math
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'DejaVu Sans'

class NgramEvaluator:
    """Đánh giá hiệu suất mô hình N-gram"""
    
    def __init__(self, ngram_model_file, test_data_file):
        """Khởi tạo evaluator"""
        # Load mô hình
        with open(ngram_model_file, 'r', encoding='utf-8') as f:
            self.model = json.load(f)
        
        self.n = self.model['n']
        self.ngrams = self.model['ngrams']
        self.probabilities = self.model['probabilities']
        
        # Load dữ liệu test (giới hạn 500 bài gần nhất để tránh timeout trên web)
        self.test_df = pd.read_csv(test_data_file, encoding='utf-8-sig').tail(500)
    
    def calculate_perplexity(self):
        """Tính Perplexity - độ đo quan trọng nhất cho mô hình ngôn ngữ"""
        total_log_prob = 0
        total_words = 0
        
        for idx, row in self.test_df.iterrows():
            tokens = ast.literal_eval(row['tokens']) if isinstance(row['tokens'], str) else row['tokens']
            
            # Tạo n-gram từ tokens
            for i in range(len(tokens) - self.n + 1):
                ngram = ' '.join(tokens[i:i+self.n])
                
                if ngram in self.probabilities:
                    prob = self.probabilities[ngram]
                    total_log_prob += math.log2(prob)
                else:
                    # Smoothing: gán xác suất nhỏ cho n-gram chưa thấy
                    total_log_prob += math.log2(1e-10)
                
                total_words += 1
        
        # Tính perplexity
        if total_words == 0:
            return float('inf')
        
        avg_log_prob = total_log_prob / total_words
        perplexity = 2 ** (-avg_log_prob)
        
        return perplexity
    
    def calculate_accuracy(self, top_k=5):
        """Tính độ chính xác trong việc dự đoán từ tiếp theo"""
        # Unigram không có context nên không thể dự đoán từ tiếp theo
        if self.n == 1:
            return 0.0, 0, 0

        correct = 0
        total = 0
        
        # Xây dựng context dict
        context_dict = {}
        for ngram_str, count in self.ngrams.items():
            words = ngram_str.split()
            if len(words) == self.n:
                context = ' '.join(words[:-1])
                next_word = words[-1]
                
                if context not in context_dict:
                    context_dict[context] = []
                context_dict[context].append((next_word, count))
        
        # Sắp xếp theo count
        for context in context_dict:
            context_dict[context].sort(key=lambda x: x[1], reverse=True)
        
        # Test trên dữ liệu
        for idx, row in self.test_df.iterrows():
            tokens = ast.literal_eval(row['tokens']) if isinstance(row['tokens'], str) else row['tokens']
            
            for i in range(len(tokens) - self.n + 1):
                context = ' '.join(tokens[i:i+self.n-1])
                actual_next = tokens[i+self.n-1]
                
                if context in context_dict:
                    # Lấy top-k dự đoán
                    predictions = [word for word, _ in context_dict[context][:top_k]]
                    
                    if actual_next in predictions:
                        correct += 1
                    
                    total += 1
        
        accuracy = correct / total if total > 0 else 0
        return accuracy, correct, total
    
    def get_coverage(self):
        """Tính coverage - tỷ lệ n-gram trong test set có trong mô hình"""
        seen = 0
        total = 0
        
        for idx, row in self.test_df.iterrows():
            tokens = ast.literal_eval(row['tokens']) if isinstance(row['tokens'], str) else row['tokens']
            
            for i in range(len(tokens) - self.n + 1):
                ngram = ' '.join(tokens[i:i+self.n])
                
                if ngram in self.ngrams:
                    seen += 1
                total += 1
        
        coverage = seen / total if total > 0 else 0
        return coverage, seen, total


def compare_models():
    """So sánh hiệu suất của các mô hình N-gram"""
    print("=" * 60)
    print("📊 SO SÁNH HIỆU SUẤT CÁC MÔ HÌNH N-GRAM")
    print("=" * 60)
    
    test_file = "dataset/news_processed.csv"
    
    models = {
        "Unigram": "dataset/1gram_model.json",
        "Bigram": "dataset/2gram_model.json",
        "Trigram": "dataset/3gram_model.json"
    }
    
    results = []
    
    for model_name, model_file in models.items():
        try:
            print(f"\n🔍 Đang đánh giá {model_name}...")
            evaluator = NgramEvaluator(model_file, test_file)
            
            # Tính các metrics
            perplexity = evaluator.calculate_perplexity()
            accuracy_top1, correct1, total1 = evaluator.calculate_accuracy(top_k=1)
            accuracy_top5, correct5, total5 = evaluator.calculate_accuracy(top_k=5)
            coverage, seen, total_ngrams = evaluator.get_coverage()
            
            results.append({
                "Model": model_name,
                "Perplexity": perplexity,
                "Accuracy@1": accuracy_top1 * 100,
                "Accuracy@5": accuracy_top5 * 100,
                "Coverage": coverage * 100,
                "Unique N-grams": evaluator.model['unique_ngrams']
            })
            
            print(f"  ✅ Perplexity: {perplexity:.2f}")
            print(f"  ✅ Accuracy@1: {accuracy_top1*100:.2f}%")
            print(f"  ✅ Accuracy@5: {accuracy_top5*100:.2f}%")
            print(f"  ✅ Coverage: {coverage*100:.2f}%")
            
        except FileNotFoundError:
            print(f"  ❌ Không tìm thấy file {model_file}")
            continue
    
    if not results:
        print("\n❌ Không có mô hình nào để đánh giá!")
        return
    
    # Hiển thị bảng so sánh
    print("\n" + "=" * 60)
    print("📈 BẢNG SO SÁNH CHI TIẾT")
    print("=" * 60)
    
    df_results = pd.DataFrame(results)
    print(df_results.to_string(index=False))
    
    # Lưu kết quả
    df_results.to_csv("dataset/model_comparison.csv", index=False, encoding='utf-8-sig')
    print(f"\n💾 Đã lưu kết quả vào dataset/model_comparison.csv")
    
    # Vẽ biểu đồ so sánh
    plot_comparison(df_results)


def plot_comparison(df):
    """Vẽ biểu đồ so sánh các mô hình"""
    print("\n📊 Đang tạo biểu đồ...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('So sanh hieu suat cac mo hinh N-gram', fontsize=16, fontweight='bold')
    
    # 1. Perplexity (càng thấp càng tốt)
    ax1 = axes[0, 0]
    ax1.bar(df['Model'], df['Perplexity'], color=['#3498db', '#2ecc71', '#e74c3c'])
    ax1.set_title('Perplexity (thap hon = tot hon)')
    ax1.set_ylabel('Perplexity')
    ax1.grid(axis='y', alpha=0.3)
    
    # 2. Accuracy@1
    ax2 = axes[0, 1]
    ax2.bar(df['Model'], df['Accuracy@1'], color=['#3498db', '#2ecc71', '#e74c3c'])
    ax2.set_title('Accuracy@1 (cao hon = tot hon)')
    ax2.set_ylabel('Accuracy (%)')
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Accuracy@5
    ax3 = axes[1, 0]
    ax3.bar(df['Model'], df['Accuracy@5'], color=['#3498db', '#2ecc71', '#e74c3c'])
    ax3.set_title('Accuracy@5 (cao hon = tot hon)')
    ax3.set_ylabel('Accuracy (%)')
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. Coverage
    ax4 = axes[1, 1]
    ax4.bar(df['Model'], df['Coverage'], color=['#3498db', '#2ecc71', '#e74c3c'])
    ax4.set_title('Coverage (cao hon = tot hon)')
    ax4.set_ylabel('Coverage (%)')
    ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('dataset/model_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Đã lưu biểu đồ vào dataset/model_comparison.png")
    
    try:
        plt.show()
    except:
        print("⚠️ Không thể hiển thị biểu đồ (có thể do môi trường không hỗ trợ GUI)")


def main():
    """Chương trình chính"""
    print("=" * 60)
    print("🎯 ĐÁNH GIÁ MÔ HÌNH N-GRAM")
    print("=" * 60)
    
    print("\n🔧 Chọn chức năng:")
    print("1. Đánh giá một mô hình cụ thể")
    print("2. So sánh tất cả các mô hình")
    
    choice = input("\nNhập lựa chọn (mặc định 2): ").strip() or "2"
    
    if choice == "1":
        print("\n📚 Chọn mô hình:")
        print("1. Unigram")
        print("2. Bigram")
        print("3. Trigram")
        
        model_choice = input("Nhập lựa chọn: ").strip()
        
        models = {
            "1": ("Unigram", "dataset/1gram_model.json"),
            "2": ("Bigram", "dataset/2gram_model.json"),
            "3": ("Trigram", "dataset/3gram_model.json")
        }
        
        if model_choice not in models:
            print("❌ Lựa chọn không hợp lệ!")
            return
        
        model_name, model_file = models[model_choice]
        test_file = "dataset/news_processed.csv"
        
        try:
            evaluator = NgramEvaluator(model_file, test_file)
            
            print(f"\n🔍 Đang đánh giá {model_name}...")
            
            perplexity = evaluator.calculate_perplexity()
            accuracy_top1, c1, t1 = evaluator.calculate_accuracy(top_k=1)
            accuracy_top5, c5, t5 = evaluator.calculate_accuracy(top_k=5)
            coverage, seen, total = evaluator.get_coverage()
            
            print("\n" + "=" * 60)
            print(f"📊 KẾT QUẢ ĐÁNH GIÁ - {model_name}")
            print("=" * 60)
            print(f"🎯 Perplexity: {perplexity:.2f}")
            print(f"   (Càng thấp càng tốt - đo độ \"bất ngờ\" của mô hình)")
            print(f"\n✅ Accuracy@1: {accuracy_top1*100:.2f}%")
            print(f"   (Dự đoán đúng từ tiếp theo trong top 1: {c1}/{t1})")
            print(f"\n✅ Accuracy@5: {accuracy_top5*100:.2f}%")
            print(f"   (Dự đoán đúng từ tiếp theo trong top 5: {c5}/{t5})")
            print(f"\n📈 Coverage: {coverage*100:.2f}%")
            print(f"   (Tỷ lệ n-gram xuất hiện trong mô hình: {seen}/{total})")
            
        except FileNotFoundError as e:
            print(f"\n❌ Lỗi: {e}")
    
    elif choice == "2":
        compare_models()
    
    else:
        print("❌ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
