from flask import Flask, render_template
from flask_socketio import SocketIO
import sys
from supabase import create_client, Client
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
import os
import string
import random
from flask import Flask
import eventlet
eventlet.monkey_patch()

url = "https://nwhobhigrgxtpnwydpxj.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
supabase: Client = create_client(url, key)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dshjhkjuyrgy5etfuytrhgf5yewrsgfqwr!'
socketio = SocketIO(app, max_http_buffer_size=1024 **
                    3, cors_allowed_origins='*', debug=True)


@socketio.on('upload')
def upload(file_data):
    supaURL = "https://nwhobhigrgxtpnwydpxj.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
    bucket = "data"
    random_base64 = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=10))
    file_path = f"./public/{random_base64}{random_base64}.mp4"

    file_size = sys.getsizeof(file_data)

    url = f"{supaURL}/storage/v1/object/{bucket}/{file_path}"

    multipart_encoder = MultipartEncoder(
        fields={
            'file': (os.path.basename(file_path), file_data, 'video/mp4')
        }
    )

    def uploadProgress(monitor):
        file_size = monitor.len
        uploaded_bytes = monitor.bytes_read
        progress = uploaded_bytes / file_size

        print(f"Upload progress: {progress * 100}%")
        socketio.send('upload_response', {
            "progress": progress * 100
        })

    monitor = MultipartEncoderMonitor(multipart_encoder, uploadProgress)

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': monitor.content_type
    }

    response = requests.post(url, data=monitor, headers=headers)

    if response.status_code == 200:
        print("Upload successful.")
        socketio.send('upload_response', {
            "status": "success",
            "progress": 100
        })
    else:
        print(f"Upload failed with status code: {response.status_code}")
        print(response.text)
        socketio.send('upload_response', {
            "status": "failure",
            "code": response.status_code,
            "error": response.text,
            "progress": 0
        })


if __name__ == '__main__':
    socketio.run(app, port=8000)
    print("Server closed gracefully.")
