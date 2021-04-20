from rest.base import *
import libs.dao as dao
from libs.campaign_manager.properties import CampaignProperties
from libs.dealer import Dealer

cmProperties = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@cmProperties.get('/api/campaignManager/properties')
@authorize()
def get():
    resp = dict()
    usr = authlayer.current_user
    user_id = dao.App().getUserID(usr.username)

    resp["country_targets"] = CampaignProperties().get_countries()
    resp["websites"] = CampaignProperties().get_websites_list(user_id)
    resp["accounts"] = CampaignProperties().get_accounts()
    resp["providers"] = CampaignProperties().get_providers()

    try:
        campaign_id = get_argument("cid")
        resp["campaign"] = CampaignProperties().get_campaign_by_id(campaign_id)
    except Exception as e:
        logger.error(msg=e)
    return resp


@cmProperties.post('/api/campaignManager/properties')
@authorize()
def post():
    post_data = dict(request.json)
    campaign_data = post_data['form_data']
    action = post_data['action']

    if action in ['create']:
        res = CampaignProperties().set_campaign(campaign_data)
        cid = res[0]['campaign_id']
        CampaignProperties().set_revcontent_targeting(cid, campaign_data['default_bid'])

    elif action in ['update']:
        cid = post_data['campaign_id']
        omg_id = CampaignProperties().get_campaign_by_id(cid)['id']
        is_global_bid = CampaignProperties().new_global_bid(cid, campaign_data['default_bid'])
        res = CampaignProperties().update_campaign_properties(campaign_data, omg_id, cid)

        if res:
            dealer(campaign_data, cid)
    else:
        cid = None

    return {'cid': cid}


def dealer(campaign, cid):
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    provider_id = CampaignProperties().get_provider_by_name(campaign['provider_name'])

    params = {
        "provider_id": provider_id,
        "user_id": usr_id,
        "account_id": campaign['account_id'],
        "site_id": campaign['website_id'],
        "campaign_id": cid
    }

    try:
        dlr = Dealer()
        res = dlr.send(provider='revcontent', action='update_properties', params=params)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        raise e

