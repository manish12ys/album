from flask import Flask, request, jsonify, send_from_directory,render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    folder = request.form.get('folder', 'default')
    folder_path = os.path.join(UPLOAD_FOLDER, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file.save(os.path.join(folder_path, file.filename))
    return jsonify({'message': 'File uploaded successfully'})
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.json.get('folder_name')
    if not folder_name:
        return jsonify({'error': 'Folder name is required'}), 400
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return jsonify({'message': 'Folder created'})

@app.route('/rename_folder', methods=['POST'])
def rename_folder():
    old_name = request.json.get('old_name')
    new_name = request.json.get('new_name')
    if not old_name or not new_name:
        return jsonify({'error': 'Both old and new names are required'}), 400
    old_path = os.path.join(UPLOAD_FOLDER, old_name)
    new_path = os.path.join(UPLOAD_FOLDER, new_name)
    
    if not os.path.exists(old_path):
        return jsonify({'error': 'Folder does not exist'}), 404
    os.rename(old_path, new_path)
    return jsonify({'message': 'Folder renamed'})

@app.route('/share_folder', methods=['POST'])
def share_folder():
    folder_name = request.json.get('folder_name')
    if not folder_name:
        return jsonify({'error': 'Folder name is required'}), 400
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
    if not os.path.exists(folder_path):
        return jsonify({'error': 'Folder does not exist'}), 404
    return jsonify({'message': 'Folder shared', 'url': f'/uploads/{folder_name}'})

@app.route('/uploads/<folder>/<filename>')
def get_image(folder, filename):
    return send_from_directory(os.path.join(UPLOAD_FOLDER, folder), filename)

if __name__ == '__main__':
    app.run(debug=True)
