from flask import Blueprint, jsonify
from core.managers import build_manager
import threading
import visualize
import matplotlib

# Must set Agg for Flask safety
matplotlib.use('Agg')

visualize_api = Blueprint('visualize_api', __name__)

class VisualizeManager:
    def __init__(self):
        self.is_running = False
        self.status = {"is_running": False, "message": "Đang chờ..."}
        
    def generate(self):
        if self.is_running:
            return False
            
        self.is_running = True
        self.status = {"is_running": True, "message": "Đang vẽ biểu đồ..."}
        
        thread = threading.Thread(target=self._run_visualization)
        thread.start()
        return True
        
    def _run_visualization(self):
        try:
            self.status["message"] = "Đang dọn dẹp ảnh cũ..."
            visualize.clean_old_visualizations()
            
            self.status["message"] = "Đang tạo biểu đồ so sánh mô hình (1/2)..."
            # Hotpatch visualize models to remove underscores
            models_data = visualize.create_model_comparison_chart()
            
            self.status["message"] = "Đang tạo biểu đồ phân tích từ vựng (2/2)..."
            visualize.create_vocabulary_analysis_chart()
            
            self.status["is_running"] = False
            self.status["message"] = "✅ Vẽ biểu đồ hoàn tất!"
        except Exception as e:
            self.status["is_running"] = False
            self.status["message"] = f"❌ Lỗi: {str(e)}"
            
vis_manager = VisualizeManager()

@visualize_api.route('/generate', methods=['POST'])
def generate_charts():
    if vis_manager.generate():
        return jsonify({"status": "started", "message": "Đang khởi tạo vẽ biểu đồ"})
    return jsonify({"status": "error", "message": "Đang chạy"}), 400

@visualize_api.route('/status', methods=['GET'])
def get_status():
    return jsonify(vis_manager.status)
