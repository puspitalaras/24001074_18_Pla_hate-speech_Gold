import re
import pandas as pd
from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

# Swagger configuration
swagger_template = {
    "info": {
        "title":  "API Documentation for Data Processing and Modeling",
        "version": "1.0.0",
        "description": "Dokumentasi API"
    },
    "host": "127.0.0.1:5000"
}
swagger_config = {
    'headers': [],
    'specs': [{
        'endpoint': 'docs',
        'route': '/docs.json',
    }],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/docs/'
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Text Processing endpoint
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    cleaned_text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }
    return jsonify(json_response)

# Text Processing from File endpoint
@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():
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
    