import logging
from rest.base import *
import libs.dao as dao
from libs.campaign_manager.targeting import CampaignTargeting

cmTargeting = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')
from libs.dealer import Dealer
from libs.campaign_manager.campaigns import CampaignsData

@cmTargeting.get('/api/campaignManager/targeting')
@authorize()
def get():
    resp = {}
    campaign_id = get_argument("cid")
    resp["targeting"] = CampaignTargeting().get_revcontent_targeting(campaign_id)

    return resp


@cmTargeting.post('/api/campaignManager/targeting')
@authorize()
def post():
    post_data = dict(request.json)
    campaign_id = post_data['campaign_id']
    keywords = post_data['keywords']
    multiple = post_data['multiple']
    action = post_data['action']

    resp = CampaignTargeting().update_rev_targeting(campaign_id, keywords, multiple)

    if resp and action in ['update']:
        try:
            params = dealer_targeting_bid(campaign_id, keywords, multiple)
            dlr = Dealer()
            if multiple:
                res = dlr.send(provider='revcontent', action='update_all_bids', params=params)
            else:
                res = dlr.send(provider='revcontent', action='update_single_bid', params=params)
            return str(res.ok)
        except Exception as e:
            global logger
            logger.exception(e)
            return False


@cmTargeting.post('/api/campaignManager/targeting/status')
@authorize()
def post():
    post_data = dict(request.json)
    campaign_id = post_data['campaign_id']
    tag_id = post_data['keyword']['tag_id']
    status = post_data['keyword']['enabled']
    action = post_data['action']

    resp = CampaignTargeting().update_revcontent_target_status(campaign_id, status, tag_id)

    if resp and action == "update":
        try:
            params = dealer_targeting_status(campaign_id, tag_id, status)
            dlr = Dealer()
            res = dlr.send(provider='revcontent', action='update_single_status', params=params)
            return str(res.ok)
        except Exception as e:
            global logger
            logger.exception(e)
            return False


def dealer_targeting_bid(campaign_id, keywords, multiple):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignsData().get_campaign_by_id(campaign_id)

    if not multiple:
        params = {
            "provider_id": campaign['provider_id'],
            "user_id": usr_id,
            "account_id": campaign['account_id'],
            "site_id": campaign['website_id'],
            "campaign_id": campaign_id,
            "args": keywords
        }

    else:
        params = {
            "provider_id": campaign['provider_id'],
            "user_id": usr_id,
            "account_id": campaign['account_id'],
            "site_id": campaign['website_id'],
            "campaign_id": campaign_id,
            "bid": keywords[0]['bid']
        }
    return params


def dealer_targeting_status(campaign_id, tag_id, status):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignsData().get_campaign_by_id(campaign_id)

    params = {
        "provider_id": campaign['provider_id'],
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": campaign_id,
        "tag_id": tag_id,
        "tag_status": status
    }

    return params
