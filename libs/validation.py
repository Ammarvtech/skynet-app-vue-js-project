import logging
import json
from libs.dao import Dao


class ValidationData(Dao):
    def get_data(self, yesterday, usr_id):
        query = "SELECT " \
                "ws.website_name," \
                "rv.site_id," \
                "rv.campaigns_revenue," \
                "rv.dfp_nc_revenue, " \
                "rv.taboola_rt_nc_revenue," \
                "rv.website_revenue, " \
                "rv.other, " \
                "rv.hb_dfp, " \
                "rv.ad_sense_dfp, " \
                "rv.ad_sense_diff, " \
                "rv.hb_diff, " \
                "rv.taboola_diff, " \
                "rv.outbrain_diff, " \
                "rv.income_adsense, " \
                "rv.income_h_bid, " \
                "rv.income_taboola, " \
                "rv.income_outbrain, " \
                "rv.income_adx, " \
                "rv.adx_diff, " \
                "rv.adx_revenue, " \
                "CAST(rv.data_date AS char) as data_date " \
                "FROM revenue_validation rv " \
                "INNER JOIN websites ws " \
                "ON rv.site_id = ws.website_id " \
                "WHERE data_date = %s AND site_id IN (SELECT website_id from website_users where user_id = %s)"

        try:
            data = self.db.query(query, yesterday, usr_id)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_cost_data(self, yesterday,usr_id):
        query = "SELECT w.website_name," \
                " site_lvl.site_id," \
                "CAST(COALESCE(site_lvl.s_cost,0) AS SIGNED ) AS s_cost," \
                "CAST(COALESCE(cmp_lvl.c_cost,0)AS SIGNED )AS c_cost," \
                "CAST(COALESCE(site_lvl.s_cost,0)AS SIGNED) - CAST(COALESCE(cmp_lvl.c_cost,0) AS SIGNED) AS difference " \
                "FROM (SELECT site_id,SUM(spent/rate) AS s_cost,rate FROM taboola_platform_cost AS tb " \
                "LEFT JOIN (SELECT 'BRL' AS currency,currency AS rate FROM brazil_currency WHERE data_date = '{0}' " \
                "UNION ALL SELECT 'USD',1.0) AS cur ON tb.currency=cur.currency WHERE data_date = '{0}' " \
                "GROUP BY site_id) AS site_lvl LEFT JOIN " \
                "(SELECT site_id, SUM(cost) AS c_cost FROM app_campaigns_final_data_dfp WHERE data_date = '{0}' " \
                "AND source='taboola' GROUP BY site_id ) as cmp_lvl ON site_lvl.site_id = cmp_lvl.site_id " \
                "LEFT JOIN websites AS w ON site_lvl.site_id=w.website_id HAVING site_id IN " \
                "(SELECT website_id FROM website_users WHERE user_id='{1}')".format(yesterday, usr_id)


        try:
            data = self.db.query(query, json=True)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message
