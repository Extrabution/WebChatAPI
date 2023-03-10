from __future__ import annotations
from fastapi import FastAPI
import uvicorn
from multiprocessing import cpu_count, freeze_support
from fastapi.staticfiles import StaticFiles
from api.routes import register
from api.websocket_events import register_ws
import socketio


app = FastAPI()
app.mount('/static', StaticFiles(directory='../static'), name='static')
sio = socketio.AsyncServer(async_mode='asgi', logger=False)
app_sio = socketio.ASGIApp(sio, app)
app.mount('/ws', app_sio)
register(app)
register_ws(sio)


def main():
    freeze_support()
    num_workers = int(cpu_count() * 0.75)
    start_server(num_workers=1, reload=False, host='0.0.0.0')


def start_server(host='127.0.0.1', port=8000, num_workers=4, loop='asyncio', reload=False):
    uvicorn.run('main:app', host=host,
      port=port,
      workers=num_workers,
      loop=loop,
      reload=reload)


if __name__ == '__main__':
    main()
