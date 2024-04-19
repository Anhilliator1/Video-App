from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
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

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    title = request.form['title']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        video = Video(title=title, filename=filename)
        db.session.add(video)
        db.session.commit()
        return jsonify({"success": True, "message": "Video uploaded successfully."})
    return jsonify({"success": False, "message": "Failed to upload video."})

@app.route('/videos/<int:video_id>')
def video(video_id):
    video = Video.query.get(video_id)
    if video:
        return send_from_directory(app.config['UPLOAD_FOLDER'], video.filename)
    return 'Video not found', 404

@app.route('/play/<int:video_id>')
def play(video_id):
    video = Video.query.get(video_id)
    if video:
        return render_template('play.html', video=video)
    return 'Video not found', 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
