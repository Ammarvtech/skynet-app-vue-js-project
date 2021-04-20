import logging
import json
from libs.dao import Dao


class DynamicData(Dao):
    def get_dynamic_data(self, site_id, test, country, group, device, win, start, end ,user_id):
        query = "call sp_get_dynamic_data('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(site_id, test, country, group, device, win, start, end, user_id)
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_dynamic_all_data(self, site_id, test, country, group, device, win, start, end ,user_id):
        query = "call sp_get_dynamic_all_data('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(site_id, test, country, group, device, win, start, end, user_id)
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_dynamic_filters(self, start, end):
        query = "call sp_get_dynamic_filters('{0}','{1}');".format(start, end)
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message