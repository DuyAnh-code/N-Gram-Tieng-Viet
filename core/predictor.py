import json
import random
from collections import defaultdict
import os
from underthesea import word_tokenize

class NgramPredictorWrapper:
    """Wrapper cho NgramPredictor"""
    
    def __init__(self, n=2):
        self.load_model(n)

    def load_model(self, n):
        self.n = n
        model_files = {
            1: "dataset/1gram_model.json",
            2: "dataset/2gram_model.json",
            3: "dataset/3gram_model.json",
            4: "dataset/4gram_model.json"
        }
        model_file = model_files.get(n, "dataset/2gram_model.json")
        
        if not os.path.exists(model_file):
            self.model = None
            self.ngrams = {}
            self.probabilities = {}
            self.context_dict = defaultdict(list)
            return
            
        with open(model_file, 'r', encoding='utf-8') as f:
            self.model = json.load(f)
            
        self.ngrams = self.model['ngrams']
        self.probabilities = self.model['probabilities']
        
        self.context_dict = defaultdict(list)
        self._build_context_dict()

    def _build_context_dict(self):
        if self.n == 1:
            return

        for ngram_str, count in self.ngrams.items():
            words = ngram_str.split()
            if len(words) == self.n:
                context = ' '.join(words[:-1])
                next_word = words[-1]
                self.context_dict[context].append((next_word, count))
        
        for context in self.context_dict:
            self.context_dict[context].sort(key=lambda x: x[1], reverse=True)
            
    def predict_next_word(self, context, top_k=5):
        if not self.model:
            return []
            
        if self.n == 1:
            top_unigrams = sorted(self.ngrams.items(), key=lambda x: x[1], reverse=True)[:top_k]
            total = sum(self.ngrams.values())
            return [(w.replace('_', ' '), c / total) for w, c in top_unigrams]

        context = context.strip().lower()
        context = " ".join(word_tokenize(context, format="text").split())
        
        if context not in self.context_dict:
            return []
            
        candidates = self.context_dict[context]
        total_count = sum(count for _, count in candidates)
        
        predictions = []
        for word, count in candidates[:top_k]:
            probability = count / total_count
            predictions.append((word.replace('_', ' '), probability))
            
        return predictions

    def generate_text(self, seed_text, num_words=20):
        if not self.model:
            return ""
            
        seed_tokens = word_tokenize(seed_text.strip().lower(), format="text").split()
        words = [w.replace('_', ' ') for w in seed_tokens]
        
        if len(words) < self.n - 1:
            return seed_text + f" [Cần {self.n - 1} từ để dự đoán (cho mô hình {self.n}-gram)]"
            
        result = words.copy()
        
        for _ in range(num_words):
            context = ' '.join(result[-(self.n-1):])
            predictions = self.predict_next_word(context, top_k=3)
            
            if not predictions:
                break
                
            next_word = self._weighted_random_choice(predictions)
            result.append(next_word)
            
        return ' '.join(result)

    def _weighted_random_choice(self, predictions):
        words = [w for w, _ in predictions]
        probs = [p for _, p in predictions]
        total = sum(probs)
        probs = [p/total for p in probs]
        return random.choices(words, weights=probs)[0]
