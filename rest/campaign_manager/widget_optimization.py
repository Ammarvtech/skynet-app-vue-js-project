import json
import logging
from rest.base import *
import libs.dao as dao
from libs.dealer import Dealer
from libs.campaign_manager.widget_optimization import CampaignWidgets
from libs.campaign_manager.campaigns import CampaignsData

cmWidgetOpt = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@cmWidgetOpt.get('/api/campaignManager/wio')
@authorize()
def get():
    resp = {}
    campaign_id = get_argument("cid")

    try:
        widget_ids = CampaignWidgets().get_widgets(campaign_id)
        resp["widget_ids"] = json.loads(widget_ids)
    except Exception as e:
        logging.error(msg=e)
        return False

    return resp


@cmWidgetOpt.post('/api/campaignManager/wio')
@authorize()
def post():
    post_data = dict(request.json)
    campaign_id = post_data['campaign_id']
    widget_type = post_data['type']
    widget_ids = post_data['widget_ids']
    action = post_data['action']

    try:
        widget_ids = combine_ids(campaign_id, widget_ids)
        resp = CampaignWidgets().save_widgets(campaign_id, widget_type, widget_ids)

        if resp and action in ['update']:
            params = dealer_add_wio(campaign_id, widget_ids, widget_type)
            dlr = Dealer()
            res = dlr.send(provider='revcontent', action='update_widgets', params=params)

            return str(res.ok)

    except Exception as e:
        logging.error(msg=e)
        return False

    return resp


@cmWidgetOpt.get('/api/campaignManager/wio/type')
@authorize()
def get():
    resp = {}
    campaign_id = get_argument("cid")

    try:
        resp["type"] = CampaignWidgets().get_type(campaign_id)
    except Exception as e:
        logging.error(msg=e)
        return False

    return resp


@cmWidgetOpt.post('/api/campaignManager/wio/type')
@authorize()
def post():
    post_data = dict(request.json)
    campaign_id = post_data['campaign_id']
    w_type = post_data['type']
    action = post_data['action']
    widget_ids = post_data['widget_ids']
    try:
        widget_ids = [int(i) for i in widget_ids]
        resp = CampaignWidgets().set_type(w_type, campaign_id)
        if resp and action in ['update']:
            params = dealer_type_wio(campaign_id, w_type, widget_ids)
            dlr = Dealer()
            res = dlr.send(provider='revcontent', action='update_widgets', params=params)

            return str(res.ok)
    except Exception as e:
        logging.error(msg=e)
        return False

    return resp


@cmWidgetOpt.post('/api/campaignManager/wio/delete')
@authorize()
def post():
    post_data = dict(request.json)
    campaign_id = post_data['campaign_id']
    is_single = post_data['single']
    widget_ids = post_data['widget_ids']
    action = post_data['action']
    widget_type = post_data['type']
    ids_list = {}

    try:
        if not is_single:
            resp = CampaignWidgets().delete_all(campaign_id)
        else:
            current_ids = CampaignWidgets().get_widgets(campaign_id)
            ids_list = json.loads(current_ids)
            ids_list.remove(int(widget_ids))
            resp = CampaignWidgets().save_widgets(campaign_id, widget_type, ids_list)

        if resp and action in ['update']:
            params = dealer_delete_widgets(campaign_id, widget_ids, is_single)
            dlr = Dealer()
            res = dlr.send(provider='revcontent', action='delete_widgets', params=params)

            return str(res.ok)

    except Exception as e:
        logging.error(msg=e)
        return False

    return resp

    ###############################################
    #                 Dealer Utils                #
    ###############################################


def dealer_add_wio(campaign_id, widget_ids, w_type):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignsData().get_campaign_by_id(campaign_id)

    params = {
        "provider_id": campaign['provider_id'],
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": campaign_id,
        "widget_ids": json.dumps(widget_ids)[1:-1],
        "widget_type": w_type
    }

    return params


def dealer_type_wio(campaign_id, w_type, widget_ids):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignsData().get_campaign_by_id(campaign_id)

    params = {
        "provider_id": campaign['provider_id'],
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": campaign_id,
        "widget_type": w_type,
        "widget_ids": json.dumps(widget_ids)[1:-1]
    }

    return params


def dealer_delete_widgets(campaign_id, widget_ids, is_single):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignsData().get_campaign_by_id(campaign_id)

    if not is_single:
        widget_ids = json.dumps(widget_ids)[1:-1]
    params = {
        "provider_id": campaign['provider_id'],
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": campaign_id,
        "widget_ids": widget_ids
    }

    return params

    ###############################################
    #                 Script Utils                #
    ###############################################


def combine_ids(campaign_id, new_ids):
    old_to_combine = []
    current_ids = CampaignWidgets().get_widgets(campaign_id)
    if current_ids:
        old_to_combine = json.loads(current_ids)
    new_to_combine = [int(x) for x in new_ids]
    combined = old_to_combine + new_to_combine

    return combined
