import logging
from libs.dao import Dao
import json


class CampaignsData(Dao):
    def get_countries(self):
        query = "SELECT * FROM prv_revcontent_countries"
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_profiles(self):
        query = "SELECT id, user_id, name FROM prv_user_profile"
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_websites_list(self):
        sql = "SELECT DISTINCT w.website_id, w.website_name, w.acronym " \
              "FROM websites w " \
              "JOIN website_users u " \
              "ON w.website_id = u.website_id " \
              "WHERE w.website_status_id = 1 " \
              "ORDER BY w.website_name ASC"
        data = self.db.query(sql)
        return data

    def get_prv_accounts(self):
        query = "SELECT account_id, replace(JSON_EXTRACT(account_json,'$.client_id'),'\"','') AS account_name " \
                "FROM prv_accounts " \
                "GROUP BY account_name " \
                "ORDER BY account_name ASC"
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_providers(self):
        query = "SELECT provider_id, provider_name " \
                "FROM prv_providers " \
                "ORDER BY provider_name ASC"
        try:
            data = self.db.query(query)
            return data
        except Exception, e:
            logging.exception(e.message)
            return -1, e.message

    def get_campaign_by_id(self, campaign_id):
        query = "SELECT rc.id, rc.website_id, rc.account_id, rc.campaign_id, " \
                "rc.campaign_name, rc.start_date, rc.end_date, rc.targeting_type, " \
                "rc.enabled, rc.status, rc.bid_type, rc.default_bid, rc.min_bid, " \
                "rc.max_bid, rc.budget, rc.cost, ctr,rc.utm_codes,rc.country_codes, " \
                " rc.country_targeting,rc.opt,rc.targeting_type, rc.device_targeting, " \
                "rc.language_targeting, rc.exclude_low_volume, 1 AS provider_id,ws.website_name, " \
                "replace(JSON_EXTRACT(acs.account_json,'$.client_id'),'\"','') AS account_name " \
                "FROM skynet_harvester.prv_revcontent_campaigns AS rc " \
                "LEFT JOIN websites AS ws  " \
                "ON rc.website_id = ws.website_id " \
                "LEFT JOIN prv_accounts AS acs " \
                "ON acs.account_id = rc.account_id  " \
                "WHERE rc.campaign_id = %s " \
                "LIMIT 1"
        try:
            data = self.db.query(query, campaign_id)
            return [] if data is None else data[0]
        except Exception as e:
            logging.error(msg=e)

    def get_manager_campaigns(self):
        query = "SELECT cm.website_id,cm.account_id,cm.source_id,CAST(cm.creation_date as char) as creation_date," \
                "cm.campaign_id,cm.campaign_name,cm.enabled,CAST(cm.budget AS DECIMAL) as budget,cm.avg_cpc,cm.start_date," \
                "cm.end_date,CAST(cm.spend AS DECIMAL) as spend,CAST(cm.spend_yesterday AS DECIMAL) as spend_yesterday," \
                "cm.ctr,CAST(cm.revenue AS DECIMAL) as revenue,CAST(cm.revenue_yesterday AS DECIMAL) as revenue_yesterday," \
                "CAST(cm.roi AS DECIMAL(4,3)) as roi, CAST(cm.roi_yesterday AS DECIMAL(4,3)) as roi_yesterday," \
                "replace(JSON_EXTRACT(pa.account_json,'$.client_id'),'\"','') AS account_name,ws.website_name " \
                "FROM prv_campaign_manager cm " \
                "INNER JOIN prv_accounts pa " \
                "ON cm.account_id = pa.account_id " \
                "LEFT JOIN websites ws " \
                "ON cm.website_id = ws.website_id " \
                "ORDER BY spend_yesterday DESC "
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def set_campaign(self, campaign_data, campaign_id="TBD"):
        tmp_val = "TBD"
        query = "call create_revcontent_campaign(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:

            res = self.db.query(query,
                                campaign_data['website_id'],
                                campaign_data['account_id'],
                                campaign_id,
                                campaign_data['name'],
                                campaign_data['start_date'],
                                campaign_data['end_date'],
                                tmp_val,
                                tmp_val,
                                tmp_val,
                                campaign_data['bid_type'],
                                campaign_data['default_bid'],
                                tmp_val,
                                tmp_val,
                                campaign_data['budget'],
                                tmp_val,
                                tmp_val,
                                campaign_data['tracking_code'],
                                json.dumps(campaign_data['country_codes']),
                                campaign_data['country_targeting'],
                                campaign_data['optimize'],
                                json.dumps(campaign_data['device_targeting']),
                                json.dumps(campaign_data['language_targeting']),
                                campaign_data['exclude_low_volume']
                                )
            return res

        except Exception, e:
            logging.error(e.message)
            return -1, e.message

    def update_switch(self, campaign_id, enabled):
        query = "UPDATE prv_revcontent_campaigns " \
                "SET enabled = %s WHERE campaign_id = %s"
        try:
            self.db.execute(query, enabled, campaign_id)
        except Exception, e:
            logging.error(e.message)

        query = "UPDATE prv_campaign_manager " \
                "SET enabled = %s WHERE campaign_id = %s"
        try:
            self.db.execute(query, enabled, campaign_id)
            return True
        except Exception, e:
            logging.error(e.message)
            return -1, e.message

    def set_revcontent_targeting(self, campaign_id):
        keywords_list = []
        get_keywords = "SELECT * FROM revcontent_keywords"
        try:
            data = self.db.query(get_keywords)
            for keyword in data:
                tmp_tup = (
                    campaign_id, keyword['key_id'], keyword['key_name'], 'on', 0, 0.03, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0)
                keywords_list.append(tmp_tup)

        except Exception, e:
            logging.error(msg=e)
            return -1