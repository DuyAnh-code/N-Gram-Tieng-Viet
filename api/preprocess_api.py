from flask import Blueprint, jsonify, request
from core.managers import preprocess_manager
from core.preprocessor import run_preprocessor

preprocess_api = Blueprint('preprocess_api', __name__)

@preprocess_api.route('/run', methods=['POST'])
def start_preprocess():
    data = request.json or {}
    remove_stop = data.get('remove_stopwords', False)
    field = str(data.get('field_choice', 1))
    
    if preprocess_manager.start(run_preprocessor, remove_stopwords=remove_stop, field_choice=field):
        return jsonify({"status": "started", "message": "Bắt đầu preprocessing"})
    return jsonify({"status": "error", "message": "Đang chạy"}), 400

@preprocess_api.route('/stop', methods=['POST'])
def stop_preprocess():
    if preprocess_manager.stop():
        return jsonify({"status": "stopped", "message": "Đang dừng..."})
    return jsonify({"status": "error", "message": "Không chạy"}), 400

@preprocess_api.route('/status', methods=['GET'])
def get_status():
    return jsonify(preprocess_manager.status)
