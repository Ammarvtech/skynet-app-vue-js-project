import logging
from libs.dao import Dao


# import json


class CampaignInventory(Dao):
    def get_rev_campaign_inventory(self, campaign_id):
        query = "SELECT inventory_id, headline, target_url, image_url, brand_name, admin_status " \
                "FROM prv_revcontent_inventory " \
                "WHERE campaign_id = %s"
        try:
            inventory = self.db.query(query, campaign_id)
            return [] if inventory is None else inventory
        except Exception as e:
            logging.error(msg=e)

    def set_revcontent_inventory(self, campaign_id, inventory_id, item):
        query = "INSERT INTO prv_revcontent_inventory(" \
                "campaign_id, " \
                "inventory_id , " \
                "headline , " \
                "target_url , " \
                "image_url , " \
                "brand_name , " \
                "admin_status , " \
                "content_type) " \
                "VALUES (%s, %s ,%s ,%s ,%s ,%s ,%s ,%s ) "
        try:
            res = self.db.execute(query,
                            campaign_id,
                            'tmp_' + str(inventory_id),
                            item['headline'],
                            item['target_url'],
                            item['image'],
                            item['brand_name'],
                            'TBD',
                            item['content_type']
                            )
            return True
        except Exception, e:
            logging.error(msg=e)
            return -1

    def update_revcontent_inventory(self, campaign_id, item):
        query = "UPDATE prv_revcontent_inventory SET " \
                "target_url = %s, " \
                "image_url = %s, " \
                "headline = %s " \
                "WHERE campaign_id = %s " \
                "AND inventory_id = %s"
        try:
            res = self.db.execute(query,
                            item['target_url'],
                            item['image_url'],
                            item['headline'],
                            campaign_id,
                            item['inventory_id']
                            )
            return res
        except Exception as e:
            logging.error(msg=e)

    def get_campaign_site(self, campaign_id):
        query = "SELECT ws.website_name " \
                "FROM prv_revcontent_campaigns AS prv_c " \
                "INNER JOIN websites AS ws " \
                "ON prv_c.website_id = ws.website_id " \
                "WHERE prv_c.campaign_id = %s "
        try:
            data = self.db.query(query, campaign_id)
            return data[0]['website_name']
        except Exception, e:
            logging.error(msg=e)
            return False
