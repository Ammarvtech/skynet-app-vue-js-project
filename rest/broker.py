import json
import libs.dao as dao
from rest.base import *
from libs.broker import BrokerData
from libs.dealer import Dealer

Broker = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@Broker.get('/api/broker/campaigns')
@authorize()
def get():
    resp = {}
    usr = authlayer.current_user
    user_id = dao.App().getUserID(usr.username)
    resp["campaigns"] = BrokerData().get_broker_campaigns()

    return resp


@Broker.get('/api/broker/campaigns/filter')
@authorize()
def get():
    resp = {}
    post_data = dict(request.query)
    provider_name = post_data["provider_name"]
    website_id = post_data["website_id"]

    resp["campaigns"] = BrokerData().get_filter_campaigns(provider_name, website_id)

    return resp


@Broker.post('/api/broker/delete/task')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    campaign_id = post_data["id"]

    resp["success"] = BrokerData().delete_task(campaign_id)
    resp["cid"] = campaign_id

    return json.dumps(resp)


@Broker.post('/api/broker/delete/interval')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    interval_id = post_data["id"]

    resp["campaigns"] = BrokerData().delete_inetrval(interval_id)

    return resp


@Broker.post('/api/broker/task')
@authorize()
def post():
    res = {}
    post_data = dict(request.json)
    updated = post_data["updated"]
    usr = authlayer.current_user
    user_id = dao.App().getUserID(usr.username)
    try:
        res["success"] = BrokerData().set_task(user_id, post_data["data"], updated)
        res["cid"] = post_data["data"]["campaign_id"]
        return json.dumps(res)
    except Exception as e:
        global logger
        logger.exception(e)
        return False
