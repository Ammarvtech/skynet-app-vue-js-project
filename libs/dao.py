import hashlib
import logging

from datastore.sql import DataStore


class Dao(object):
    def __init__(self):
        self.db = DataStore()

    def hash(self, password):
        hash = hashlib.sha1()
        hash.update(password)
        return hash.hexdigest()


class Dealer(Dao):
    def __init__(self):
        super(Dealer, self).__init__()

    def get_data_by_user_id(self, user_id, date_start, date_end):
        sql = "call sp_get_dealer_data_by_user(%s,%s,%s);"
        data = self.db.query(sql, user_id, date_start, date_end)
        return data

    def updateCampaignPixelStatus(self, payload):
        payload.pop('provider_id')
        payload.pop('user_id')
        payload.pop('account_id')
        self.db.upsert_many([payload], 'dfp_pixel')


class WebsiteSettings(Dao):
    def __init__(self):
        super(WebsiteSettings, self).__init__()

    def get_website_list_by_user(self, user_id):
        sql = "call get_website_list_by_user(%s);"
        data = self.db.query(sql, user_id)
        return data

    def get_chart_data(self, site_id, device, source, start, end):
        sql = "call sp_get_chart_data(%s,%s,%s,%s,%s);"
        data = self.db.query(sql, site_id, device, source, start, end)
        return data

    def get_duplicate_templates(self, source, site_id, user_id):
        sql = "call get_dynamic_duplicate_campaign_settings_by_site_id(%s, %s, %s);"
        data = self.db.query(sql, source, site_id, user_id)
        return data

    def get_duplicate_audience_mapping(self, source):
        sql = "select audience_id, audience_display_name as display_name from " \
              "skynet_harvester.prv_audience_per_account where source = lower(%s) and is_active = 1;"
        data = self.db.query(sql, source)
        return data


class SiteConfiguration(Dao):
    def __init__(self):
        super(SiteConfiguration, self).__init__()

    def get_website_settings_by_site(self, site_id, device, key):
        sql = "call sp_get_admin_website_settings_by_site(%s, %s, %s);"
        data = self.db.query(sql, site_id, device, key)
        return data

    def get_website_settings_keys(self):
        sql = "call get_admin_website_settings_keys();"
        data = self.db.query(sql)
        return data

    def get_website_settings_history(self, site_id, device, key):
        sql = "call sp_get_admin_website_settings_history(%s, %s, %s);"
        data = self.db.query(sql, site_id, device, key)
        return data

    def update_website_settings_by_site(self, site_id, key, device, value, ab_testing_percentage, ab_testing_config,
                                        group_vals, use_group_vals, group_country_settings):
        sql = "call update_admin_website_settings_by_site(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        try:
            self.db.query(sql, site_id, key, device, value, ab_testing_percentage,
                          ab_testing_config, group_vals, use_group_vals, group_country_settings)
            return True, "OK"
        except Exception as e:
            return False, e.message

    def get_themes(self):
        sql = "call sp_get_admin_website_themes();"
        data = self.db.query(sql)
        return data

    def update_website_settings_batch(self, source, sites, fields, device, key):
        result = True
        for site in sites:
            sql = "call sp_publish_website_settings(%s, %s, %s, %s, %s);"
            try:
                self.db.query(sql, source, site, fields, device, key)
            except Exception:
                result &= False

        return result


