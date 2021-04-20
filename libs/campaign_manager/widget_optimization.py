import logging
import json
from libs.dao import Dao


class CampaignWidgets(Dao):
    def get_widgets(self, campaign_id):
        query = "SELECT  JSON_EXTRACT(widget_ids,'$**.id') AS widget_ids FROM prv_revcontent_widget_optimizer " \
                "WHERE campaign_id = %s"
        try:
            widget_ids = self.db.query(query, campaign_id)
            return [] if widget_ids is None else widget_ids[0]['widget_ids']
        except Exception as e:
            logging.error(msg=e)

    def save_widgets(self, campaign_id, op_type, widget_ids):
        ids_json = map(lambda x: {"id": x}, widget_ids)

        query = "INSERT INTO prv_revcontent_widget_optimizer SET " \
                "campaign_id = %s, " \
                "typ = %s, " \
                "widget_ids = %s " \
                "ON DUPLICATE KEY UPDATE " \
                "widget_ids = %s "
        try:
            self.db.execute(query, campaign_id, op_type, json.dumps(ids_json), json.dumps(ids_json))
            return "True"
        except Exception as e:
            logging.error(msg=e)

    def get_type(self, campaign_id):
        query = "SELECT  typ from prv_revcontent_widget_optimizer " \
                "WHERE campaign_id = %s"

        try:
            w_type = self.db.query(query, campaign_id)
            return [] if w_type is None else w_type[0]["typ"]
        except Exception as e:
            logging.error(msg=e)

    def set_type(self, w_type, campaign_id):
        query = "UPDATE prv_revcontent_widget_optimizer SET typ = %s " \
                "WHERE campaign_id = %s"

        try:
            self.db.query(query, w_type, campaign_id)
            return True
        except Exception as e:
            logging.error(msg=e)

    def delete_all(self, campaign_id):
        query = "UPDATE prv_revcontent_widget_optimizer " \
                "SET widget_ids = '[]' " \
                "WHERE campaign_id = %s"
        try:
            self.db.query(query, campaign_id)
            return True
        except Exception as e:
            logging.error(msg=e)



