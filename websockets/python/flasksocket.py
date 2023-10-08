import socketio
from flask import Flask
import eventlet
import socketio
import random
import string
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
import requests
from supabase import create_client, Client
import sys
import algorithm

url = "https://nwhobhigrgxtpnwydpxj.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
supabase: Client = create_client(url, key)


sio = socketio.Server(logger=True, async_mode="threading", cors_allowed_origins='*',
                      max_http_buffer_size=1024 ** 3)
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(
    sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'
thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('server', {'data': 'Server generated event'})


@sio.event
def my_room_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=message['room'])


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')


@sio.on('upload')
def upload(sid, file_data):
    supaURL = "https://nwhobhigrgxtpnwydpxj.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
    bucket = "data"
    random_base64 = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=10))
    file_path = f"./public/{sid}{random_base64}.mp4"

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
        sio.emit('upload_response', {
            "progress": progress * 100
        }, room=sid)

    monitor = MultipartEncoderMonitor(multipart_encoder, uploadProgress)

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': monitor.content_type
    }

    response = requests.post(url, data=monitor, headers=headers)
    # processing the sound

    def audioProcessCAllback(progress):
        sio.emit('sound_progress', {
            "progress": progress
        }, room=sid)
    audio_data = algorithm.processAudio(sid, file_data, audioProcessCAllback)
    # uploading the sound

    sound_path = f"./public/{sid}{random_base64}.wav"

    file_size = sys.getsizeof(audio_data)

    url = f"{supaURL}/storage/v1/object/{bucket}/{sound_path}"

    multipart_encoder = MultipartEncoder(
        fields={
            'file': (os.path.basename(sound_path), audio_data, 'audio/wav')
        }
    )

    def uploadSoundProgress(monitor):
        file_size = monitor.len
        uploaded_bytes = monitor.bytes_read
        progress = uploaded_bytes / file_size

        print(f"Upload progress: {progress * 100}%")
        sio.emit('send_response', {
            "progress": progress * 100
        }, room=sid)

    monitor = MultipartEncoderMonitor(multipart_encoder, uploadSoundProgress)

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': monitor.content_type
    }

    response = requests.post(url, data=monitor, headers=headers)

    # finish sound uploading
    sio.emit('sound', {
        "status": "success",
        "progress": 100,
        "url": supabase.storage.from_('data').get_public_url(sound_path)
    }, room=sid)

    # for i in range(0, 11):
    #     sio.emit('sound_progress', {
    #         "progress": i * 10
    #     }, room=sid)
    #     sio.sleep(0.1 + 0.5 * random.random())
    #     if i == 8:
    #         sio.sleep(1 * random.random())

    # for i in range(0, 11):
    #     sio.emit('send_response', {
    #         "progress": i * 10
    #     }, room=sid)
    #     sio.sleep(0.08 + 0.2 * random.random())
    #     if i == 8:
    #         sio.sleep(3 * random.random())

    if response.status_code == 200:
        print("Upload successful.")
        sio.emit('upload_response', {
            "status": "success",
            "progress": 100,
            "url": supabase.storage.from_('data').get_public_url(file_path)
        }, room=sid)
    else:
        print(f"Upload failed with status code: {response.status_code}")
        print(response.text)
        sio.emit('upload_response', {
            "status": "failure",
            "code": response.status_code,
            "error": response.text,
            "progress": 0
        }, room=sid)


if __name__ == '__main__':

    if sio.async_mode == 'threading':
        app.run(threaded=True, port=8000, debug=True, host="0.0.0.0")
    elif sio.async_mode == 'eventlet':
        import eventlet
        import eventlet.wsgi
        eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
    print("Server terminated gracefully.")