class App(Dao):

    def __init__(self):
        super(App, self).__init__()

    def getUsersList(self, user_id=None):
        if not user_id or user_id == 1 or user_id == 103767:
            sql = "SELECT user_id, username, first_name, last_name, CONCAT_WS(' ', first_name, last_name) AS " \
                  "full_name, email_addr FROM skynet_harvester.users;"
            data = self.db.query(sql)
        else:
            sql = "SELECT user_id, username, first_name, last_name, CONCAT_WS(' ', first_name, last_name) AS " \
                  "full_name, email_addr FROM skynet_harvester.users where user_id = %s;"
            data = self.db.query(sql, user_id)
        return data

    def getUserGroup(self, user_name):
        sql = "select groups_ids from skynet_harvester.users where username='{}';".format(user_name)
        data = self.db.query(sql)
        return data

    def getUserID(self, user_name):
        # Update here to and active=1
        sql = "select user_id from skynet_harvester.users where username='{}' AND active=1;".format(user_name)
        data = self.db.query(sql)
        if data:
            return data[0]['user_id']
        else:
            return ''

    def getUserRole(self, user_id):
        sql = "select role from skynet_harvester.users where user_id='{}';".format(user_id)
        data = self.db.query(sql)
        return data[0]['role']

    def getUserWebsites(self, user_id):
        sql = "SELECT w.website_id, w.website_name,w.url ,wu.user_id " \
              "FROM skynet_harvester.websites w inner join skynet_harvester.website_users wu on w.website_id = " \
              "wu.website_id where wu.user_id =%s AND w.website_status_id = 1 ORDER BY w.website_name;"
        data = self.db.query(sql, user_id)
        return data

    def getSources(self):
        sql = "SELECT provider_name FROM skynet_harvester.prv_providers WHERE source = 1;"
        data = self.db.query(sql)
        return data

    def getAlert(self):
        sql = "SELECT alert FROM skynet_harvester.skynet_alert;"
        data = self.db.query(sql)
        return data

    def setAlert(self, alert):
        sql = "UPDATE skynet_harvester.skynet_alert SET alert = %s WHERE id = '1';"
        return self.db.query(sql, alert)

    def getCurrency(self):
        sql = "SELECT currency FROM skynet_harvester.brazil_currency order by data_date desc limit 1;"
        data = self.db.query(sql)
        return data

    def getUserSettings(self, user_id):
        sql = "CALL get_user_settings_by_user_id(%s)"
        data = self.db.query(sql, user_id)
        return data

    def get_gemini_3p_audiences(self):
        sql = "call get_gemini_3p_audiences()"
        data = self.db.query(sql)
        return data

    def validate_user_access(self, user_id, login_time):
        sql = "call validate_user_access(%s, %s);"
        data = self.db.query(sql, user_id, login_time)
        return data[0]['allow']


class Revenue(Dao):

    def __init__(self):
        super(Revenue, self).__init__()

    def get_report(self, date_start, date_end, groups):
        sql = 'call get_revenue_report(%s, %s, %s);'
        return self.db.query(sql, date_start, date_end, groups)

    def get_yesterday_report(self, date_yesterday, groups):
        sql = 'call get_yesterday_revenue_report(%s, %s);'
        return self.db.query(sql, date_yesterday, groups)

    def get_device_report(self, date_start, date_end, groups):
        sql = "SELECT rrd.*, CAST(rrd.data_date as CHAR),w.website_name " \
              "FROM skynet_harvester.revenue_report_device rrd " \
              "INNER JOIN skynet_harvester.websites w " \
              "ON rrd.site_id = w.website_id " \
              "WHERE data_date BETWEEN %s AND %s AND w.group_id in({})".format(groups)
        try:
            data = self.db.query(sql, date_start, date_end)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_new_device_report(self, date_start, date_end, device):
        sql = "SELECT rrd.*, w.website_name " \
              "FROM skynet_harvester.revenue_report_device rrd " \
              "INNER JOIN skynet_harvester.websites w " \
              "ON rrd.site_id = w.website_id " \
              "WHERE data_date BETWEEN %s AND %s AND rrd.device = %s GROUP BY rrd.site_id, rrd.device"
        try:
            if device == 'all':
                sql = sql.replace("AND rrd.device = %s", "")
                data = self.db.query(sql, date_start, date_end)
            else:
                data = self.db.query(sql, date_start, date_end, device)

            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_device_report_by_site(self, date_start, date_end, site_id):
        sql = "SELECT rrd.*, CAST(rrd.data_date as CHAR),w.website_name " \
              "FROM skynet_harvester.revenue_report_device rrd " \
              "INNER JOIN skynet_harvester.websites w " \
              "ON rrd.site_id = w.website_id " \
              "WHERE data_date BETWEEN %s AND %s " \
              "AND site_id = %s"
        try:
            data = self.db.query(sql, date_start, date_end, site_id)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def setCustomAmount(self, site_id, key, value, data_date):
        sql = "UPDATE skynet_harvester.revenue_report SET {}=%s WHERE site_id=%s AND data_date=%s".format(key)
        return self.db.execute(sql, value, int(site_id), data_date)

    def get_revenue_report_by_source(self, date_start, date_end, source, device):
        try:
            sql = "call sp_get_new_revenue_report_by_source(%s,%s,%s,%s)"
            data = self.db.query(sql, device, source, date_start, date_end)

            return data
        except Exception as e:
            logging.exception(e.message)
            return []

    def get_revenue_report_by_device(self, date_start, date_end, source, device):
        try:
            sql = "call sp_get_new_revenue_report_by_device(%s,%s,%s,%s)"
            data = self.db.query(sql, device, source, date_start, date_end)

            return data
        except Exception as e:
            logging.exception(e.message)
            return []

    def get_revenue_report_by_site(self, date_start, date_end, source, device):
        try:
            sql = "call sp_get_new_revenue_report_by_site(%s,%s,%s,%s)"
            data = self.db.query(sql, device, source, date_start, date_end)

            return data
        except Exception as e:
            logging.exception(e.message)
            return []


