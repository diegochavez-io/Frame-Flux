from flask import Flask, render_template, request, send_file, url_for
import cv2
import os
import uuid
import tempfile

app = Flask(__name__)

# Ensure the static/frames directory exists
FRAMES_DIR = os.path.join(app.static_folder, 'frames')
os.makedirs(FRAMES_DIR, exist_ok=True)

def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []
    
    # Read the first frame
    ret, first_frame = cap.read()
    
    # Move to the last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
    ret, last_frame = cap.read()
    
    cap.release()
    
    # Generate unique filenames
    unique_id = str(uuid.uuid4())
    first_frame_path = os.path.join(FRAMES_DIR, f'first_frame_{unique_id}.jpg')
    last_frame_path = os.path.join(FRAMES_DIR, f'last_frame_{unique_id}.jpg')
    
    cv2.imwrite(first_frame_path, first_frame)
    cv2.imwrite(last_frame_path, last_frame)
    
    return [os.path.basename(first_frame_path), os.path.basename(last_frame_path)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_type = request.form['input_type']
        frames = []
        error = None
        
        try:
            if input_type == 'file':
                video = request.files['input']
                if video:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
                        video.save(temp_video.name)
                        frames = extract_frames(temp_video.name)
                    os.unlink(temp_video.name)
                else:
                    error = "No video file uploaded."
            else:
                uploaded_files = request.files.getlist('input')
                for file in uploaded_files:
                    if file.filename.endswith(('.mp4', '.avi', '.mov')):
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
                            file.save(temp_video.name)
                            frames.extend(extract_frames(temp_video.name))
                        os.unlink(temp_video.name)
            
            if not frames and not error:
                error = "No frames were extracted. Please check your input."
        except Exception as e:
            error = f"An error occurred: {str(e)}"
        
        return render_template('results.html', frames=frames, error=error)
    return render_template('index.html')

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(os.path.join(FRAMES_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)