import libs.dao as dao
from libs.hourly_roi import HourlyRoiData
from rest.base import *
from rest.websites.website import validate_user_db_access

HourlyRoi = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@HourlyRoi.get('/api/reports/get_hourly_roi_data')
def get():
    site = get_argument('site')
    start_date = get_argument('start_date')
    end_date = get_argument('end_date')
    campaign_id = get_argument('campaign_id')
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    resp = {"data": HourlyRoiData().get_hourly_roi_data(site, str(campaign_id), start_date, end_date)}
    return json.dumps(resp, indent=4, sort_keys=True, default=str)