class Dashboard(Dao):
    def __init__(self):
        super(Dashboard, self).__init__()

    def get_bidder_data(self, cols, args):

        stmt = ''
        fields = ['start_date', 'end_date', 'website_name', 'device', 'publisher', 'placement', 'source']

        for field in sorted(fields, reverse=True):
            if field not in cols:
                fields.remove(field)

        if fields[0] == 'start_date':
            fields[0] = 'SUBSTRING(CAST(data_date AS char),1,10) AS date'
            del fields[1]
            selected = ", ".join(fields)
            grouped = "data_date, " + ", ".join(fields[1:])
        else:
            selected = grouped = ", ".join(fields)

        # structs SELECT filters by key value
        for key in args.keys():
            if args[key] is None or key == 'website_name' and args[key] == '0' or key == 'end_date' or args[key] == 'All' or key == "date_switch":
                continue
            if key == 'start_date':
                stmt += ' AND data_date BETWEEN "' + args[key] + '" AND "' + args['end_date'] + '" '
            elif key == 'website_name':
                stmt += ' AND website_id = ' + args[key]
            else:
                stmt += ' AND ' + key + '= "' + args[key] + '" '

        if len(stmt) > 1:
            stmt = ' WHERE ' + stmt[5:]
        if grouped.endswith(', '):
            grouped = grouped[:-2]
        if args["date_switch"] == "false":
            grouped = grouped.replace("data_date,", "")
        sql = (
                'SELECT ' + selected + ',sum(bid) AS revenue, sum(impressions) AS impressions '
                                       'FROM header_bidder_data hb '
                                       'INNER JOIN websites '
                                       'ON websites.website_id = hb.site_id '
                + stmt + ' GROUP BY ' + grouped
        )

        try:
            data = self.db.query(sql)
            for item in data:
                item["revenue"] = round(item["revenue"], 2)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_advertisers(self):
        sql = "select distinct publisher from skynet_harvester.header_bidder_data ORDER BY publisher;"
        try:
            advertisers = self.db.query(sql)
            return advertisers
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_colors(self, source, device, page_type):
        try:
            sql = "call sp_get_colors(%s,%s, %s)"
            data = self.db.query(sql, source, device, page_type)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_last_update(self, site_id):
        try:
            if site_id == 'all':
                sql = "SELECT l.site_id, l.last_update, w.acronym, w.website_name FROM " \
                      "skynet_harvester.app_last_update l LEFT JOIN skynet_harvester.websites w " \
                      "ON w.website_id = l.site_id;"
                data = self.db.query(sql)
            else:
                sql = "SELECT site_id,last_update FROM skynet_harvester.app_last_update WHERE site_id = %s;"
                data = self.db.query(sql, site_id)

            return data
        except:
            return []


