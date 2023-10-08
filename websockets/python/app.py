from aiohttp import web
import socketio
import random
import string
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
import requests
from supabase import create_client, Client
import sys
import asyncio

url = "https://nwhobhigrgxtpnwydpxj.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
supabase: Client = create_client(url, key)


sio = socketio.AsyncServer(
    async_mode='aiohttp', cors_allowed_origins='*', max_http_buffer_size=1024 ** 3, logger=False)
app = web.Application()


sio.attach(app)


async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        await sio.emit('my_response', {'data': 'Server generated count ' + str(count)})


@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)


@sio.event
async def connect(sid, environ):
    print('Client connected')


@sio.event
def disconnect(sid):
    print('Client disconnected')


@sio.on('upload')
async def upload(sid, file_data):

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

    async def uploadProgress(monitor):
        progress = monitor.bytes_read / file_size

        async def sendProgress(progress):
            print(f"Upload progress: {progress * 100}%")
            await sio.emit('upload_response', {
                "id": sid,
                "progress": progress * 100
            }, room=sid)

        await sendProgress(progress)

    monitor = MultipartEncoderMonitor(multipart_encoder, uploadProgress)

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': monitor.content_type
    }

    response = requests.post(url, data=monitor, headers=headers)

    if response.status_code == 200:
        print("Upload successful.")
        await sio.emit('upload_response', {
            "status": "success",
            "url": supabase.storage.from_('bucket_name').get_public_url(file_path)

        }, room=sid)
    else:
        print(f"Upload failed with status code: {response.status_code}")
        print(response.text)
        await sio.emit('upload_response', {
            "status": "failure",
            "code": response.status_code,
        }, room=sid)

# app.router.add_static('/static', 'static')


async def init_app():

    sio.start_background_task(background_task)
    return app


if __name__ == '__main__':
    print("Starting server...")
    web.run_app(init_app(), port=8000)
