import logging
import json
from libs.dao import Dao


class OptimizationData(Dao):
    def get_rules(self):
        query = "SELECT cr.id,cr.campaign_id,cr.site_id,cr.source,cr.device,cr.rules,cr.active,fd.name," \
                "cr.status,CAST(modification_date as CHAR) AS date " \
                "FROM app_campaigns_rules cr " \
                "LEFT JOIN app_campaigns_final_data fd " \
                "ON cr.campaign_id = fd.campaign_id " \
                "GROUP BY cr.campaign_id,cr.site_id"
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_campaigns(self):
        query = "SELECT site_id,source,campaign_id " \
                "FROM app_campaigns_final_data " \
                "WHERE source = 'taboola' " \
                "GROUP BY campaign_id "
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_single_campaign(self, cid):
        query = "SELECT site_id,source,device  " \
                "FROM app_campaigns_final_data " \
                "WHERE campaign_id = %s " \
                "GROUP BY campaign_id "
        try:
            data = self.db.query(query, cid)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_campaign_rules(self, cid):
        query = "SELECT rules  " \
                "FROM app_campaigns_rules " \
                "WHERE id = %s "
        try:
            data = self.db.query(query, cid)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def set_rules(self, data, campaign_data, user_id):
        website_id = campaign_data[0]["site_id"] if len(campaign_data) else data["website_id"] if data["campaign_id"] in ["All"] else "NA";
        query = "INSERT INTO app_campaigns_rules (" \
                "`campaign_id`, " \
                "`site_id`, " \
                "`source`, " \
                "`device`, " \
                "`rules`, " \
                "`active`, " \
                "`user_id`) " \
                "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.db.execute(query,
                            data["campaign_id"],
                            website_id,
                            campaign_data[0]["source"] if len(campaign_data) else "NA",
                            campaign_data[0]["device"] if len(campaign_data) else "NA",
                            json.dumps(data["rules"]),
                            1,
                            user_id
                            )
            resp = self.get_last_campaign()
            return resp
        except Exception, e:
            logging.error(msg=e)
            return -1

    def update_rule(self, data):
        query = "UPDATE app_campaigns_rules SET " \
                "rules = %s " \
                "WHERE id = %s"
        try:
            self.db.execute(query,
                            json.dumps(data["rules"]),
                            data["record_id"]
                            )
            return 1
        except Exception, e:
            logging.error(msg=e)
            return -1

    def switch_multiple(self, ids, status):
        for record_id in ids:
            query = "UPDATE app_campaigns_rules SET " \
                    "active = %s " \
                    "WHERE id = %s"
            try:
                self.db.execute(query, status, record_id)
            except Exception, e:
                logging.error(msg=e)
                return -1
        return 1

    def delete_multiple(self, ids):
        for record_id in ids:
            query = "DELETE FROM app_campaigns_rules " \
                    "WHERE id = %s"
            try:
                self.db.execute(query, record_id)
            except Exception, e:
                logging.error(msg=e)
                return -1
        return 1

    def set_opt_active(self, opt_id, status):
            query = "UPDATE app_campaigns_rules SET " \
                    "active = %s " \
                    "WHERE id = %s"
            try:
                self.db.execute(query, status, opt_id)
                return 1
            except Exception, e:
                logging.error(msg=e)
                return -1

    def get_last_campaign(self):
        try:
            query = "SELECT cr.id,cr.campaign_id,cr.source,cr.site_id,cr.active,cr.rules,fd.name " \
                    "FROM app_campaigns_rules cr " \
                    "LEFT JOIN app_campaigns_final_data fd " \
                    "ON cr.campaign_id = fd.campaign_id " \
                    "ORDER BY id DESC " \
                    "LIMIT 1"
            resp = self.db.query(query)
            return resp
        except Exception, e:
            logging.error(msg=e)
            return -1

    def activate_campaign(self, record_id):
        query = "UPDATE app_campaigns_rules " \
                "SET active = 1 " \
                "WHERE id = %s"
        try:
            resp = self.db.execute(query, record_id)
            return resp
        except Exception as e:
            logging.error(msg=e)
            return -1