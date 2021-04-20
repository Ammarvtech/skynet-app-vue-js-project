from rest.base import *
import libs.realtime.campaigns as dao

logger = cfg.set_logger(__name__,__name__+'.log')
RTCampaigns = app()
response.content_type = 'application/json'


@RTCampaigns.get('/api/realtime/campaigns')
@authorize(role="admin", fail_redirect='/')
def get_campaigns():
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')
    try:
        resp = {}
        resp["campaigns"] = json.loads(dao.RTCampaigns().getCampaigns(site_id, start, end))
        return resp
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@RTCampaigns.get('/api/realtime/campaigns/:campaign')
@authorize(role="admin", fail_redirect='/')
def get_campaigns(campaign):
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')
    resp = {}
    try:
        resp["campaigns"] = json.loads(dao.RTCampaigns().getCampaign(site_id, start, end, campaign))
        return resp
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@RTCampaigns.get('/api/realtime/campaigns/delta/:campaign')
@authorize(role="admin", fail_redirect='/')
def get_campaigns(campaign):
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')
    resp = {}
    try:
        resp["campaigns"] = json.loads(dao.RTCampaigns().getCampaignDelta(site_id, start, end, campaign))
        return resp
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@RTCampaigns.get('/api/realtime/campaigns/summary')
@authorize(role="admin", fail_redirect='/')
def get_campaigns():
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')
    resp = {}
    try:
        resp["campaigns"] = json.loads(dao.RTCampaigns().getCampaignsSiteSummary(site_id, start, end))
        return resp
    except Exception as e:
        global logger
        logger.exception(e)
        return {}

@RTCampaigns.get('/api/realtime/campaigns/mediums/:campaign')
@authorize(role="admin", fail_redirect='/')
def get_campaigns(campaign):
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')
    try:
        resp = {}
        resp["campaigns"] = json.loads(dao.RTCampaigns().getMediums(site_id, start, end, campaign))
        return resp
    except Exception as e:
        global logger
        logger.exception(e)
        return {}