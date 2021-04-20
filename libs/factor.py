import logging
import json
from libs.dao import Dao


class FactorData(Dao):
    def set_factor(self, factor, date):
        query = "UPDATE dfp_factor SET factor = '{0}';".format(factor)
        try:
            data = self.db.query(query)
            # call funtion to update history
            self.set_history_factor(factor, date)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def set_history_factor(self,factor,date):
        query = "INSERT INTO factor_history (factor,data_date) VALUES ('{0}','{1}'); ".format(factor, date)
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_factor_data(self):
        query = "SELECT id, date(data_date) AS data_date,CAST(((1 - factor)*100) AS DECIMAL(10,2)) as factor FROM factor_history ORDER BY id DESC LIMIT 3"

        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message
