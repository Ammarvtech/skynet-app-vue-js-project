import libs.dao as dao
from libs.report_dynamic import DynamicData
from rest.base import *
from rest.websites.website import validate_user_db_access

ReportDynamic = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@ReportDynamic.get('/api/reports/get_dynamic_data')
def get():
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')
    device = get_argument('devices')
    country = get_argument('country')
    test = get_argument('test')
    group = get_argument('group')
    win = get_argument('win')
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    resp = {"data": DynamicData().get_dynamic_data(site_id, test, country, group, device, win, start, end ,user_id)}

    return resp

@ReportDynamic.get('/api/reports/get_dynamic_all_data')
def get():
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')
    device = get_argument('devices')
    country = get_argument('country')
    test = get_argument('test')
    group = get_argument('group')
    win = get_argument('win')
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    resp = {"data": DynamicData().get_dynamic_all_data(site_id, test, country, group, device, win, start, end ,user_id)}
    return resp


@ReportDynamic.get('/api/reports/get_dynamic_filters')
def get():
    start = get_argument('start')
    end = get_argument('end')

    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow
    try:
        myfilter = {}
        temp_resp = {'data' : DynamicData().get_dynamic_filters(start, end)}
        for d in temp_resp['data']:
             myfilter.update(json.loads(d['filters']))
        return myfilter
    except Exception as e:
        global logger
        logger.exception(e)
        return {}