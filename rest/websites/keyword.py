from rest.base import *
from libs.utils import get_account_details
from libs.dealer import Dealer
import gevent
import libs.dao as dao
import datetime

logger = cfg.set_logger(__name__,__name__+'.log')
dlr = Dealer()
Keywords = app()
response.content_type = 'application/json'

today = datetime.date.today()
yesterday = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")


@Keywords.get('/api/website/keywords')
def get_keywords():

    campaign_id = get_argument('campaign_id')
    site_id = get_argument('site_id')
    device = get_argument('device')
    source = get_argument('source')
    start = get_argument('start')
    end = get_argument('end')

    try:
        return dict(enumerate(dao.WebsiteStatistics().get_keywords(campaign_id, site_id, device, source, start, end), 0))
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Keywords.post('/api/website/revcontent/keyword/status_update')
@authorize()
def stop_keyword():

    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    target_id = request.json['tag_id']
    device = request.json['device']
    data_date = request.json['data_date']

    account = get_account_details(source, campaign_id)

    params_toggle_target = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id,
        "target_id": target_id,
        "device": device,
        "data_date": data_date
    }

    try:
        res = dlr.send(provider=source, action='toggle_target', params=params_toggle_target)
        if res.ok:
            gevent.spawn(keyword_status_update, 'PENDING', campaign_id, target_id, yesterday, device, 'revcontent')
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Keywords.post('/api/website/revcontent/keyword/cpc_update')
@authorize()
def keyword_cpc_update():

    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    tag_id = request.json['tag_id']
    new_bid = request.json['new_bid']
    device = request.json['device']
    data_date = request.json['data_date']

    account = get_account_details(source, campaign_id)

    params_update_target_bid = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id,
        "target_id": tag_id,
        "bid": new_bid,
        "device": device,
        "data_date": data_date
    }

    try:
        res = dlr.send(provider=source, action='update_target_bid', params=params_update_target_bid)
        if res.ok:
            gevent.spawn(keyword_status_update, 'PENDING', campaign_id, tag_id, yesterday, device, 'revcontent')
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Keywords.post('/api/website/keywords/revcontent/bid_bulk')
@authorize()
def keyword_cpc_bulk_update():

    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)

    keywords = request.json

    if keywords:
        site_id = keywords[0]['site_id']
        source = keywords[0]['source']
        campaign_id = keywords[0]['campaign_id']
        device = keywords[0]['device']
        data_date = keywords[0]['data_date']
        account = get_account_details(source, campaign_id)
        count = 0

        for key in keywords:
            keyword = key['keyword']
            bid = key['bid_adjust']
            params_update_target_bid = {
                "provider_id": account['provider_id'],
                "user_id": usr_id,
                "account_id": account['account_id'],
                "site_id": site_id,
                "campaign_id": campaign_id,
                "target_id": key['tag_id'],
                "bid": bid,
                "device": device,
                "data_date": data_date
            }
            try:
                res = dlr.send(provider=source, action='update_target_bid', params=params_update_target_bid)
                if res.ok:
                    gevent.spawn(keyword_status_update, 'PENDING', campaign_id, keyword, yesterday, device)
                    count = count + 1
            except Exception as e:
                global logger
                logger.exception(e)
                return {}

        if count == len(keywords):
            return "True"
    else:
        return "False"


def keyword_status_update(status, campaign_id, keyword, date, device, source):
    dao.WebsiteStatistics().update_keyword_status(status, campaign_id, keyword, date, device, source)


