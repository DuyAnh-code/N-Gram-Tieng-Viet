from evaluate_model import NgramEvaluator
import os
import pandas as pd

def run_evaluation(model_name, n_values=[1, 2, 3]):
    results = []
    test_file = "dataset/news_processed.csv"
    
    if not os.path.exists(test_file):
        return {"error": "Không tìm thấy file dataset/news_processed.csv. Vui lòng chạy tiền xử lý trước!"}
        
    for n in n_values:
        model_file = f"dataset/{n}gram_model.json"
        try:
            evaluator = NgramEvaluator(model_file, test_file)
            
            perplexity = evaluator.calculate_perplexity()
            accuracy_top1, _, _ = evaluator.calculate_accuracy(top_k=1)
            accuracy_top5, _, _ = evaluator.calculate_accuracy(top_k=5)
            coverage, _, _ = evaluator.get_coverage()
            
            results.append({
                "n": n,
                "model_name": f"{n}-gram",
                "perplexity": round(perplexity, 2) if perplexity != float('inf') else -1,
                "accuracy_top1": round(accuracy_top1 * 100, 2),
                "accuracy_top5": round(accuracy_top5 * 100, 2),
                "coverage": round(coverage * 100, 2),
                "unique_ngrams": evaluator.model['unique_ngrams']
            })
        except Exception as e:
            results.append({
                "n": n,
                "model_name": f"{n}-gram",
                "error": str(e)
            })
            
    return {"results": results}