class WebsiteStatistics(Dao):

    def get_rt_chart_data(self, website_id, device, source, start, end, user_id):
        sql = "call sp_get_campaigns_rt_hourly_data(%s,%s,%s,%s,%s,%s)"
        data = self.db.query(sql, website_id, device, source, start, end, user_id)
        return data

    def get_website_campaigns_dfp_data(self, website_id, device, source, start, end, user_id, restrict):
        try:
            sql = "call sp_get_campaigns_daily_data(%s,%s,%s,%s,%s,%s,%s)"
            data = self.db.query(sql, website_id, device, source, start, end, user_id, restrict)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_website_campaigns_rt_data(self, website_id, device, source, start, end, user_id, restrict):
        try:
            sql = "call sp_get_campaigns_rt_data(%s,%s,%s,%s,%s,%s,%s)"
            data = self.db.query(sql, website_id, device, source, start, end, user_id, restrict)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_website_campaigns_dfp_data_valid(self, website_id, device, source, start, end, user_id):
        try:
            sql = "call sp_get_campaigns_daily_data(%s,%s,%s,%s,%s,%s,%s)"
            data = self.db.query(sql, website_id, device, source, start, end, user_id, 0)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_website_campaigns_action_log(self, website_id, source, start, end, user_id):
        try:
            sql = "call sp_get_campaigns_action_logs(%s,%s,%s,%s,%s)"
            data = self.db.query(sql, website_id, source, start, end, user_id)
            return data
        except Exception as e:
            logger = logging.getLogger('sp_action_log')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_website_campaigns_rt_data_valid(self, website_id, device, source, start, end, user_id):
        try:
            sql = "call sp_get_campaigns_rt_data(%s,%s,%s,%s,%s,%s,%s)"
            data = self.db.query(sql, website_id, device, source, start, end, user_id, 0)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_country_data(self, campaign_id, site_id, start, end):

        try:
            sql = "call sp_get_country_data(%s,%s,%s,%s);"
            data = self.db.query(sql, campaign_id, site_id, start, end)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_ipageviews_data(self, campaign_id, site_id, start, end):

        try:
            sql = "SELECT campaign_id, site_id, data_date, page, exit_rate, page_title," \
                  "CONCAT(round(CAST(avg_time as DECIMAL)/60), '.', MOD(CAST(avg_time as DECIMAL),60)) AS avg_time, " \
                  "sum(pageviews) AS 'pageviews' " \
                  "FROM skynet_harvester.google_analytics_pageviews_data WHERE " \
                  "campaign_id = '{0}' AND site_id = '{1}' AND data_date BETWEEN '{2}' AND '{3}' GROUP BY " \
                  "page,page_title ORDER BY pageviews desc".format(campaign_id, site_id, start, end)

            data = self.db.query(sql)
            return data

        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_ad_content_data(self, campaign_id, site_id, start, end, compare, source):

        try:
            sql = "call sp_get_ad_content_data(%s,%s,%s,%s,%s,%s);"
            data = self.db.query(sql, campaign_id, site_id, start, end, compare, source)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_device_data(self, campaign_id, site_id, start, end):

        try:
            sql = "call sp_get_device_data(%s,%s,%s,%s)"
            data = self.db.query(sql, campaign_id, site_id, start, end)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_hours_data(self, campaign_id, site_id, start, end, compare):

        try:
            sql = "call sp_get_hours_data(%s,%s,%s,%s,%s);"
            data = self.db.query(sql, campaign_id, site_id, start, end, compare)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_taboola_blocked(self, campaign_id):

        try:
            sql = "SELECT JSON_EXTRACT(publisher_targeting,'$.value') AS publisher_targeting FROM " \
                  "skynet_harvester.prv_taboola_campaigns " \
                  "WHERE JSON_EXTRACT(publisher_targeting,'$.value') not like '[]' " \
                  "AND campaign_id = %s;"
            data = self.db.query(sql, campaign_id)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_taboola_bids(self, campaign_id, website_id):

        try:
            sql = "SELECT JSON_EXTRACT(publisher_bid_modifier,'$.values') AS " \
                  "bid_modifier FROM skynet_harvester.prv_taboola_campaigns where " \
                  "JSON_EXTRACT(publisher_bid_modifier,'$.values') not like '[]' " \
                  "AND campaign_id = %s AND website_id = %s;"
            data = self.db.query(sql, campaign_id, website_id)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_revcontent_blocked_target(self, campaign_id):

        try:
            sql = "SELECT tag_name, enabled, tag_id FROM skynet_harvester.prv_revcontent_targeting " \
                  "WHERE campaign_id = %s;"
            data = self.db.query(sql, campaign_id)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_revcontent_blocked_widget(self, campaign_id):

        try:
            sql = "SELECT typ, widget_ids FROM skynet_harvester.prv_revcontent_widget_optimizer WHERE campaign_id = %s;"
            data = self.db.query(sql, campaign_id)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_mediums(self, campaign_id, site_id, device, source, start, end):

        try:
            sql = "SELECT fd.medium, fd.campaign_id, fd.source, fd.device, fd.site_id, fd.data_date, " \
                  "fd.bid, fd.rule_mark, fd.status, lc.alert, " \
                  "sum(fd.clicks) AS 'clicks', " \
                  "sum(fd.sessions) AS 'sessions', " \
                  "sum(fd.creative_ctr) AS 'ctr', " \
                  "IFNULL(sum(clicks * user_value) / IFNULL(sum(clicks),0),0) AS 'user_value', " \
                  "IFNULL(sum(clicks * hb_user_value) / IFNULL(sum(clicks),0),0) AS 'hb_user_value', " \
                  "IFNULL(sum(clicks * pages_session) / IFNULL(sum(clicks),0),0) AS 'pages_session', " \
                  "IFNULL(sum(clicks * roi) / IFNULL(sum(clicks),0),0) AS 'roi_final',  " \
                  "IFNULL(sum(clicks * final_uv) / IFNULL(sum(clicks),0),0) AS 'final_uv', " \
                  "IFNULL(sum(clicks * taboola_uv) / IFNULL(sum(clicks),0),0) AS 'taboola_uv', " \
                  "IFNULL(sum(clicks * revcontent_uv) / IFNULL(sum(clicks),0),0) AS 'revcontent_uv', " \
                  "IFNULL(sum(clicks * provider_uv) / IFNULL(sum(clicks),0),0) AS 'provider_uv', " \
                  "sum(revenue) AS 'revenue', " \
                  "sum(provider_revenue) AS 'provider_revenue', " \
                  "sum(calculated_dfp_revenue) AS 'calculated_dfp_revenue', " \
                  "sum(cost) AS 'cost', " \
                  "(sum(revenue)- sum(cost)) AS 'profit', " \
                  "max(block) AS 'block', " \
                  "TRUE AS 'bid_currency' " \
                  "FROM skynet_harvester.app_medium_final_data_dfp fd " \
                  "LEFT JOIN skynet_harvester.app_losing_medium_indication lc " \
                  "ON fd.medium = lc.medium AND fd.campaign_id = lc.campaign_id AND fd.site_id = lc.site_id AND " \
                  "fd.data_date = lc.data_date WHERE " \
                  "fd.campaign_id = %s AND fd.site_id = %s AND fd.device = %s AND fd.clicks > 0 " \
                  "AND fd.source = %s AND fd.data_date BETWEEN %s AND %s GROUP BY fd.medium;"

            data = self.db.query(sql, campaign_id, site_id, device, source, start, end)
            return data

        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_adjust_mediums(self, campaign_id, site_id, device, source, start, end):

        try:
            sql = "SELECT medium, campaign_id, source, device, site_id, data_date, final_uv, bid " \
                  "FROM skynet_harvester.app_medium_final_data_dfp WHERE " \
                  "campaign_id = %s AND site_id = %s AND device = %s AND clicks > 50 AND block !='1'" \
                  "AND source = %s AND data_date BETWEEN %s AND %s GROUP BY medium;"

            data = self.db.query(sql, campaign_id, site_id, device, source, start, end)
            return data

        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_lost_mediums(self, campaign_id, site_id, device, source, start, end):

        try:
            sql = "SELECT a1.medium, a1.campaign_id, a1.source, a1.device, a1.site_id, a1.bid, a1.rule_mark, " \
                  "sum(a1.sessions) AS 'sessions', " \
                  "IFNULL(sum(a1.sessions * a1.user_value) / IFNULL(sum(a1.sessions),0),0) AS 'user_value', " \
                  "IFNULL(sum(a1.sessions * a1.hb_user_value) / IFNULL(sum(a1.sessions),0),0) AS 'hb_user_value', " \
                  "IFNULL(sum(a1.sessions * a1.bounce_rate) / IFNULL(sum(a1.sessions),0),0) AS 'bounce_rate', " \
                  "IFNULL(sum(a1.sessions * a1.pages_session) / IFNULL(sum(a1.sessions),0),0) AS 'pages_session', " \
                  "IFNULL(sum(a1.sessions * a1.adsense_cpc) / IFNULL(sum(a1.sessions),0),0) AS 'adsense_cpc', " \
                  "IFNULL(sum(a1.sessions * a1.roi) / IFNULL(sum(a1.sessions),0),0) AS 'roi', " \
                  "IFNULL(sum(a1.sessions * a1.final_uv) / IFNULL(sum(a1.sessions),0),0) AS 'final_uv', " \
                  "IFNULL(sum(a1.sessions * a1.taboola_uv) / IFNULL(sum(a1.sessions),0),0) AS 'taboola_uv', " \
                  "IFNULL(sum(a1.sessions * a1.revcontent_uv) / IFNULL(sum(a1.sessions),0),0) AS 'revcontent_uv', " \
                  "IFNULL(sum(a1.sessions * a1.provider_uv) / IFNULL(sum(a1.sessions),0),0) AS 'provider_uv', " \
                  "IFNULL(sum(a1.sessions * a1.publisher_ctr) / IFNULL(sum(a1.sessions),0),0) AS 'publisher_ctr', " \
                  "sum(a1.publisher_revenue) AS 'publisher_revenue', " \
                  "sum(a1.taboola_revenue) AS 'taboola_revenue', " \
                  "sum(a1.revcontent_revenue) AS 'revcontent_revenue', " \
                  "sum(a1.publisher_revenue) - sum(a1.cost) as 'lost', " \
                  "sum(a1.cost) AS 'cost', " \
                  "max(a2.data_date) as 'data_date' ," \
                  "(a2.ablock) as 'ablock', " \
                  "max(a2.block) as 'block', " \
                  "(a2.status) as 'status' " \
                  "FROM skynet_harvester.app_medium_final_data a1 " \
                  "JOIN skynet_harvester.app_medium_final_data a2 " \
                  "ON (a1.campaign_id = a2.campaign_id) AND " \
                  "(a1.site_id = a2.site_id) AND " \
                  "(a1.device = a2.device) AND " \
                  "(a1.medium = a2.medium) " \
                  "WHERE a1.campaign_id = %s AND a1.site_id = %s AND a1.device = %s AND " \
                  "a1.source = %s AND a1.data_date " \
                  "BETWEEN %s and %s and a2.ablock = '1' " \
                  "GROUP BY a1.medium "

            data = self.db.query(sql, campaign_id, site_id, device, source, start, end)
            return data

        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_keywords(self, campaign_id, site_id, device, source, start, end):

        try:
            sql = "SELECT keyword, tag_id, campaign_id, source, device, site_id, data_date, bid, rule_mark, " \
                  "enabled, status, " \
                  "sum(sessions) AS 'sessions', " \
                  "IFNULL(sum(sessions * user_value) / IFNULL(sum(sessions),0),0) AS 'user_value', " \
                  "IFNULL(sum(sessions * hb_user_value) / IFNULL(sum(sessions),0),0) AS 'hb_user_value', " \
                  "IFNULL(sum(sessions * bounce_rate) / IFNULL(sum(sessions),0),0) AS 'bounce_rate', " \
                  "IFNULL(sum(sessions * pages_session) / IFNULL(sum(sessions),0),0) AS 'pages_session', " \
                  "IFNULL(sum(sessions * adsense_cpc) / IFNULL(sum(sessions),0),0) AS 'adsense_cpc', " \
                  "IFNULL(sum(sessions * roi) / IFNULL(sum(sessions),0),0) AS 'roi', " \
                  "IFNULL(sum(sessions * final_uv) / IFNULL(sum(sessions),0),0) AS 'final_uv', " \
                  "IFNULL(sum(sessions * taboola_uv) / IFNULL(sum(sessions),0),0) AS 'taboola_uv', " \
                  "IFNULL(sum(sessions * revcontent_uv) / IFNULL(sum(sessions),0),0) AS 'revcontent_uv', " \
                  "IFNULL(sum(sessions * provider_uv) / IFNULL(sum(sessions),0),0) AS 'provider_uv', " \
                  "IFNULL(sum(sessions * publisher_ctr) / IFNULL(sum(sessions),0),0) AS 'publisher_ctr', " \
                  "IFNULL(sum(sessions * ad_sense_uv) / IFNULL(sum(sessions),0),0) AS 'ad_sense_uv', " \
                  "IFNULL(sum(sessions * delta_uv) / IFNULL(sum(sessions),0),0) AS 'delta_uv', " \
                  "sum(publisher_revenue) AS 'publisher_revenue', " \
                  "sum(taboola_revenue) AS 'taboola_revenue', " \
                  "sum(revcontent_revenue) AS 'revcontent_revenue', " \
                  "sum(cost) AS 'cost' " \
                  "FROM skynet_harvester.app_keyword_final_data WHERE " \
                  "campaign_id = %s AND site_id = %s AND device = %s " \
                  "AND source = %s AND data_date BETWEEN %s AND %s GROUP BY keyword"

            data = self.db.query(sql, campaign_id, site_id, device, source, start, end)
            return data

        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def update_medium_status(self, status, campaign_id, medium, device, data_date):
        try:
            sql = "UPDATE skynet_harvester.app_medium_final_data_dfp SET status= %s " \
                  "WHERE campaign_id = %s AND medium = %s AND device = %s AND data_date = %s"
            self.db.execute(sql, status, campaign_id, medium, device, data_date)
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)

    def update_keyword_status(self, status, campaign_id, keyword, data_date, device, source=None):
        try:
            sql = "UPDATE skynet_harvester.app_keyword_final_data SET status= %s " \
                  "WHERE campaign_id = %s AND keyword = %s AND data_date = %s AND devive = %s"

            if source == 'revcontent':
                sql = sql.replace("keyword ", "tag_id ")

            self.db.execute(sql, status, campaign_id, keyword, data_date, device)
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)

    def get_taboola_campaigns_bids(self, website_id):
        if website_id in ["all"]:
            sql = "SELECT campaign_id,website_id as site_id,cpc FROM skynet_harvester.prv_taboola_campaigns;"
            data = self.db.query(sql)
        else:
            sql = "SELECT campaign_id,website_id as site_id,cpc FROM skynet_harvester.prv_taboola_campaigns WHERE " \
                  "website_id = %s;"
            data = self.db.query(sql, website_id)
        try:
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_campaign_chart_data(self, site_id, campaign_id, device, source, start, end):
        try:
            sql = "SELECT data_date, " \
                  "IFNULL(SUM(sessions * pages_session) / IFNULL(sum(sessions),0),0) as 'pages_sessions', " \
                  "IFNULL(SUM(sessions * final_uv) / IFNULL(sum(sessions),0),0) as 'uv', " \
                  "IFNULL(SUM(sessions * avg_cpc) / IFNULL(sum(sessions),0),0) as 'avg_bid', " \
                  "IFNULL(SUM(sessions * roi) / IFNULL(sum(sessions),0),0) as 'roi', " \
                  "SUM(cost) as 'cost', " \
                  "SUM(revenue) as 'revenue', " \
                  "SUM(sessions) as 'sessions' " \
                  "FROM skynet_harvester.app_campaigns_final_data " \
                  "WHERE device = %s AND source = %s AND site_id = %s AND campaign_id = %s AND " \
                  "data_date BETWEEN %s AND %s GROUP BY data_date ORDER BY data_date;"

            return self.db.query(sql, device, source, site_id, campaign_id, start, end)
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_sessions_by_device(self, campaign_id, site_id, source, start, end):
        try:
            sql = "SELECT device, sessions FROM skynet_harvester.campaigns_final_data_dfp WHERE " \
                  "data_date BETWEEN %s AND %s AND site_id = %s AND source = %s AND campaign_id = %s GROUP BY device;"
            data = self.db.query(sql, start, end, site_id, source, campaign_id)
            return data
        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []

    def get_inventory_by_site(self, site_id):
        try:
            if site_id != 'all':
                sql = "SELECT campaign_id,url FROM skynet_harvester.prv_taboola_inventory WHERE " \
                      "website_id = %s GROUP BY campaign_id;"
                data = self.db.query(sql, site_id)
            else:
                sql = "SELECT campaign_id,url FROM skynet_harvester.prv_taboola_inventory GROUP BY campaign_id;"
                data = self.db.query(sql)

            return data

        except Exception as e:
            logger = logging.getLogger('dashboard')
            logger.info(e)
            logging.exception(e.message)
            return []


