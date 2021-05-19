from flask import Flask, render_template
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'*': {'origins': 'https://d3js.org'}})

    @app.route('/')
    def index():
        return render_template('test.html')
        
    @app.route('/graph')
    def graph():
        return render_template('index.html')

    @app.route('/node')
    def node():
        return render_template('index2.html')
    
    return app