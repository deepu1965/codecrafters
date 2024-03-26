from flask import request, jsonify
from flask import render_template

def configure_routes(app):

    @app.route('/login', methods=['POST'])
    def login():
        # login
        return jsonify(message="Login Successful"), 200

    @app.route('/signup', methods=['POST'])
    def signup():
        #  signup
        return jsonify(message="Signup Successful"), 201

    @app.route('/upload', methods=['POST'])
    def upload():
        #  file upload
        return jsonify(message="Upload Successful"), 200

    @app.route('/create-video', methods=['POST'])
    def create_video():
        # video creation
        return jsonify(message="Video Creation Successful"), 200
