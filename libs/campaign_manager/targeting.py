import logging
from libs.dao import Dao
# import json


class CampaignTargeting(Dao):
    def get_revcontent_targeting(self, campaign_id):
        campaign_id = '%{0}%'.format(campaign_id)
        sql = "SELECT tag_name,bid,tag_id,enabled,avg_cpc,clicks_week,min_bid,max_bid " \
              "FROM prv_revcontent_targeting " \
              "WHERE campaign_id LIKE %s"
        try:
            data = self.db.query(sql, campaign_id)
            return data
        except Exception as e:
            logging.error(msg=e)

    def update_rev_targeting(self, campaign_id, keywords, multiple):
        try:
            if multiple:
                sql = "UPDATE prv_revcontent_targeting SET bid = %s " \
                      "WHERE campaign_id = %s"
                self.db.execute(sql, keywords[0]['bid'], campaign_id)
            else:
                sql = "UPDATE prv_revcontent_targeting SET bid = %s " \
                      "WHERE campaign_id = %s AND tag_id = %s"
                self.db.execute(sql, keywords['bid'], campaign_id, keywords['tag_id'])
            return True
        except Exception, e:
            logging.error("failed to update target")
            logging.exception(e.message)
            return -1

    def update_revcontent_target_status(self, campaign_id, status, tag_id):

        sql = "UPDATE prv_revcontent_targeting SET enabled = %s " \
              "WHERE campaign_id = %s AND tag_id = %s"
        try:
            self.db.execute(sql, status, campaign_id, tag_id)
            return 1
        except Exception, e:
            logging.error("failed to update target")
            logging.exception(e.message)
            return -1