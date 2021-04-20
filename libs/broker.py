import logging
from libs.dao import Dao
from libs.campaign_manager.properties import CampaignProperties


class BrokerData(Dao):
    def get_broker_campaigns(self):
        format = '%H:%i'
        query = "SELECT DISTINCT bd.id, bd.campaign_id, bd.website_id,bd.provider_id, " \
                "bd.bid_change, ws.website_name, bd.status, " \
                "CAST(TIME_FORMAT(task_hour, %s) as char) as task_hour, pr.provider_name " \
                "FROM broker_data bd " \
                "INNER JOIN websites ws " \
                "ON bd.website_id = ws.website_id " \
                "INNER JOIN prv_providers pr " \
                "ON bd.provider_id = pr.provider_id"
        try:
            data = self.db.query(query, format)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_filter_campaigns(self, provider, website_id):
        active_status = ""
        active_column = ""
        provider_name = str(provider).lower()
        table = "prv_{0}_campaigns".format(provider_name)
        if provider_name in ["revcontent"]:
            active_column = "enabled"
            active_status = "active"
        elif provider_name in ["taboola"]:
            active_column = "status"
            active_status = "RUNNING"

        query = "SELECT campaign_id FROM {0} " \
                "WHERE website_id = {1} " \
                "AND {2} = '{3}'".format(table, website_id, active_column, active_status)
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def delete_task(self, campaign_id):
        query = "DELETE FROM broker_data WHERE campaign_id = %s"
        try:
            self.db.execute(query, campaign_id)
            return "true"
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def delete_inetrval(self, interval_id):
        query = "DELETE FROM broker_data WHERE id = %s"
        try:
            data = self.db.execute(query, interval_id)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def set_task(self, user_id, data, updated):
        provider_id = CampaignProperties().get_provider_by_name(data["provider_name"].lower())
        account_id = self.get_account_id(data["campaign_id"], data["provider_name"])

        status = "active"
        to_insert = {}

        if updated:
            to_update = [x for x in data["intervals"] if 'is_new' not in x.keys()]
            to_insert = [x for x in data["intervals"] if 'is_new' in x.keys()]

            for interval in to_update:

                if "id" not in interval.keys():
                    interval["id"] = self.get_interval_id(provider_id, account_id, data["campaign_id"], interval["time"], interval["bid_change"])
                try:
                    query = "UPDATE broker_data SET " \
                            "task_hour = %s," \
                            "bid_change = %s " \
                            "WHERE id = %s"
                    self.db.execute(query, interval["time"], interval["bid_change"], interval["id"])
                except Exception as e:
                    logging.error(msg=e)
                    return -1
        else:
            to_insert = data["intervals"]
        for interval in to_insert:
            try:
                query = "INSERT INTO broker_data(" \
                        "user_id," \
                        "campaign_id," \
                        "website_id," \
                        "account_id," \
                        "provider_id," \
                        "task_hour," \
                        "bid_change," \
                        "status)" \
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
                self.db.execute(query,
                                user_id,
                                data["campaign_id"],
                                data["website_id"],
                                account_id,
                                provider_id,
                                interval["time"],
                                interval["bid_change"],
                                status
                                )
            except Exception as e:
                logging.error(msg=e)
                return -1

        return True

    def get_account_id(self, campaign_id, provider_name):
        table = "prv_{0}_campaigns".format(str(provider_name).lower())

        query = "SELECT account_id FROM {0} " \
                "WHERE campaign_id = {1} " \
                "LIMIT 1".format(table, campaign_id)
        try:
            data = self.db.query(query)
            return data[0]["account_id"]
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_interval_id(self,provider_id, account_id, campaign_id, task_hour, bid_change):
        query = "SELECT id FROM broker_data " \
                "WHERE provider_id = %s " \
                "AND account_id = %s " \
                "AND campaign_id = %s " \
                "AND task_hour = %s " \
                "AND bid_change = %s "
        try:
            id = self.db.query(query, provider_id, account_id, campaign_id, task_hour, bid_change)
            return id[0]["id"]
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

