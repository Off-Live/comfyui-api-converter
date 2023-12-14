from flask import Flask, jsonify, request
from prompt import convert_to_api
from id_refactor import apply_id_offset, apply_rule
import json 
import sys
import boto3

app = Flask(__name__)

data = {"name": "simple comfyui workflow converter"}
url = 'http://127.0.0.1:8188/'
port = 3003

@app.route('/api/test')
def download_and_update_rule():
  print("Downloading rule from S3...")
  s3 = boto3.client('s3')
  s3.download_file('pumky-config','rule.json','./rule.json')


@app.route('/')
def index():
    return jsonify(data)

@app.route('/api/convert', methods=['POST'])
def convert():
    rule = {}
    with open('./rule.json','r') as f:
      rule = json.load(f)

    content = request.get_json()
    api = convert_to_api(content, url)
    api = apply_id_offset(api)
    api = apply_rule(api, rule)
    
    return jsonify(api)

@app.route('/api/update', methods=['POST'])
def update():
    rule = {}
    with open('./rule.json','r') as f:
      rule = json.load(f)

    old_api = request.get_json()
    new_api = apply_id_offset(old_api)
    new_api = apply_rule(new_api, rule)
    return jsonify(new_api)

@app.route('/api/update_rule', methods=['POST'])
def update_rule():
    download_and_update_rule()
    return jsonify({"status":"ok"})

if __name__ == '__main__':

    if len(sys.argv)==3:
        url = sys.argv[1]
        port = int(sys.argv[2])
    
    download_and_update_rule()
    app.run(host='0.0.0.0', port=port, debug=True)
