import datetime
from datetime import timedelta

import gevent

import libs.dao as dao
from libs.dealer import Dealer
from libs.utils import get_account_details
from rest.base import *
from rest.websites.website import validate_user_db_access

logger = cfg.set_logger(__name__, __name__ + '.log')
dlr = Dealer()
Mediums = app()
response.content_type = 'application/json'

today = datetime.date.today()
yesterday = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")


@Mediums.get('/api/website/mediums')
def get_mediums():
    campaign_id = get_argument('campaign_id')
    site_id = get_argument('site_id')
    device = get_argument('device')
    source = get_argument('source')
    start = get_argument('start')
    end = get_argument('end')

    try:
        return dict(enumerate(dao.WebsiteStatistics().get_mediums(campaign_id, site_id, device, source, start, end), 0))
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Mediums.get('/api/website/block_mediums')
def get_mediums():
    campaign_id = get_argument('campaign_id')
    site_id = get_argument('site_id')
    device = get_argument('device')
    source = get_argument('source')
    start = str(today - timedelta(days=15))
    end = get_argument('end')

    try:
        return dict(enumerate(dao.WebsiteStatistics().get_lost_mediums(campaign_id, site_id, device, source, start, end), 0))
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Mediums.post('/api/website/mediums/taboola/bulk')
@authorize()
def taboola_bulk_update():

    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    mediums = request.json

    if mediums:
        # handle if single medium
        if not isinstance(mediums, list):
            mediums = [mediums]

        login_time = mediums[0]['login_time']
        allow = validate_user_db_access(usr_id, login_time)
        if allow.status_code != 200:
            return allow

        site_id = mediums[0]['site_id']
        source = mediums[0]['source']
        campaign_id = mediums[0]['campaign_id']
        data_date = mediums[0]['data_date']
        device = mediums[0]['device']
        action = mediums[0]['action']
        account = get_account_details(source, campaign_id)
        mediums_array = []
        action_type = None
        bid = None

        for med in mediums:

            if action == 'bid':
                action_type = 'update_bulk_medium_bid'
                bid = float(med['bid'])
            elif action == 'toggle':
                bid = 1.0
                action_type = 'toggle_bulk_medium'
            elif action == 'roi':
                action_type = 'update_bulk_medium_bid'
                bid = float(med['bid_adjust'])

            params_update_medium = {
                "provider_id": account['provider_id'],
                "user_id": usr_id,
                "account_id": account['account_id'],
                "site_id": site_id,
                "campaign_id": campaign_id,
                "medium": med['medium'],
                "cpc_modification": bid,
                "data_date": data_date,
                "device": device,
                "type": action
            }
            mediums_array.append(params_update_medium)
        try:
            res = dlr.send(provider=source, action=action_type, params=mediums_array)
            if res.ok:
                for med in mediums:
                    medium = med['medium']
                    gevent.spawn(medium_status_update, 'PENDING', campaign_id, medium, device, data_date)
            return "True"
        except Exception as e:
            global logger
            logger.exception(e)
            return {}
    else:
        return "False"


def taboola_roi_bulk_bid_update(roi_mediums=None, **kwargs):

    if roi_mediums:
        site_id = kwargs['site_id']
        source = kwargs['source']
        campaign_id = kwargs['campaign_id']
        data_date = kwargs['data_date']
        device = kwargs['device']
        account = get_account_details(source, campaign_id)

        for med in roi_mediums:
            try:
                calc_bid = med['final_uv'] / kwargs['new_roi']
                medium_new_bid = (calc_bid / kwargs['new_campaign_bid']) - 1
                bid_adjust = 1 + medium_new_bid

                if bid_adjust > 1:
                    bid_adjust = 1
                elif bid_adjust < 0.5:
                    bid_adjust = 0.5

                params_update_medium_bid = {
                    "provider_id": account['provider_id'],
                    "user_id": kwargs['usr_id'],
                    "account_id": account['account_id'],
                    "site_id": site_id,
                    "campaign_id": campaign_id,
                    "medium": med['medium'],
                    "cpc_modification": float(bid_adjust),
                    "data_date": data_date,
                    "device": device
                }

                res = dlr.send(provider=source, action='update_bulk_medium_bid', params=params_update_medium_bid)
                if res.ok:
                    gevent.spawn(medium_status_update, 'PENDING', campaign_id, med['medium'], device, yesterday)

            except Exception as e:
                global logger
                logger.exception(e)
                continue


def mediums_bid_adjust(**kwargs):
    start = end = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    mediums = dao.WebsiteStatistics().get_adjust_mediums(kwargs['campaign_id'], kwargs['site_id'], kwargs['device'], kwargs['source'], start, end)
    if mediums:
        taboola_bulk_update(mediums, **kwargs)


def medium_status_update(status, campaign_id, medium, device, data_date):
    dao.WebsiteStatistics().update_medium_status(status, campaign_id, medium, device, data_date)
