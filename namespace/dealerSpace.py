from gevent import sleep, spawn
import socketio
import json
import boto3
import datetime
from config import cfg
from libs import dao

sqs = boto3.resource('sqs', region_name=cfg.SQS_REGION,
                          aws_access_key_id=cfg.SQS_ACCESS_KEY,
                          aws_secret_access_key=cfg.SQS_SECRET_KEY)
alertsQ = sqs.get_queue_by_name(QueueName=cfg.SQS_ALERT_QUEUE_NAME)
cfg.set_logger('botocore','botocore.log', level=20)
cfg.set_logger('boto3','boto3.log', level=20)
logger = cfg.set_logger(__name__,__name__+'.log')

class DealerSpace(socketio.Namespace):

    _registry = {}
    _usersById = {}
    _usersByName = {}


    def __init__(self, *args, **kwargs):
        super(DealerSpace, self).__init__(*args, **kwargs)
        spawn(self.alertsEngine)
        ulist = dao.App().getUsersList()
        for u in ulist:
            self._usersById[u['user_id']] = u
            self._usersByName[u['username']] = u

    def on_connect(self, *args, **kwargs):
        pass
        # self.emit('user_trigger', 'Dealer Connection Established', room=args[0])
        # self.emit('identify', 'identify')

    def on_disconnect(self, *args, **kwargs):
        if self.userName:
            DealerSpace._registry.pop(self.userName, None)

    def on_trigger(self, *args, **kwargs):
        pass
        # sleep(2)
        # self.emit('user_trigger', 'PENDING')
        # sleep(2)
        # self.emit('user_trigger', 'STAGED')
        # sleep(2)
        # self.emit('user_trigger', 'IN_PROCESS')
        # sleep(2)
        # self.emit('user_trigger', 'DONE')

    def on_userIdentify(self, *args, **kwargs):
        self.userName = args[1]
        if self.userName is dict:
            self.userName = 'tmp'
        self.sessionID = args[0]
        self.dateID = datetime.datetime.now()
        DealerSpace._registry[self.userName] = self
        usr = self._usersByName[self.userName]
        print DealerSpace._registry
        self.emit('user_trigger', 'Welcome {0} {1}'.format(usr['first_name'], usr['last_name']), room=args[0])

    def alertsEngine(self):
        while True:
            try:
                sleep(0.1)
                msgs = alertsQ.receive_messages(15, MessageAttributeNames=['provider'])

                if 0 == len(msgs):
                    continue

                for msg in msgs:
                    if msg.message_attributes is not None:
                        try:
                            provider_name = msg.message_attributes.get('provider').get('StringValue')
                            payload = json.loads(msg.body)
                            user_name = self._getUserName(payload['user_id'])
                            if provider_name in 'taboola':
                                self._broadcast_user(user_name, 'dealer_trigger', payload)
                                logger.info('Sent Payload to Taboola')
                            elif provider_name in 'revcontent':
                                self._broadcast_user(user_name, 'dealer_trigger', payload)
                                logger.info('Sent Payload to Revcontent')
                        except Exception as e:
                            logger.warning(e)
                            logger.warning(msg)
                    try:
                        logger.warning('Deleting Message')
                        res = msg.delete()
                        logger.info('Success Message Deleted')
                    except Exception as m:
                        logger.exception(m)
            except Exception as e:
                logger.exception(e)

    def _getUserName(self, userId):
        return self._usersById[int(userId)]['username']

    def _broadcast(self, event, message):
        print DealerSpace._registry
        for s in DealerSpace._registry.values():
            s.emit(event, message)

    def _broadcast_user(self, to, event, message):
        if len(DealerSpace._registry) is 0:
            pass
        else:
            try:
                s = DealerSpace._registry.get(to)
                s.emit(event, message, room=s.sessionID)
            except Exception as e:
                logger.warning(e)




