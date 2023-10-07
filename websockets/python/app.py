from aiohttp import web
import socketio
import random
import string
import os

from supabase import create_client, Client

url = "https://nwhobhigrgxtpnwydpxj.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53aG9iaGlncmd4dHBud3lkcHhqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NjY4Njg1MiwiZXhwIjoyMDEyMjYyODUyfQ.7UxyPZo5PLIEuuntEAXi01t0ZrEc7ZcReQRA08af1qU"
supabase: Client = create_client(url, key)


sio = socketio.AsyncServer(
    async_mode='aiohttp', cors_allowed_origins='*', max_http_buffer_size=1024 ** 3)
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
async def my_event(sid, message):
    await sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
async def my_broadcast_event(sid, message):
    await sio.emit('my_response', {'data': message['data']})


@sio.event
async def join(sid, message):
    await sio.enter_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
                   room=sid)


@sio.event
async def leave(sid, message):
    await sio.leave_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Left room: ' + message['room']},
                   room=sid)


@sio.event
async def close_room(sid, message):
    await sio.emit('my_response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'])
    await sio.close_room(message['room'])


@sio.event
async def my_room_event(sid, message):
    await sio.emit('my_response', {'data': message['data']},
                   room=message['room'])


@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)


@sio.event
async def connect(sid, environ):
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')


def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)


@sio.on('upload')
async def upload(sid, file_data):
    try:
        random_base64 = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=10))
        folder = f"./tmp/{sid}/"
        filepath = f'{folder}{random_base64}.mp4'
        createPath(folder)
        with open(filepath, 'wb') as file:
            file.write(file_data)
        print(f"File uploaded successfully: {filepath}")
        response = {'message': 'success'}

        with open(filepath, 'rb') as f:
            supabase.storage.from_("data").upload(
                file=f, path=f"./public/{sid}{random_base64}.mp4", file_options={"content-type": "video/mp4"})
    except Exception as e:
        print(f"Failed to upload file: {str(e)}")
        response = {'message': 'failure', 'error': str(e)}
    await sio.emit('upload_response', response, room=sid)

# app.router.add_static('/static', 'static')


async def init_app():

    sio.start_background_task(background_task)
    return app


if __name__ == '__main__':
    print("Starting server...")
    web.run_app(init_app(), port=8000)
