import json, requests
import config.cfg as cfg

HOST = cfg.DEALER_HOST

PROVIDERS = ['revcontent', 'taboola']

PROVIDERS_ACTIONS = {
    'revcontent':
        {
            'update_target_bid': ['user_id', 'provider_id', 'account_id', 'site_id', 'campaign_id', 'tag_id', 'bid'],
            'toggle_target': ['user_id', 'provider_id', 'account_id', 'site_id', 'campaign_id', 'target_id'],
            'toggle_medium': ['user_id', 'provider_id', 'account_id', 'site_id', 'campaign_id', 'medium'],
            'toggle_campaign': ['user_id', 'provider_id', 'account_id', 'site_id', 'campaign_id']
        },
    'taboola': {
            'update_campaign_bid': ['user_id', 'provider_id', 'account_id', 'site_id', 'campaign_id', 'cpc'],
            'toggle_medium': ['user_id', 'provider_id', 'account_id', 'site_id', 'campaign_id', 'medium'],
            'update_medium_bid': ['user_id', 'provider_id', 'account_id', 'site_id', 'campaign_id', 'medium',
                                  'cpc_modification'],
            'toggle_campaign': ['user_id', 'provider_id', 'account_id', 'site_id', 'campaign_id']

        }
}

PAYLOAD_TEMPLATE = ['provider', 'action', 'params']


def validate(schema=PROVIDERS_ACTIONS):
    def decorator(function):
        def validator(*args, **kwargs):
            fields = [x for x in PAYLOAD_TEMPLATE]
            bad_fields = []
            if kwargs:
                # Single Object
                # Initial Template Validation
                for key, value in kwargs.iteritems():
                    if key in fields:
                        continue
                    else:
                        bad_fields.append(key)
                    if len(bad_fields) > 0:
                        msg = 'Mismatch in Received Fields: {0} \n Expected Fields: {1}'.format(
                            json.dumps(bad_fields), json.dumps(fields))
                        raise AttributeError(msg)
                # Inner Params Validation
                provider = kwargs.get('provider')
                action = kwargs.get('action')
                params = kwargs.get('params')
                params_fields = schema[provider][action]
                for key, val in params.iteritems():
                    if key in params_fields:
                        continue
                    else:
                        bad_fields.append(key)
                    if len(bad_fields) > 0:
                        msg = 'Mismatch in Received Fields: {0} \n Expected Fields: {1}'.format(
                            json.dumps(bad_fields), json.dumps(fields))
                        raise AttributeError(msg)


            elif args and len(args) > 1:
                # Many Objects
                obj = args[1]
                for key, value in obj.iteritems():
                    if key in fields:
                        continue
                    else:
                        bad_fields.append(key)
                    # Inner Params Validation
                    if len(bad_fields) > 0:
                        msg = 'Mismatch in Received Fields: {0} \n Expected Fields: {1}'.format(
                             json.dumps(bad_fields), json.dumps(fields))
                        raise AttributeError(msg)

                provider = obj.get('provider')
                action = obj.get('action')
                params = obj.get('params')
                params_fields = schema[provider][action]
                for key, val in params.iteritems():
                    if key in params_fields:
                        continue
                    else:
                        bad_fields.append(key)
                    if len(bad_fields) > 0:
                        msg = 'Mismatch in Received Fields: {0} \n Expected Fields: {1}'.format(
                            json.dumps(bad_fields), json.dumps(fields))
                        raise AttributeError(msg)


            return function(*args, **kwargs)

        return validator

    return decorator

session = requests.session()

class Dealer(object):
    def __init__(self):
        self.ses = session
        self.uri = 'http://{0}:5000/put'.format(HOST)

    def health(self):
        pass

    def send(self, *args, **kwargs):
        '''
        :param args:
            payload (dict): should contain provider, action, params
        :param kwargs:
            provider (str): provider name Taboola, Revcontent
            action (str): action type
            params (dict):action required params
        :return:
            http status confirmation from dealer
        '''
        try:
            payload = None
            if kwargs:
                payload = kwargs
            if args:
                payload = args[0]
            r = self.ses.post(self.uri, json=payload)
            return r
        except:
            pass

if __name__ == '__main__':

    # Test Use Cases
    dlr = Dealer()
    # Send Dict
    # pyld = {'provider':'taboola','action':'toggle_campaign','params':{'campaign_id':''}}
    # dlr.send(pyld)
    # Use Arguments
    # dlr.send(provider='taboola', action='toggle_campaign', params={})
