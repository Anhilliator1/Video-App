from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

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

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/play/<int:video_id>')
def play(video_id):
    video = Video.query.get(video_id)
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
        # If the query is empty, retrieve all videos
        videos = Video.query.all()
    else:
        # If the query is not empty, perform search
        videos = Video.query.filter(Video.title.ilike(f'%{query}%')).all()

    return render_template('search_results.html', videos=videos, query=query)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
