import socketio

from namespace.dealerSpace import DealerSpace

socketApp = socketio.Server(ping_interval=5000, ping_timeout=120000, engineio_logger=True)

socketApp.register_namespace(DealerSpace(namespace='/dlr'))

__all__ = [
    "socketApp"
]