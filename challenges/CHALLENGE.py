import re
import pandas as pd

from flask import Flask, jsonify

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = {
    "info": {
        "title":  "API Documentation for Data Processing and Modeling",
        "version": "1.0.0",
        "description": "Dokumentasi API"
    },
    "host": "127.0.0.1:5000"
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'challenges',
            "route": '/challenges',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/challenges/"
}
swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)

@swag_from("docs/textProcessing.yaml", methods=['POST'])
@app.route('/text_processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }
    return jsonify(json_response)

@swag_from("docs/fileTextProcessing.yaml", methods=['POST'])
@app.route('/file_text_processing', methods=['POST'])
def text_processing1():
    try:
        file = request.files.getlist('file')[0]
        df = pd.read_csv(file)
        texts = df.text.tolist()
        cleaned_text = [re.sub(r'[^a-zA-Z0-9]', ' ', text) for text in texts]
        json_response = {
            'status_code': 200,
            'description': "Teks yang sudah diproses",
            'data': cleaned_text,
        }
    except Exception as e:
        json_response = {
            'status_code': 500,
            'description': "Terjadi kesalahan dalam pemrosesan file",
            'error': str(e)
        }
    return jsonify(json_response)

if __name__ == '__main__':
    app.run()