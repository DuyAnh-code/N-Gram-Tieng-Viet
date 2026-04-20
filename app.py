import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from api.crawler_api import crawler_api
from api.preprocess_api import preprocess_api
from api.ngram_api import ngram_api
from api.predict_api import predict_api
from api.evaluate_api import evaluate_api
from api.dashboard_api import dashboard_api
from api.visualize_api import visualize_api

app = Flask(__name__, static_folder='static')
CORS(app)

# Create dataset folder if not exists
os.makedirs("dataset", exist_ok=True)

# Register Blueprints
app.register_blueprint(crawler_api, url_prefix='/api/crawler')
app.register_blueprint(preprocess_api, url_prefix='/api/preprocess')
app.register_blueprint(ngram_api, url_prefix='/api/ngram')
app.register_blueprint(predict_api, url_prefix='/api/predict')
app.register_blueprint(evaluate_api, url_prefix='/api/evaluate')
app.register_blueprint(dashboard_api, url_prefix='/api/dashboard')
app.register_blueprint(visualize_api, url_prefix='/api/visualize')

@app.route('/dataset/<path:filename>')
def serve_dataset(filename):
    if os.path.exists(os.path.join('dataset', filename)):
        return send_from_directory('dataset', filename)
    return "Not found", 404

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return serve_index()

if __name__ == '__main__':
    # Fix import issues for un-reorganized old code imports
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
