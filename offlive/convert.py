from flask import (
    Blueprint, jsonify, request, current_app
)
from rest_client import get_json_object
from prompt import convert_to_api
from id_refactor import apply_rule, apply_id_offset

bp = Blueprint('convert', __name__, url_prefix='/api')


@bp.route('/convert', methods=['POST'])
def convert():
    rule = get_json_object(current_app.config["CONFIG_BUCKET"], current_app.config["RULE_FILE"])
    content = request.get_json()
    api = convert_to_api(content, current_app.config['COMFY_URL'])
    api = apply_id_offset(api)
    api = apply_rule(api, rule)

    return jsonify(api)


@bp.route('/convert', methods=['PUT'])
def update():
    rule = get_json_object(current_app.config["CONFIG_BUCKET"], current_app.config["RULE_FILE"])
    old_api = request.get_json()
    new_api = apply_id_offset(old_api)
    new_api = apply_rule(new_api, rule)
    return jsonify(new_api)