class Tasks(Dao):
    def insert_task(self, description, user_id, site_id, priority, campaign_id, subject, due_date, created_by, action,
                    task_id):
        status_id = 1
        sql = ""
        new = True
        if action == "new":
            sql = "INSERT INTO skynet_harvester.task_management SET " \
                  "description = %s, " \
                  "user_id = %s, " \
                  "site_id = %s, " \
                  "priority = %s, " \
                  "campaign_id = %s, " \
                  "subject = %s, " \
                  "due_date = %s, " \
                  "status_id = %s, " \
                  "created_by = %s, " \
                  "created_on = CURDATE();"

        elif action == "update" and task_id != "null" and int(task_id) > 0:
            new = False
            sql = "UPDATE skynet_harvester.task_management SET " \
                  "description = %s, " \
                  "user_id = %s, " \
                  "site_id = %s, " \
                  "priority = %s, " \
                  "campaign_id = %s, " \
                  "subject = %s, " \
                  "due_date = %s, " \
                  "created_by = %s " \
                  "WHERE task_id = %s;"
        try:
            if new:
                self.db.query(sql, description, user_id, site_id, priority, campaign_id, subject, due_date, status_id,
                              created_by)
            elif not new:
                self.db.query(sql, description, user_id, site_id, priority, campaign_id, subject, due_date,
                              created_by, task_id)
            return "true"
        except Exception as e:
            logging.error("Failed to Add Task")
            logging.exception(e.message)
            return -1, e.message

    def get_tasks(self, user_id):

        sql = "call sp_get_tasks_by_user(%s)"
        try:
            data = self.db.query(sql, user_id)
            return data
        except Exception as e:
            logging.error("Failed to get Tasks")
            logging.exception(e.message)
            return []

    def change_task(self, action, task_id, status_id):
        sql = ""
        if action == "close":
            sql = "UPDATE skynet_harvester.task_management SET `status_id`='{0}' WHERE task_id = %s;".format(status_id)

        elif action == "delete":
            sql = "DELETE FROM skynet_harvester.task_management WHERE task_id = %s;"
        try:
            self.db.query(sql, task_id)
            return "true"
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message


