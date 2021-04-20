from rest.base import *
import libs.dao as dao
from libs.utils import validate_args

logger = cfg.set_logger(__name__,__name__+'.log')

Devices = app()
response.content_type = 'application/json'


@Devices.get('/api/website/devices')
def get_devices():

    campaign_id = get_argument('campaign_id')
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')

    try:
        return dict(enumerate(dao.WebsiteStatistics().get_device_data(campaign_id, site_id, start, end), 0))
    except Exception as e:
        global logger
        logger.exception(e)
        return {}
