from core.server import sio


@sio.on('connect', namespace='/redis')
def main_chanel(sid, environ):
    print("connected: ", sid)


@sio.on('message', namespace='/redis')
def message(sid, data):
    print("New message: ", data)
    sio.emit("message reply", room=sid)


@sio.on('disconnect', namespace='/redis')
def disconnect(sid):
    print("disconnect", sid)
