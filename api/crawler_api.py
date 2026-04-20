from flask import Blueprint, jsonify, request
from core.managers import crawler_manager
from core.crawler import run_crawler

crawler_api = Blueprint('crawler_api', __name__)

@crawler_api.route('/start', methods=['POST'])
def start_crawl():
    data = request.json or {}
    limit = data.get('limit', 1)
    if crawler_manager.start(run_crawler, limit_pages=limit):
        return jsonify({"status": "started", "message": "Crawler đã bắt đầu"})
    return jsonify({"status": "error", "message": "Crawler đang chạy"}), 400

@crawler_api.route('/stop', methods=['POST'])
def stop_crawl():
    if crawler_manager.stop():
        return jsonify({"status": "stopped", "message": "Đang dừng crawler..."})
    return jsonify({"status": "error", "message": "Crawler không chạy"}), 400

@crawler_api.route('/status', methods=['GET'])
def get_status():
    return jsonify(crawler_manager.status)
