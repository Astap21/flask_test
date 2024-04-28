import os
from flask import Flask, render_template, request, abort, send_file, redirect, url_for

app = Flask(__name__)
#app.secret_key = 'your_secret_key'

# Получаем абсолютный путь к текущему рабочему каталогу, где находится запущенный скрипт
script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)
BASE_DIR = script_directory  # Specify the base directory
logs_dir = os.path.join(script_directory, "Logs")  # Specify the base directory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def show_files():
    return render_template('files.html', files=get_files(logs_dir))

@app.route('/change_speed_0', methods=['POST'])
def change_speed_0():
    selected_speed = request.form['bus_speed']
    return f"The selected speed for can 0 is: {selected_speed}  kbit/s"

@app.route('/change_speed1', methods=['POST'])
def change_speed_1():
    selected_speed = request.form['bus_speed']
    return f"The selected speed for can 1 is: {selected_speed}  kbit/s"

@app.route('/command_line', methods=['POST'])
def command_line():
    text_command = request.form['my_command']
    return f"My command is: {text_command}"

@app.route('/reboot', methods=['POST'])
def reboot():
    return f"System rebooting"

@app.route('/<path:filename>')
def download_file(filename):
    file_path = os.path.join(logs_dir, filename)
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return show_subfolder_files(file_path)

@app.route('/<path:subpath>')
def show_subfolder_files(subpath):
    folder_path = os.path.join(logs_dir, subpath)
    if os.path.isdir(folder_path):
        return render_template('files.html', files=get_files(folder_path))
    else:
        abort(404)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    # Save the uploaded file to a specific directory, e.g., 'uploads'
    file.save('uploads/' + file.filename)
    return 'File successfully uploaded'

def get_files(folder_path):
    files = []
    for name in os.listdir(folder_path):
        path = os.path.join(folder_path, name)
        if os.path.isfile(path):
            files.append(os.path.relpath(path, logs_dir))
        elif os.path.isdir(path):
            files.append(os.path.relpath(path, logs_dir) + os.path.sep)
    return files

if __name__ == '__main__':
    app.run(debug=True)