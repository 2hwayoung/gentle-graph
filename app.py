from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json


def create_app():
    app = Flask(__name__, static_folder='./data/')
    CORS(app)

    @app.route('/')
    def index():
        return render_template('index.html')
        
    @app.route('/test')
    def test():

        data = json.loads("./data/graphFile.json")
    
        return jsonify(data)

    @app.route('/node')
    def node():
        return render_template('index2.html')
    
    return app
