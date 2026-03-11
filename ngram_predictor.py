import json
import random
from collections import defaultdict

class NgramPredictor:
    """Dự đoán từ tiếp theo dựa trên mô hình N-gram"""
    
    def __init__(self, ngram_model_file):
        """Khởi tạo predictor từ file mô hình"""
        with open(ngram_model_file, 'r', encoding='utf-8') as f:
            self.model = json.load(f)
        
        self.n = self.model['n']
        self.ngrams = self.model['ngrams']
        self.probabilities = self.model['probabilities']
        
        # Tạo dictionary để tra cứu nhanh
        self.context_dict = defaultdict(list)
        self._build_context_dict()
    
    def _build_context_dict(self):
        """Xây dựng dictionary context -> next_word"""
        for ngram_str, count in self.ngrams.items():
            words = ngram_str.split()
            if len(words) == self.n:
                context = ' '.join(words[:-1])  # Tất cả từ trừ từ cuối
                next_word = words[-1]
                self.context_dict[context].append((next_word, count))
        
        # Sắp xếp theo count giảm dần
        for context in self.context_dict:
            self.context_dict[context].sort(key=lambda x: x[1], reverse=True)
    
    def predict_next_word(self, context, top_k=5):
        """
        Dự đoán từ tiếp theo dựa trên context
        
        Args:
            context: Chuỗi từ đầu vào (ví dụ: "tp hcm")
            top_k: Số từ dự đoán trả về
            
        Returns:
            List các (word, probability) được sắp xếp theo xác suất
        """
        context = context.strip().lower()
        
        if context not in self.context_dict:
            return []
        
        candidates = self.context_dict[context]
        
        # Tính tổng count
        total_count = sum(count for _, count in candidates)
        
        # Tính xác suất
        predictions = []
        for word, count in candidates[:top_k]:
            probability = count / total_count
            predictions.append((word, probability))
        
        return predictions
    
    def generate_text(self, seed_text, num_words=20):
        """
        Tạo văn bản tự động từ seed text
        
        Args:
            seed_text: Văn bản khởi đầu
            num_words: Số từ muốn tạo
            
        Returns:
            Văn bản được tạo
        """
        words = seed_text.strip().lower().split()
        
        if len(words) < self.n - 1:
            return seed_text + " [Cần ít nhất {} từ để bắt đầu]".format(self.n - 1)
        
        result = words.copy()
        
        for _ in range(num_words):
            # Lấy context (n-1 từ cuối)
            context = ' '.join(result[-(self.n-1):])
            
            # Dự đoán từ tiếp theo
            predictions = self.predict_next_word(context, top_k=3)
            
            if not predictions:
                break
            
            # Chọn ngẫu nhiên có trọng số theo xác suất
            next_word = self._weighted_random_choice(predictions)
            result.append(next_word)
        
        return ' '.join(result)
    
    def _weighted_random_choice(self, predictions):
        """Chọn ngẫu nhiên có trọng số"""
        words = [w for w, _ in predictions]
        probs = [p for _, p in predictions]
        
        # Normalize probabilities
        total = sum(probs)
        probs = [p/total for p in probs]
        
        return random.choices(words, weights=probs)[0]


def main():
    """Demo sử dụng N-gram Predictor"""
    print("=" * 60)
    print("🤖 DỰ ĐOÁN TỪ TIẾP THEO VỚI MÔ HÌNH N-GRAM")
    print("=" * 60)
    
    # Chọn mô hình
    print("\n📚 Chọn mô hình:")
    print("1. Bigram (2-gram)")
    print("2. Trigram (3-gram)")
    print("3. 4-gram")
    
    choice = input("Nhập lựa chọn (mặc định 2): ").strip() or "2"
    
    model_files = {
        "1": "dataset/2gram_model.json",
        "2": "dataset/3gram_model.json",
        "3": "dataset/4gram_model.json"
    }
    
    model_file = model_files.get(choice, "dataset/3gram_model.json")
    
    try:
        predictor = NgramPredictor(model_file)
        print(f"\n✅ Đã tải mô hình {predictor.n}-gram")
    except FileNotFoundError:
        print(f"\n❌ Không tìm thấy file {model_file}")
        print("💡 Hãy chạy 'python build_ngram.py' trước!")
        return
    
    while True:
        print("\n" + "=" * 60)
        print("🎯 CHỌN CHỨC NĂNG:")
        print("1. Dự đoán từ tiếp theo")
        print("2. Tạo văn bản tự động")
        print("3. Thoát")
        
        func_choice = input("\nNhập lựa chọn: ").strip()
        
        if func_choice == "1":
            # Dự đoán từ tiếp theo
            print("\n" + "-" * 60)
            context = input(f"Nhập {predictor.n-1} từ: ").strip()
            
            if not context:
                print("⚠️ Bạn chưa nhập gì!")
                continue
            
            predictions = predictor.predict_next_word(context, top_k=10)
            
            if predictions:
                print(f"\n📈 Top 10 từ tiếp theo sau '{context}':")
                print("-" * 60)
                for i, (word, prob) in enumerate(predictions, 1):
                    print(f"{i:2d}. {word:20s} | {prob*100:6.2f}%")
            else:
                print(f"\n❌ Không tìm thấy dự đoán cho '{context}'")
                print("💡 Thử với các từ khác trong dataset!")
        
        elif func_choice == "2":
            # Tạo văn bản
            print("\n" + "-" * 60)
            seed = input(f"Nhập văn bản khởi đầu (ít nhất {predictor.n-1} từ): ").strip()
            
            if not seed:
                seed = "tp hcm"
                print(f"💡 Sử dụng seed mặc định: '{seed}'")
            
            num_words = input("Số từ muốn tạo (mặc định 30): ").strip()
            num_words = int(num_words) if num_words else 30
            
            print("\n📝 Đang tạo văn bản...")
            generated = predictor.generate_text(seed, num_words)
            
            print("\n✨ KẾT QUẢ:")
            print("-" * 60)
            print(generated)
            print("-" * 60)
        
        elif func_choice == "3":
            print("\n👋 Tạm biệt!")
            break
        
        else:
            print("\n⚠️ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
