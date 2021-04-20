import json

import libs.dao as dao
from rest.base import *

Dealer = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@Dealer.get('/api/dealer/data')
@authorize()
def get():
    try:
        date_start = get_argument('date_start') + " 00:00"
        date_end = get_argument('date_end') + " 23:59"
        if 'user_id' in request.query and request.query['user_id'] != '':
            user_id = get_argument("user_id")
        else:
            usr = authlayer.current_user
            user_id = dao.App().getUserID(usr.username)
        res = dict(enumerate(dao.Dealer().get_data_by_user_id(user_id, date_start, date_end), 0))

        for item in res.keys():
            res[item]['modification_date'] = ""
            status_data = json.loads(res[item]['status'])
            res[item]['status_name'] = status_data['value']
            if res[item]['source'] == 'Revcontent':
                account_data = json.loads(res[item]['account'])
                res[item]['account'] = account_data['client_id']

        return res

    except Exception as e:
        logger.exception(e.message)
        return False


@Dealer.get('/api/dealer/users')
@authorize()
def get():
    try:
        usr = authlayer.current_user
        user_id = dao.App().getUserID(usr.username)
        response = dict(enumerate(dao.App().getUsersList(user_id), 0))
        return response
    except Exception as e:
        logger.exception(e.message)
        return False
