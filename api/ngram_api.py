from flask import Blueprint, jsonify, request
from core.managers import build_manager
from core.ngram_builder import run_ngram_builder
import os
import json

ngram_api = Blueprint('ngram_api', __name__)

@ngram_api.route('/build', methods=['POST'])
def start_build():
    data = request.json or {}
    n_values = data.get('n_values', [1, 2, 3, 4])
    if build_manager.start(run_ngram_builder, n_values=n_values):
        return jsonify({"status": "started", "message": "Đang build N-gram"})
    return jsonify({"status": "error", "message": "Đang chay"}), 400

@ngram_api.route('/stop', methods=['POST'])
def stop_build():
    if build_manager.stop():
        return jsonify({"status": "stopped", "message": "Đang dừng..."})
    return jsonify({"status": "error", "message": "Không chạy"}), 400

@ngram_api.route('/status', methods=['GET'])
def get_status():
    return jsonify(build_manager.status)
    
@ngram_api.route('/top', methods=['GET'])
def get_top():
    n = int(request.args.get('n', 2))
    limit = int(request.args.get('limit', 30))
    model_file = f"dataset/{n}gram_model.json"
    if not os.path.exists(model_file):
        return jsonify({"error": f"Mô hình {n}-gram chưa được xây dựng"}), 404
        
    try:
        with open(model_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        top_list = data.get("top_30", [])[:limit]
        for item in top_list:
            item["ngram"] = item["ngram"].replace("_", " ")
        return jsonify({"top": top_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
