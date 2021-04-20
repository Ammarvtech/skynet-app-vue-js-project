import logging
import libs.dao as dao
from rest.base import *
from libs.campaign_manager.inventory import CampaignInventory
from libs.dealer import Dealer
from libs.campaign_manager.properties import CampaignProperties
cmInventory = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@cmInventory.get('/api/campaignManager/inventory')
@authorize()
def get():
    resp = {}
    campaign_id = get_argument("cid")
    resp["inventory"] = CampaignInventory().get_rev_campaign_inventory(campaign_id)

    return resp


@cmInventory.post('/api/campaignManager/inventory')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    campaign_id = post_data['campaign_id']
    action = post_data['action']
    website_name = CampaignInventory().get_campaign_site(campaign_id)

    # update inventory in DB - pre API worker
    if len(post_data['new_items']):
        for idx, item in enumerate(post_data['new_items']):
            item["brand_name"] = website_name
            resp = CampaignInventory().set_revcontent_inventory(campaign_id, idx, item)
            if not resp:
                logging.error(msg="Failed to create inventory")
                return False
            else:
                post_data['new_items'][idx]['inventory_id'] = 'tmp_' + str(idx)
        if action in ['update']:
            dealer_add(campaign_id, post_data['new_items'])

    if len(post_data['updated_items']):
        for idx, item in enumerate(post_data['updated_items']):
            resp["success"] = CampaignInventory().update_revcontent_inventory(campaign_id, item)
            if not resp:
                logging.error(msg="Failed to update inventory")
                return False
        if action in ['update']:
            dealer_update(campaign_id, post_data['updated_items'])

        return {"resp": resp}


def dealer_update(campaign_id, updated_items):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignProperties().get_campaign_by_id(campaign_id)
    provider_id = CampaignProperties().get_provider_by_name(campaign['provider'].lower())

    params = {
        "provider_id": provider_id,
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": campaign_id,
        "args": {"items": updated_items, "action": "update"}
    }

    try:
        dlr = Dealer()
        res = dlr.send(provider='revcontent', action='update_inventory', params=params)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        raise e


def dealer_add(campaign_id, new_items):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaign = CampaignProperties().get_campaign_by_id(campaign_id)
    provider_id = CampaignProperties().get_provider_by_name(campaign['provider'].lower())

    params = {
        "provider_id": provider_id,
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": campaign_id,
        "items": new_items
    }

    try:
        dlr = Dealer()
        res = dlr.send(provider='revcontent', action='add_inventory', params=params)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        raise e
