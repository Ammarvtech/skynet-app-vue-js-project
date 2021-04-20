import bottle
import gevent

import libs.dao as dao
from libs.dealer import Dealer
from libs.utils import get_account_details
from rest.base import *
from rest.websites.medium import mediums_bid_adjust
from rest.websites.website import validate_user_db_access
from datetime import datetime, timedelta
from pytz import timezone

logger = cfg.set_logger(__name__, __name__ + '.log')
dlr = Dealer()
Campaigns = app()
response.content_type = 'application/json'


@Campaigns.post('/api/website/stop_campaign')
@authorize()
def stop_campaign():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['params']['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['params']['site_id']
    source = request.json['params']['source']
    campaign_id = request.json['params']['campaign_id']

    account = get_account_details(source, campaign_id, site_id)

    params_toggle_campaign = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,  
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id
    }

    try:
        res = dlr.send(provider=source, action='toggle_campaign', params=params_toggle_campaign)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/gemini/campaign/update_budget')
@authorize()
def update_gemini_budget():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    budget = request.json['new_budget']

    account = get_account_details(source, campaign_id)

    params_update_campaign_budget = {
        "provider_id": account['provider_id'],
        "account_id": account['account_id'],
        "user_id": usr_id,
        "site_id": site_id,
        "campaign_id": campaign_id,
        "budget": budget
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_budget', params=params_update_campaign_budget)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/gemini/campaign/bid_update')
@authorize()
def update_gemini_campaign_bid():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    new_bid = request.json['new_bid']
    old_bid = request.json['bid']
    adgroup_id = request.json['adgroup_id']

    account = get_account_details(source, campaign_id)

    params_campaign_bid = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id,
        "cpc": new_bid,
        "prev_cpc": old_bid,
        "adgroup_id": adgroup_id
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_bid', params=params_campaign_bid)
        if request.json['sessions'] == 'rt':
            params_campaign_bid['data_date'] = request.json['data_date']
            dao.Dealer().updateCampaignPixelStatus(params_campaign_bid)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/taboola/campaign/bid_update')
@authorize()
def update_taboola_campaign_bid():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    new_bid = request.json['new_bid']
    old_bid = request.json['bid']

    account = get_account_details(source, campaign_id)

    params_campaign_bid = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id,
        "cpc": new_bid,
        "prev_cpc": old_bid,
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_bid', params=params_campaign_bid)
        if request.json['sessions'] == 'rt':
            params_campaign_bid['data_date'] = request.json['data_date']
            dao.Dealer().updateCampaignPixelStatus(params_campaign_bid)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/campaign/roi_adjust')
@authorize()
def update_campaign_bid():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    new_campaign_bid = request.json['new_campaign_bid']
    previous_campaign_bid = request.json['bid']

    request.json['usr_id'] = usr_id
    account = get_account_details(source, campaign_id, site_id)

    params_campaign_bid = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id,
        "cpc": new_campaign_bid,
        "prev_cpc": previous_campaign_bid,
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_bid', params=params_campaign_bid)
        # gevent.spawn(mediums_bid_adjust, **request.json)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/taboola/campaign/update_budget')
@authorize()
def update_taboola_budget():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    budget = request.json['new_budget']

    account = get_account_details(source, campaign_id)

    params_update_campaign_budget = {
        "provider_id": account['provider_id'],
        "account_id": account['account_id'],
        "user_id": usr_id,
        "site_id": site_id,
        "campaign_id": campaign_id,
        "budget": budget
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_budget', params=params_update_campaign_budget)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/facebook/campaign/update_budget')
@authorize()
def update_facebook_budget():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    budget = request.json['new_budget']

    account = get_account_details(source, campaign_id)

    params_update_campaign_budget = {
        "provider_id": account['provider_id'],
        "account_id": account['account_id'],
        "user_id": usr_id,
        "site_id": site_id,
        "campaign_id": campaign_id,
        "budget": budget
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_budget', params=params_update_campaign_budget)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/facebook/campaign/bid_update')
@authorize()
def update_facebook_campaign_bid():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    new_bid = request.json['new_bid']
    old_bid = request.json['bid']

    account = get_account_details(source, campaign_id)

    params_campaign_bid = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id,
        "cpc": new_bid,
        "prev_cpc": old_bid,
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_bid', params=params_campaign_bid)
        if request.json['sessions'] == 'rt':
            params_campaign_bid['data_date'] = request.json['data_date']
            dao.Dealer().updateCampaignPixelStatus(params_campaign_bid)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}

