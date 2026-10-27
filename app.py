import os
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PDF_FOLDER'] = 'outputs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversions.db'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class ConversionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    image_count = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert_images():
    if 'images' not in request.files:
        return jsonify({'error': 'No images uploaded'}), 400
    
    files = request.files.getlist('images')
    
    if len(files) > 30:
        return jsonify({'error': 'Maximum 30 images allowed'}), 400

    # Get ordered filenames sent from the frontend drag-and-drop rearrangement
    order = request.form.getlist('order') # list of original filenames in desired order
    
    saved_files = {}
    for file in files:
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
            file.save(filepath)
            saved_files[file.filename] = filepath

    # Order images based on user rearrangement
    ordered_paths = []
    for name in order:
        if name in saved_files:
            ordered_paths.append(saved_files[name])
    
    # Fallback if order wasn't passed correctly
    if not ordered_paths:
        ordered_paths = list(saved_files.values())

    if not ordered_paths:
        return jsonify({'error': 'No valid images processed'}), 400

    try:
        images = [Image.open(p).convert('RGB') for p in ordered_paths]
        pdf_filename = f"{uuid.uuid4()}.pdf"
        pdf_path = os.path.join(app.config['PDF_FOLDER'], pdf_filename)
        
        # Save first image and append the rest
        images[0].save(pdf_path, save_all=True, append_images=images[1:])

        # Log conversion in database
        log = ConversionLog(filename=pdf_filename, image_count=len(images))
        db.session.add(log)
        db.session.commit()

        return jsonify({'success': True, 'pdf_url': f'/download/{pdf_filename}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_pdf(filename):
    return send_from_directory(app.config['PDF_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)