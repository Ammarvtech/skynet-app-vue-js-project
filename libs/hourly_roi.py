import logging
import json
from libs.dao import Dao


class HourlyRoiData(Dao):
    def get_hourly_roi_data(self, site, campaign_id, start_date, end_date):
        query = "call sp_get_hourly_campaign_roi('{0}','{1}','{2}','{3}')".format(site, campaign_id, start_date, end_date)
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