@Campaigns.post('/api/website/zemanta/campaign/update_budget')
@authorize()
def update_zemanta_budget():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    budget = request.json['new_budget']

    account = get_account_details(source, campaign_id)

    params_update_campaign_budget = {
        "provider_id": account['provider_id'],
        "account_id": account['account_id'],
        "user_id": usr_id,
        "site_id": site_id,
        "campaign_id": campaign_id,
        "budget": budget
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_budget', params=params_update_campaign_budget)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}

@Campaigns.post('/api/website/zemanta/campaign/bid_update')
@authorize()
def update_zemanta_campaign_bid():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    new_bid = request.json['new_bid']
    old_bid = request.json['bid']

    account = get_account_details(source, campaign_id)

    params_campaign_bid = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id,
        "cpc": new_bid,
        "prev_cpc": old_bid,
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_bid', params=params_campaign_bid)
        if request.json['sessions'] == 'rt':
            params_campaign_bid['data_date'] = request.json['data_date']
            dao.Dealer().updateCampaignPixelStatus(params_campaign_bid)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}

@Campaigns.post('/api/website/outbrain/campaign/update_budget')
@authorize()
def update_outbrain_budget():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    budget = request.json['new_budget']
    account = get_account_details(source, campaign_id, site_id)


    params_update_campaign_budget = {
        "provider_id": account['provider_id'],
        "account_id": account['account_id'],
        "user_id": usr_id,
        "site_id": site_id,
        "campaign_id": campaign_id,
        "budget": budget,
        "budget_id": account['budget_id']
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_budget', params=params_update_campaign_budget)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}

@Campaigns.post('/api/website/outbrain/campaign/bid_update')
@authorize()
def update_outbrain_campaign_bid():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    new_bid = request.json['new_bid']
    old_bid = request.json['bid']

    account = get_account_details(source, campaign_id, site_id)

    params_campaign_bid = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id,
        "cpc": new_bid,
        "prev_cpc": old_bid,
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_bid', params=params_campaign_bid)
        if request.json['sessions'] == 'rt':
            params_campaign_bid['data_date'] = request.json['data_date']
            dao.Dealer().updateCampaignPixelStatus(params_campaign_bid)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/revcontent/campaign/change_budget')
@authorize()
def update_revcontent_budget():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow

    site_id = request.json['site_id']
    source = request.json['source']
    campaign_id = request.json['campaign_id']
    budget = request.json['budget']

    account = get_account_details(source, campaign_id)

    params_update_campaign_budget = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "account_id": account['account_id'],
        "site_id": site_id,
        "campaign_id": campaign_id,
        "budget": budget
    }

    try:
        res = dlr.send(provider=source, action='update_campaign_budget', params=params_update_campaign_budget)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/taboola/campaign/duplicate')
