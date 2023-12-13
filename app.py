from flask import Flask, jsonify, request
from prompt import convert_to_api
from id_refactor import apply_id_offset, apply_rule
import json 
import sys

app = Flask(__name__)

data = {"name": "simple comfyui workflow converter"}
url = 'http://127.0.0.1:8188/'
port = 3003

@app.route('/')
def index():
    return jsonify(data)

@app.route('/api/convert', methods=['POST'])
def convert():
    rule_fp = open("rule.json")
    rule = json.load(rule_fp)
    rule_fp.close()

    content = request.get_json()

    api = convert_to_api(content, url)
    api = apply_id_offset(api)
    api = apply_rule(api, rule)
    
    return jsonify(api)

if __name__ == '__main__':

    if len(sys.argv)==3:
        url = sys.argv[1]
        port = int(sys.argv[2])
    
    app.run(host='0.0.0.0', port=port, debug=True)
