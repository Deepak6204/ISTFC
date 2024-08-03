from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, render_template_string, send_file
import os
import face_recognition
import base64
from io import BytesIO
from PIL import Image
import uuid
import qrcode
from zipfile import ZipFile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def create_user_folder():
    while True:
        user_id = str(uuid.uuid4())
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
            return user_id, user_folder

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    user_id, user_folder = create_user_folder()

    if 'files' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('files')
    if not files:
        return redirect(request.url)
    
    for file in files:
        if file.filename == '':
            continue
        file_path = os.path.join(user_folder, file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
        file.save(file_path)
    
    query_url = url_for('query', user_id=user_id, _external=True)
    
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(query_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    
    # Save QR code to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('ascii')
    # Render the HTML with the QR code and the actual link
    
    return render_template('upload_success.html', query_url=query_url, qr_code=img_base64)

@app.route('/query/<user_id>')
def query(user_id):
    return render_template('query.html', user_id=user_id)

@app.route('/compare_faces/<user_id>', methods=['POST'])
def compare_faces(user_id):
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data"}), 400
    
    image_data = data['image'].split(",")[1]
    query_image = face_recognition.load_image_file(BytesIO(base64.b64decode(image_data)))
    query_encodings = face_recognition.face_encodings(query_image)

    if not query_encodings:
        return jsonify({"error": "No faces found in the query image"}), 400

    query_encoding = query_encodings[0]
    matched_images = []

    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    for root, _, files in os.walk(user_folder):
        for file in files:
            file_path = os.path.join(root, file)
            target_image = face_recognition.load_image_file(file_path)
            target_encodings = face_recognition.face_encodings(target_image)

            for target_encoding in target_encodings:
                match = face_recognition.compare_faces([target_encoding], query_encoding, tolerance=0.6)
                if match[0]:
                    matched_images.append(os.path.join(user_id,'images', file))
                    break

    return render_template('results.html', matched_images=matched_images, user_id = user_id)


@app.route('/download_all_images/<path:user_id>')
def download_all_images(user_id):
    # user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    matched_images = [os.path.join(root, file) for root, _, files in os.walk(user_folder) for file in files]
    
    if not matched_images:
        return jsonify({"error": "No images found to download."}), 404

    # Create a temporary zip file
    zip_filename = 'matched_images.zip'
    zip_filepath = os.path.join('/tmp', zip_filename)

    with ZipFile(zip_filepath, 'w') as zipf:
        for image_path in matched_images:
            zipf.write(image_path, os.path.basename(image_path))

    return send_file(zip_filepath, as_attachment=True, download_name=zip_filename)


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000, debug=True)
