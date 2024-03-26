from flask import Flask, render_template, send_from_directory, request, Response, redirect, url_for, flash
import os
from io import BytesIO
from base64 import b64encode, b64decode
from moviepy.editor import *
import cv2
import numpy as np
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
import tempfile
import models
import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_url_path='', static_folder=os.path.join(FRONTEND_DIR, 'static'), template_folder=FRONTEND_DIR)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
models.db.init_app(app)

def utf8_to_image(utf8_string):
    if utf8_string.startswith("data:image/jpeg;base64,"):
        utf8_string = utf8_string[len("data:image/jpeg;base64,"):]
    image_data = b64decode(utf8_string)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def generate_video(data, audio_file, transition_name, duration):
    img_dur = int(duration)
    utf8_images = []
    for row in data:
        remo = row.read()
        utf8image = b64encode(remo).decode("utf-8")
        utf8_images.append(utf8image)

    images = [utf8_to_image(utf8_str) for utf8_str in utf8_images if utf8_str]

    max_width = max(img.shape[1] for img in images)
    max_height = max(img.shape[0] for img in images)

    resized_images = [cv2.resize(img, (max_width, max_height)) for img in images]
    resized_images_rgb = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in resized_images]

    clips = []
    for img in resized_images_rgb:
        clip = ImageClip(img).set_duration(img_dur)
        clips.append(clip)
    print(data)
    # Apply fadein transition between consecutive clips´
    transitioned_clips = []
    if transition_name == 'fadein': 
        for i in range(len(clips)):
            if i != 0:
                transitioned_clip = fadein(clips[i], duration=1)  # Apply fadein effect
            else:
                transitioned_clip = clips[i]
            transitioned_clips.append(transitioned_clip)

    elif transition_name == 'crossfade':
        for i in range(len(clips)):
            transitioned_clip = clips[i].crossfadein(1)
            transitioned_clips.append(transitioned_clip)
    elif transition_name == 'fadeout':
        for i in range(len(clips)):
            if i != 0:
                transitioned_clip = fadeout(clips[i], duration=1)  # Apply fadein effect
            else:
                transitioned_clip = clips[i]
            transitioned_clips.append(transitioned_clip)
    else:
        return Response("success", 200)
    # Concatenate the clips into a single video clip
    final_clip = concatenate_videoclips(transitioned_clips, method="compose")

    # Set fps attribute for the final clip
    final_clip.fps = 24  # Adjust fps as needed
    temp_audio_file_path = ""
    # Set audio clip
    audio_data = audio_file.read()
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        temp_audio_file.write(audio_data)
        temp_audio_file_path = temp_audio_file.name

    # Load the audio file
    audioclip = AudioFileClip(temp_audio_file_path)
    # audioclip = afx.audio_loop(audioclip, duration=img_dur)
    final_clip.audio = audioclip
    output_path = os.path.join("..", "frontend", "static", "uploads", "output_video.mp4")
    final_clip.write_videofile(output_path, codec='libx264')

    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Handle form submission
        models.db.create_all()
        user = models.User()
        user.email = request.form['email']
        user.password = request.form['password']
        models.db.session.add(user)
        models.db.session.commit()
        return render_template('login.html')
    else:
        # Handle GET request (e.g., render the login form)
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # create a signup
    if request.method == 'POST':
        user = models.User()
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        if not all([user.name, user.email, user.password]):
            return render_template('signup.html', error='Please fill in all fields')
        else:
            # check if user already exists
            existing_user = models.User.query.filter_by(email=user.email).first()
            if existing_user:
                return render_template('signup.html', error='An account with that email already exists')
            models.db.session.add(user)
            models.db.session.commit()
            flash("Account created successfully! You are now logged in.")
            return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/api/create-video', methods=['POST', 'GET'])
def create_video():
    if request.method == "POST":
        images = request.files.getlist('ImageFile')
        music = request.files.get('musicFile')
        effect = request.form.get('effect')
        duration = request.form.get('duration')
        resolution = request.form.get('resolution')
        generate_video(images, music, effect, duration)
    return Response("Successful", 200)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(os.path.join(FRONTEND_DIR, 'static'), path)

if __name__ == '__main__':
    app.run(debug=True)
