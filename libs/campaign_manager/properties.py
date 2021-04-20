import logging
from libs.dao import Dao
import json


class CampaignProperties(Dao):
    def get_campaign_by_id(self, campaign_id):
        data_dict = {}

        query = "SELECT rc.id, rc.website_id, rc.account_id, rc.campaign_id, " \
                "rc.campaign_name, rc.start_date, rc.end_date, rc.targeting_type, " \
                "rc.enabled, rc.status, rc.bid_type, rc.default_bid, rc.min_bid, " \
                "rc.max_bid, rc.budget, rc.cost, ctr,rc.utm_codes,rc.country_codes, " \
                " rc.country_targeting,rc.opt,rc.targeting_type, rc.device_targeting, " \
                "rc.language_targeting, rc.exclude_low_volume, 'revcontent' AS provider,ws.website_name, " \
                "replace(JSON_EXTRACT(acs.account_json,'$.client_id'),'\"','') AS account_name " \
                "FROM skynet_harvester.prv_revcontent_campaigns AS rc " \
                "inner join websites AS ws  " \
                "ON rc.website_id = ws.website_id " \
                "inner join prv_accounts as acs " \
                "ON acs.account_id = rc.account_id  " \
                "WHERE rc.campaign_id = %s " \
                "LIMIT 1"
        try:
            data = self.db.query(query, campaign_id)[0]
            keys = data.keys()
            values = data.values()
            for idx in range(0, len(data)):
                data_dict[keys[idx]] = values[idx]
            return data_dict
        except Exception as e:
            logging.error(msg=e)

    def get_countries(self):
        query = "SELECT * FROM prv_revcontent_countries"
        try:
            data = self.db.query(query)
            return data
        except Exception, e:
            logging.exception(e.message)
            return -1, e.message

    def get_websites_list(self, user_id):
        sql = "SELECT w.website_id, w.website_name, w.acronym " \
              "FROM websites w " \
              "JOIN website_users u " \
              "ON w.website_id = u.website_id " \
              "WHERE user_id = %s " \
              "ORDER BY w.website_name ASC"
        data = self.db.query(sql, user_id)
        return data

    def get_accounts(self):
        query = "SELECT account_id, replace(JSON_EXTRACT(account_json,'$.client_id'),'\"','') AS account_name " \
                "FROM prv_accounts " \
                "WHERE provider_id = 1 " \
                "GROUP BY account_name " \
                "ORDER BY account_name ASC"
        try:
            data = self.db.query(query)
            return data
        except Exception, e:
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

    def set_campaign(self, campaign_data, campaign_id="TBD"):
        tmp_val = "TBD"
        query = "call create_revcontent_campaign(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            res = self.db.executeSP(query,
                                    campaign_data['website_id'],
                                    campaign_data['account_id'],
                                    campaign_id,
                                    campaign_data['name'],
                                    campaign_data['start_date'],
                                    campaign_data['end_date'],
                                    tmp_val,
                                    "active",
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

    def set_revcontent_targeting(self, campaign_id, bid):
        try:
            query = "INSERT INTO prv_revcontent_targeting(" \
                    "campaign_id, " \
                    "tag_id, " \
                    "tag_name," \
                    "enabled," \
                    "bid_type," \
                    "bid," \
                    "max_bid," \
                    "min_bid," \
                    "avg_cpc," \
                    "avg_position," \
                    "impressions," \
                    "clicks," \
                    "clicks_week," \
                    "conversions," \
                    "ctr," \
                    "cost," \
                    "rtrn," \
                    "profit)" \
                    "SELECT  %s,key_id,key_name,'enabled',0,%s,0,0,0,0,0,0,0,0,0,0,0,0 " \
                    "FROM revcontent_keywords"
            self.db.execute(query, campaign_id, bid)
        except Exception as e:
            logging.error(msg=e)
            return -1

        return True

    def update_campaign_properties(self, campaign, omg_id, cid):
        query = "UPDATE prv_revcontent_campaigns SET " \
                "campaign_name = %s, " \
                "default_bid = %s, " \
                "budget = %s, " \
                "end_date = %s, " \
                "country_codes = %s, " \
                "country_targeting = %s, " \
                "device_targeting = %s, " \
                "language_targeting = %s, " \
                "exclude_low_volume = %s " \
                "WHERE id = %s " \
                "AND campaign_id = %s"

        try:
            self.db.execute(query,
                            campaign['name'],
                            campaign['default_bid'],
                            campaign['budget'],
                            campaign['end_date'],
                            json.dumps(campaign['country_codes']),
                            campaign['country_targeting'],
                            json.dumps(campaign['device_targeting']),
                            json.dumps(campaign['language_targeting']),
                            campaign['exclude_low_volume'],
                            omg_id,
                            cid
                            )
        except Exception, e:
            logging.error(msg=e)
            return -1
        return True

    def get_provider_by_name(self, provider_name):
        query = "SELECT provider_id " \
                "FROM prv_providers " \
                "WHERE provider_name = LOWER(%s)"

        try:
            res = self.db.query(query, provider_name.lower())
            return res[0]['provider_id']
        except Exception as e:
            logging.error(msg=e)
            return False

    def new_global_bid(self, campaign_id, new_bid):
        current_bid = ''

        query = "SELECT default_bid " \
                "FROM prv_revcontent_campaigns " \
                "WHERE campaign_id = %s"
        try:
            current_bid = self.db.query(query, campaign_id)[0]['default_bid']
        except Exception as e:
            logging.error(msg=e)

        if str(current_bid) != str(new_bid):
            query = "UPDATE prv_revcontent_targeting SET bid = %s " \
                    "WHERE campaign_id = %s"
            try:
                res = self.db.query(query, new_bid, campaign_id)
                return res
            except Exception as e:
                logging.error(msg=e)
        else:
            return False
