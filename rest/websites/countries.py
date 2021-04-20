from rest.base import *
import libs.dao as dao
from libs.utils import validate_args

logger = cfg.set_logger(__name__,__name__+'.log')

Countries = app()
response.content_type = 'application/json'


@Countries.get('/api/website/countries')
def get_countries():

    campaign_id = get_argument('campaign_id')
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')

    try:
        return dict(enumerate(dao.WebsiteStatistics().get_country_data(campaign_id, site_id, start, end), 0))
    except Exception as e:
        global logger
        logger.exception(e)
        return {}
