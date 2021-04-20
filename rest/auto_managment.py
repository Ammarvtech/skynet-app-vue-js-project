import libs.dao as dao
from libs.auto_managment import AutomationData
from rest.base import *
from rest.websites.website import validate_user_db_access

AutomationManagment = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@AutomationManagment.get('/api/reports/get_automation_data')
def get():
    sites = get_argument('sites')
    start = get_argument('start')
    end = get_argument('end')
    sources = get_argument('sources')
    status = get_argument('status')
    name = get_argument('name')
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    resp = {"data": AutomationData().get_automation_data(sites, sources, status, name, start, end, user_id)}

    return resp


@AutomationManagment.get('/api/reports/get_automation_names')
def get():
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow
    resp = {"data": AutomationData().get_automation_name()}
    return resp


@AutomationManagment.get('/api/reports/toggle_automation')
def get():
    site = get_argument('site')
    name = get_argument('name')
    active = get_argument('active')
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow
    resp = {"data": AutomationData().toggle_automation(site, name, active)}
    return resp
