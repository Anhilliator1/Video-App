from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'
db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['video']
        title = request.form['title']

        if file and title:
            video_id = str(uuid.uuid4())

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            video = Video(title=title, filename=filename)

            db.session.add(video)
            db.session.commit()

    return render_template('upload.html')

@app.route('/play/<video_id>')
def play(video_id):
    video = Video.query.filter_by(id=video_id).first()
    if video:
        return render_template('play.html', video=video)
    return 'Video not found', 404

@app.route('/videos/<int:video_id>')
def video(video_id):
    video = Video.query.get(video_id)
    if video:
        return send_from_directory(app.config['UPLOAD_FOLDER'], video.filename)
    return 'Video not found', 404

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    
    if not query:
        videos = Video.query.all()
    else:
        videos = Video.query.filter(Video.title.ilike(f'%{query}%')).all()

    return render_template('search_results.html', videos=videos, query=query)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
