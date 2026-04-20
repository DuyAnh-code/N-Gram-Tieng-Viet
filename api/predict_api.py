from flask import Blueprint, jsonify, request
from core.predictor import NgramPredictorWrapper

predict_api = Blueprint('predict_api', __name__)
predictors = {}

def get_predictor(n):
    if n not in predictors:
        predictors[n] = NgramPredictorWrapper(n)
    return predictors[n]

@predict_api.route('/next_word', methods=['POST'])
def predict_next():
    data = request.json or {}
    context = data.get('context', '')
    n = int(data.get('n', 2))
    top_k = int(data.get('top_k', 5))
    
    predictor = get_predictor(n)
    if not predictor.model:
        return jsonify({"error": f"Mô hình {n}-gram chưa được xây dựng"}), 404
        
    preds = predictor.predict_next_word(context, top_k)
    return jsonify({"predictions": [{"word": w, "prob": p} for w, p in preds]})

@predict_api.route('/generate', methods=['POST'])
def generate_text():
    data = request.json or {}
    seed = data.get('seed', 'tp hcm')
    n = int(data.get('n', 2))
    num_words = int(data.get('num_words', 20))
    
    predictor = get_predictor(n)
    if not predictor.model:
        return jsonify({"error": f"Mô hình {n}-gram chưa được xây dựng"}), 404
        
    text = predictor.generate_text(seed, num_words)
    return jsonify({"generated_text": text})
