from aiohttp import web
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


def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_callback(sio, sid, encoder):
    encoder_len = len(encoder)

    def callback(monitor):
        progress = monitor.bytes_read / encoder_len
        print(f"Upload progress: {progress * 100}%")
        sio.emit('upload_response', {
            "id": sid,
            "progress": progress * 100
        }, room=sid)

    return callbac


@sio.on('upload')
async def upload(sid, file_data):
    # try:
    #     random_base64 = ''.join(random.choices(
    #         string.ascii_lowercase + string.digits, k=10))
    #     folder = f"./tmp/{sid}/"
    #     filepath = f'{folder}{random_base64}.mp4'
    #     createPath(folder)
    #     # with open(filepath, 'wb') as file:
    #     #     file.write(file_data)
    #     print(f"File uploaded successfully: {filepath}")
    #     response = {'message': 'success'}

    #     supabase.storage.from_("data").upload(
    #         file=file_data, path=f"./public/{sid}{random_base64}.mp4", file_options={"content-type": "video/mp4"})
    # except Exception as e:
    #     print(f"Failed to upload file: {str(e)}")
    #     response = {'message': 'failure', 'error': str(e)}
    # await sio.emit('upload_response', response, room=sid)

    # try:
    #     random_base64 = ''.join(random.choices(
    #         string.ascii_lowercase + string.digits, k=10))
    #     folder = f"./tmp/{sid}/"
    #     filepath = f'{folder}{random_base64}.mp4'
    #     createPath(folder)
    #     print(f"File uploaded successfully: {filepath}")

    #     # Create form data
    #     multipart_data = MultipartEncoder(
    #         fields={
    #             'cacheControl': '3600',
    #             '': (filepath, file_data, 'video/mp4')
    #         }
    #     )

    #     monitor = MultipartEncoderMonitor(
    #         multipart_data, create_callback(sio, sid, multipart_data))

    #     headers = {
    #         "Content-Type": monitor.content_type,
    #         **supabase.headers,
    #     }

    #     response = requests.post(
    #         f"{url}/storage/v1/object/data/{sid}{random_base64}.mp4",
    #         data=monitor,
    #         headers=headers
    #     )

    #     if response.status_code == 200:
    #         print("The transfer is complete.")
    #         response = {'message': 'success'}
    #     else:
    #         print(f"Failed to upload file: {response.content}")
    #         response = {'message': 'failure', 'error': str(response.content)}

    # except Exception as e:
    #     print(f"Failed to upload file: {str(e)}")
    #     response = {'message': 'failure', 'error': str(e)}

    # await sio.emit('upload_response', response, room=sid)
    supaURL = "https://nwhobhigrgxtpnwydpxj.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
    bucket = "data"
    file_path = "test.mp4"

    file_size = os.path.getsize(file_path)
    file_size = sys.getsizeof(file_data)

    url = f"{supaURL}/storage/v1/object/{bucket}/{file_path}"

    multipart_encoder = MultipartEncoder(
        fields={
            'file': (os.path.basename(file_path), file_data, 'video/mp4')
        }
    )

    monitor = MultipartEncoderMonitor(multipart_encoder, lambda monitor: print(
        f"Upload progress: {monitor.bytes_read} / {file_size} bytes uploaded"))

    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': monitor.content_type
    }

    response = requests.post(url, data=monitor, headers=headers)

    if response.status_code == 200:
        print("Upload successful.")
    else:
        print(f"Upload failed with status code: {response.status_code}")
        print(response.text)

# app.router.add_static('/static', 'static')


async def init_app():

    sio.start_background_task(background_task)
    return app


if __name__ == '__main__':
    print("Starting server...")
    web.run_app(init_app(), port=8000)