@authorize()
def duplicate_taboola_campaign():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    login_time = request.json['login_time']
    allow = validate_user_db_access(usr_id, login_time)
    if allow.status_code != 200:
        return allow
    # init campaigns duplicated via app with start date tomorrow
    est_time = timezone('EST')
    tomorrow = (datetime.now(est_time) + timedelta(days=1)).strftime('%Y-%m-%d')
    username = usr.username.encode('utf-8')
    site_id = request.json['dst_payload']['site_id']
    source = request.json['dst_payload']['source']
    campaign_id = request.json['dst_payload']['campaign_id']
    template_params = request.json['dst_payload']['dst_params']
    template_params['start_date'] = tomorrow

    account = get_account_details(source, campaign_id)

    for k, v in template_params.items():
        try:
            template_params[k] = json.loads(v)
        except (TypeError, ValueError):
            pass

    template_params.pop('duplicate_id')
    params_duplicate_campaign = {
        "provider_id": account['provider_id'],
        "user_id": usr_id,
        "username": username,
        "account_id": account['account_id'],
        "site_id": site_id,
        "medium": template_params.pop('medium', 'dup: missing medium'),
        "campaign_id": campaign_id,
        "dst_params": template_params
    }

    try:
        res = dlr.send(provider=source, action='duplicate_campaign', params=params_duplicate_campaign)
        return str(res.ok)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/gemini/campaign/duplicate')
def duplicate_gemini_campaign():
    campaign_id = request.json['campaign_id']
    audience_groups = dao.App().get_gemini_3p_audiences()
    all_requests_passed = True
    res = {}

    try:
        site_id = dao.Campaigns().get_gemini_campaign_site(campaign_id)[0]['site_id']
    except IndexError:
        return bottle.HTTPResponse(status=400, body={'Invalid Campaign ID': campaign_id})

    for audience_group in audience_groups:
        params = {
            "user_id": 5,  # Dealer User ID
            "provider_id": 4,  # Gemini provider ID
            "site_id": site_id,
            "account_id": 171,  # Gemini account ID
            "campaign_id": campaign_id,
            "audience_group": audience_group['audience_display_name'],
            "dst_params": {}
        }

        try:
            res = dlr.send(provider='gemini', action='duplicate_campaign', params=params)
        except Exception as e:
            global logger
            logger.exception(e)
            all_requests_passed = False

    if all_requests_passed:
        return str(res.ok)
    else:
        return {}


@Campaigns.get('/api/website/chart_data/campaign')
@authorize()
def chart():
    site_id = get_argument('site_id')
    campaign_id = get_argument('campaign_id')
    device = get_argument('device')
    source = get_argument('source')
    start = get_argument('start')
    end = get_argument('end')

    try:
        data = dao.WebsiteStatistics().get_campaign_chart_data(site_id, campaign_id, device, source, start, end)
        for item in data:
            item['profit'] = item['revenue'] - item['cost']

        return dict(enumerate(data, 0))
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.get('/api/website/campaign/automation_toggle')
@authorize()
def automation_toggle():
    usr = authlayer.current_user
    user_id = dao.App().getUserID(usr.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    target_value = get_argument('target_value')
    is_active = get_argument('is_active')
    user_id = user_id

    role_id = '-1'
    target_type = '2'

    data = [{'user_id': user_id, 'target_value': target_value, 'is_active': is_active, 'role_id': role_id, 'target_type': target_type}]

    try:
        dao.Campaigns().update_automation_status(data)
        return "True"
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Campaigns.post('/api/website/campaigns/bulk')
@authorize()
def bulk_update():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    campaigns = request.json

    if campaigns:
        # handle if single campaign
        if not isinstance(campaigns, list):
            campaigns = [campaigns]

        login_time = campaigns[0]['login_time']
        allow = validate_user_db_access(usr_id, login_time)
        if allow.status_code != 200:
            return allow

        for campaign in campaigns:
            site_id = campaign['site_id']
            campaign_id = campaign['campaign_id']
            source = campaign['source']
            account = get_account_details(source, campaign_id, site_id)

            params = {
                "provider_id": account['provider_id'],
                "user_id": usr_id,
                "account_id": account['account_id'],
                "site_id": site_id,
                "campaign_id": campaign_id,
                "cpc": campaign['bid_adjust']
            }

            try:
                dlr.send(provider=source, action='update_campaign_bid', params=params)
            except Exception as e:
                global logger
                logger.exception(e)
        return "True"
    else:
        return "False"
