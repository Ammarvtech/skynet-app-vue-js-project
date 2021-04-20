import libs.dao as dao
from rest.base import *
from libs.dealer import Dealer
from libs.campaign_manager.campaigns import CampaignsData

cmCampaigns = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@cmCampaigns.get('/api/campaignManager/campaigns')
@authorize()
def get():
    resp = {}
    resp["campaigns"] = CampaignsData().get_manager_campaigns()

    return resp


@cmCampaigns.get('/api/campaignManager/data')
@authorize()
def get():
    resp = {}

    resp["country_targets"] = CampaignsData().get_countries()
    resp["websites"] = CampaignsData().get_websites_list()
    resp["accounts"] = CampaignsData().get_prv_accounts()
    resp["providers"] = CampaignsData().get_providers()
    resp["profiles"] = CampaignsData().get_profiles()

    return resp


@cmCampaigns.post('/api/campaignManager/create')
@authorize()
def post():
    post_data = json.loads(request.body.buf)
    campaign_id = post_data['campaign_id']

    try:
        params = dealer_create(campaign_id)
        dlr = Dealer()
        res = dlr.send(provider='revcontent', action='create_campaign', params=params)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@cmCampaigns.post('/api/campaignManager/duplicate')
@authorize()
def post():
    post_data = dict(request.json)
    campaign_id = post_data['campaign_id']  # old id
    data = post_data['data']  # new data
    action = 'duplicate_multiple' if isinstance(data["profile_id"], int) else 'duplicate_campaign'

    try:
        params = dealer_duplicate(campaign_id, data)
        dlr = Dealer()
        res = dlr.send(provider='revcontent', action=action, params=params)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@cmCampaigns.post('/api/campaignManager/switch')
@authorize()
def post():
    post_data = dict(request.json)
    campaign_id = post_data['campaign_id']  # old id
    enabled = post_data['enabled']  # new data
    resp = CampaignsData().update_switch(campaign_id, enabled)

    if resp:
        try:
            params = dealer_switch(campaign_id, enabled)
            dlr = Dealer()
            res = dlr.send(provider='revcontent', action='set_campaign_status', params=params)
            return str(res.ok)
        except Exception as e:
            global logger
            logger.exception(e)
            return {}


def dealer_create(campaign_id):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignsData().get_campaign_by_id(campaign_id)  # old campaign

    params = {
        "provider_id": campaign['provider_id'],
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": campaign_id,
        "args": campaign
    }

    return params


def dealer_duplicate(campaign_id, data):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignsData().get_campaign_by_id(campaign_id)

    params = {
        "provider_id": campaign['provider_id'],
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": campaign_id,
        "new_data": data
    }

    return params


def dealer_switch(campaign_id, enabled):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignsData().get_campaign_by_id(campaign_id)

    params = {
        "provider_id": campaign['provider_id'],
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": campaign_id,
        "enabled": enabled
    }

    return params
