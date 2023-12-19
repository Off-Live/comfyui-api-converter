from flask import (
    Blueprint, jsonify, request, current_app
)
from rest_client import get_json_object, put_json_object

bp = Blueprint('rule', __name__, url_prefix='/api')


@bp.route('/rule', methods=['GET'])
def get_rule():
    rule = get_json_object(current_app.config["CONFIG_BUCKET"], current_app.config["RULE_FILE"])
    return jsonify(rule)


@bp.route('/rule', methods=['PUT'])
def update_rule():
    json = request.get_json()
    put_json_object(json, current_app.config["CONFIG_BUCKET"], current_app.config["RULE_FILE"])
    return jsonify({"status": "ok"})
