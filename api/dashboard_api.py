from flask import Blueprint, jsonify
import os
import pandas as pd
import json

dashboard_api = Blueprint('dashboard_api', __name__)

@dashboard_api.route('/stats', methods=['GET'])
def get_stats():
    stats = {
        "dataset_size": 0,
        "processed_size": 0,
        "models": [],
        "vocab_size": 0
    }
    
    try:
        if os.path.exists("dataset/news.csv"):
            df = pd.read_csv("dataset/news.csv", encoding='utf-8-sig', usecols=['url'])
            stats["dataset_size"] = len(df)
            
        if os.path.exists("dataset/news_processed.csv"):
            df = pd.read_csv("dataset/news_processed.csv", encoding='utf-8-sig', usecols=['url'])
            stats["processed_size"] = len(df)
            
        for n in [1, 2, 3, 4]:
            model_file = f"dataset/{n}gram_model.json"
            if os.path.exists(model_file):
                size_mb = os.path.getsize(model_file) / (1024 * 1024)
                stats["models"].append({
                    "n": n,
                    "size_mb": round(size_mb, 2)
                })
                if n == 1:
                    with open(model_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        stats["vocab_size"] = data.get("unique_ngrams", 0)
    except Exception as e:
        stats["error"] = str(e)
        
    return jsonify(stats)
