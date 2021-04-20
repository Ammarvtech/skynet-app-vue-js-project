import logging
import json
from libs.dao import Dao


class AutomationData(Dao):
    def get_automation_data(self, sites, sources, status, name, start, end, user_id):
        query = "call sp_get_automations_management_screen('{0}','{1}','{2}','{3}','{4}','{5}','{6}');".format(sites, sources, status, name, start, end, user_id)
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_automation_name(self):
        query = "select name from optimization_action_types where is_active = 1 "
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def toggle_automation(self, site_id, name, active):
        query = "select id, name from optimization_action_types "
        try:
            mapping = self.db.query(query)
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

        auto_role_mapping = dict(
            [(str(x['name']), int(x['id'])) for x in mapping])
        role_id = auto_role_mapping[name]

        query = "INSERT INTO optimization_role_targets (role_id, user_id, target_type, target_value, is_active) " \
                "VALUES ('{0}', '1', '1', '{1}', '{2}') ON DUPLICATE KEY UPDATE is_active='{2}'".format(role_id, site_id, active)
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