class Campaigns(Dao):
    def get_countries(self):
        query = "SELECT * FROM skynet_harvester.prv_revcontent_countries;"
        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_keywords(self):
        query = "SELECT * FROM skynet_harvester.revcontent_keywords;"

        try:
            data = self.db.query(query)
            return data
        except Exception as e:
            logging.exception(e.message)
            return -1, e.message

    def get_campaign_account(self, source, campaign_id, site_id):

        sql = "call sp_get_prv_campaign_account(%s,%s,%s);"
        return self.db.query(sql, source, campaign_id, site_id)

    def get_bidders(self, user_id, source, site_id, campaign_id='all'):
        query = "call sp_get_campaigns_bidders(%s, %s, %s, %s)"
        try:
            data = self.db.query(query, site_id, source, user_id, campaign_id)
            return data
        except Exception as e:
            logging.exception(e.message)
            return {}

    def get_automation_ruls(self):
        try:
            sql = "SELECT target_value AS campaign_id,max(is_active) AS automation_active FROM " \
                  "skynet_harvester.optimization_role_targets WHERE target_type = '2' GROUP BY target_value;"
            data = self.db.query(sql)
            return data
        except Exception as e:
            logging.exception(e.message)
            return {}

    def update_automation_status(self, data):
        try:
            self.db.upsert_many(data, 'optimization_role_targets')

        except Exception as e:
            logging.exception(e.message)

    def save_bidders(self, data):
        try:
            self.db.upsert_many(data, 'app_campaigns_bidder')
        except Exception as e:
            logging.exception(e.message)
            return {}

    def delete_bidder(self, bidder_id):
        query = "DELETE FROM skynet_harvester.app_campaigns_bidder WHERE id = %s;"
        try:
            cursor = self.db.cursor
            return cursor.execute(query, bidder_id)
        except Exception as e:
            logging.exception(e.message)
            return {}

    def get_gemini_campaign_site(self, campaign_id):
        sql = "SELECT site_id FROM skynet_harvester.prv_gemini_campaigns WHERE campaign_id = %s;"
        return self.db.query(sql, campaign_id)
