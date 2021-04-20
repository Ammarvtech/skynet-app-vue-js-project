# import system libraries
from gevent import monkey;monkey.patch_all();monkey.patch_thread()
from config import cfg
from beaker.middleware import SessionMiddleware
import socketio

# configure logging
import logging
logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='[%(asctime)s.%(msecs)d] [%(name)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

# HTTP Sessions

if __name__ == '__main__':
    from gevent import pywsgi
    import argparse
    parser = argparse.ArgumentParser(description="Test parser")
    parser.add_argument('--port', type=int, required=True, help="Please enter port", default=8888)
    parser.add_argument('--rest', type=bool, required=False, help="Enable only rest routes", default=False)
    parser.add_argument('--socket',type=bool, required=False, help="Enable only socket io", default=False)
    parser.add_argument('--prod', type=bool,required=False, help="Enable rest & sockets for development", default=False)
    args = parser.parse_args()

    try:
        if not args.prod:
            from geventwebsocket.handler import WebSocketHandler
            from namespace import socketApp
            from rest import restApp
            app = SessionMiddleware(restApp, cfg.SESSION_OPT)
            app = application = socketio.Middleware(socketApp, app)
            pywsgi.WSGIServer((cfg.SERV_IP, args.port), app, handler_class=WebSocketHandler).serve_forever()
        elif args.rest:
            from rest import restApp
            app = application = SessionMiddleware(restApp, cfg.SESSION_OPT)
            pywsgi.WSGIServer((cfg.SERV_IP, args.port), app).serve_forever()
        elif args.socket:
            from geventwebsocket.handler import WebSocketHandler
            from bottle import Bottle
            from namespace import socketApp
            app = application = socketio.Middleware(socketApp, Bottle)
            pywsgi.WSGIServer((cfg.SERV_IP, args.port), app, handler_class=WebSocketHandler).serve_forever()
    except Exception as e:
        raise e

