from flask import Blueprint, jsonify, request
from core.evaluator import run_evaluation

evaluate_api = Blueprint('evaluate_api', __name__)

@evaluate_api.route('/run', methods=['POST'])
def run_eval():
    data = request.json or {}
    n_values = data.get('n_values', [1, 2, 3])
    res = run_evaluation("All", n_values)
    if "error" in res:
        return jsonify(res), 400
    return jsonify(res)
