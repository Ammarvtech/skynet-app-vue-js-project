import logging
from libs.dao import Dao
import json


class ProfilerData(Dao):
    def get_sets(self):
        try:
            query = "SELECT ui.id,ui.profile_id, ui.country,ui.device,ui.widget_type," \
                    "ui.widget_list_id,ui.budget,ui.bid,ui.`desc`,wl.name as list_name " \
                    "FROM prv_rev_user_profile_items ui " \
                    "INNER JOIN prv_user_profile up " \
                    "ON ui.profile_id = up.id " \
                    "LEFT JOIN prv_rev_user_widget_list wl " \
                    "ON wl.id = ui.widget_list_id "
            res = self.db.query(query)
            return res
        except Exception as e:
            logging.error(msg=e)
            return -1

    def get_profiles(self):
        try:
            query = "SELECT up.user_id,CAST(up.creation_date AS char) AS creation_date, " \
                    "up.name, up.id AS profile_id,u.username " \
                    "FROM prv_user_profile up " \
                    "INNER JOIN users u " \
                    "ON up.user_id = u.user_id "
            res = self.db.query(query)
            return res
        except Exception as e:
            logging.error(msg=e)
            return -1

    def get_w_lists(self):
        try:
            query = "SELECT * FROM  prv_rev_user_widget_list"
            res = self.db.query(query)
            return res
        except Exception as e:
            logging.error(msg=e)
            return -1

    def set_profile(self, data, user_id):
        try:
            query = "INSERT INTO prv_user_profile(`user_id`,`name`) " \
                    "VALUES(%s,%s)"
            resp = self.db.execute(query, user_id, data["name"])
            query = "SELECT last_insert_id() as last_id"
            last_id = self.db.query(query)[0]["last_id"]
            return last_id
        except Exception as e:
            logging.error(msg=e)
            return -1

    def set_item(self, data):
        if data["id"]:
            query = "UPDATE prv_rev_user_profile_items SET " \
                    "country = %s," \
                    "device = %s," \
                    "widget_type = %s," \
                    "widget_list_id = %s," \
                    "budget = %s," \
                    "bid = %s," \
                    "`desc` = %s " \
                    "WHERE id = %s"
            self.db.execute(query,
                            json.dumps(data["country"]),
                            json.dumps(data["device"]),
                            data["widget_type"],
                            data["widget_list_id"],
                            data["budget"],
                            data["bid"],
                            data["desc"],
                            data["id"])
        else:
            query = "INSERT INTO prv_rev_user_profile_items(" \
                    "profile_id, " \
                    "country, " \
                    "device, " \
                    "widget_type, " \
                    "widget_list_id, " \
                    "budget, " \
                    "bid, " \
                    "`desc`) " \
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
            self.db.execute(query,
                            int(data["profile_id"]),
                            json.dumps(data["country"]),
                            json.dumps(data["device"]),
                            data["widget_type"],
                            data["widget_list_id"],
                            data["budget"],
                            data["bid"],
                            data["desc"])

        try:
            query = "SELECT last_insert_id() as last_id"
            last_id = self.db.query(query)[0]["last_id"]
            return last_id
        except Exception as e:
            logging.error(msg=e)
            return -1

    def set_list(self, name, w_list):
        try:
            query = "INSERT INTO prv_rev_user_widget_list(name, widget_list) " \
                    "VALUES(%s,%s)"
            self.db.execute(query, name, w_list)
            query = "SELECT last_insert_id() as last_id"
            last_id = self.db.query(query)[0]["last_id"]
            return last_id
        except Exception as e:
            logging.error(msg=e)
            return -1

    def update_list(self, w_list):
        try:
            query = "UPDATE prv_rev_user_widget_list " \
                    "SET name = %s," \
                    "widget_list = %s " \
                    "WHERE id = %s"
            res = self.db.execute(query, w_list["name"], w_list["list"], w_list["list_id"])
            return res
        except Exception as e:
            logging.error(msg=e)
            return -1

    def delete_set(self, set_id):
        query = "DELETE FROM prv_rev_user_profile_items WHERE id = %s"
        try:
            self.db.execute(query, set_id)
            return "true"
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def delete_list(self, list_id):
        query = "DELETE FROM prv_rev_user_widget_list WHERE id = %s"
        try:
            self.db.execute(query, list_id)
            return "true"
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def delete_profile(self, profile_id):
        try:
            query = "DELETE FROM prv_user_profile WHERE id = %s"
            self.db.execute(query, profile_id)
            query = "DELETE FROM  prv_rev_user_profile_items WHERE profile_id = %s"
            self.db.execute(query, profile_id)
            return "true"
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message
