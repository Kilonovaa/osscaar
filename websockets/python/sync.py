from flask import Flask, request
from aiohttp import web
import eventlet

import socketio
import random
import string
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
import requests
from supabase import create_client, Client
import sys

url = "https://nwhobhigrgxtpnwydpxj.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
supabase: Client = create_client(url, key)


sio = socketio.Server(cors_allowed_origins='*',
                      max_http_buffer_size=1024 ** 3, logger=False)

app = socketio.WSGIApp(sio)


@sio.on('connect')
def connect():
    print('Client connected')


@sio.on('disconnect')
def disconnect():
    print('Client disconnected')


@sio.on('upload')
def upload(sid, file_data):
    supaURL = "https://nwhobhigrgxtpnwydpxj.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
    bucket = "data"
    file_path = "./testing/test.mp4"

    file_size = sys.getsizeof(file_data)

    url = f"{supaURL}/storage/v1/object/{bucket}/{file_path}"

    multipart_encoder = MultipartEncoder(
        fields={
            'file': (os.path.basename(file_path), file_data, 'video/mp4')
        }
    )

    def uploadProgress(monitor):
        progress = monitor.bytes_read / file_size

        def sendProgress(progress):
            print(f"Upload progress: {progress * 100}%")
            sio.emit('upload_response', {
                "progress": progress * 100
            })

        sendProgress(progress)

    monitor = MultipartEncoderMonitor(multipart_encoder, uploadProgress)

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': monitor.content_type
    }

    response = requests.post(url, data=monitor, headers=headers)

    if response.status_code == 200:
        print("Upload successful.")
        sio.emit('upload_response', {
            "status": "success",
        })
    else:
        print(f"Upload failed with status code: {response.status_code}")
        print(response.text)
        sio.emit('upload_response', {
            "status": "failure",
            "code": response.status_code,
        })


if __name__ == '__main__':
    print("Starting server...")
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
