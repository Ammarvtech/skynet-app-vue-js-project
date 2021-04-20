from libs.dao import Dao


class RTCampaigns(Dao):
    '''
    to-do must move website_name join to harvester
    '''
    def getCampaigns(self, site, start, end):
        '''
        Get One Site or All Sites Campaigns
        :param site:
        :param start:
        :param end:
        :return:
        '''
        try:
            sql = "SELECT ws.*, cs.* FROM (SELECT site_id, creation_date, modification_date, last_date, campaign, clicks, cpc, spent, hb_uv, hb_revenue, IFNULL(p_uv,0.0) AS p_uv, IFNULL(ads_uv,0.0) AS ads_uv, hb_factor, " \
                  "IFNULL(d_uv,0.0) AS d_uv, ((p_uv*clicks)+(IFNULL(ads_uv,0.0)*clicks)+(hb_uv*clicks)+(IFNULL(d_uv,0.0)*clicks)) as final_revenue, " \
                  "(((p_uv*clicks)+(IFNULL(ads_uv,0.0)*clicks)+(hb_uv*clicks)) - spent) as profit, " \
                  "(hb_uv*hb_factor) as hb_factor_uv, " \
                  "((((p_uv*clicks)+(IFNULL(ads_uv,0.0)*clicks)+(hb_uv*clicks)) - spent) / spent) as roi " \
                  "FROM skynet_harvester.rt_taboola_slim_final WHERE last_date >= '{0}' AND last_date <= '{1}' AND site_id IN ({2}) AND hb_uv <> 0 " \
                  "ORDER BY spent DESC) AS cs " \
                  "LEFT JOIN (SELECT website_id, website_name,acronym FROM skynet_harvester.websites) as ws " \
                  "ON ws.website_id = cs.site_id " \
                  "ORDER BY cs.spent DESC".format(start, end, site)
            data = self.db.query(sql, json=True)
            return data
        except Exception as e:
            raise e

    def getCampaign(self, site, start, end, campaign):
        '''
        Get Specific Campaign all entries Unfiltered
        :param site:
        :param start:
        :param end:
        :param campaign:
        :return:
        '''
        try:
            sql = "SELECT ws.*, cs.* FROM (SELECT site_id, creation_date, modification_date, last_date, campaign, clicks, cpc, spent, hb_uv, hb_revenue, p_uv, IFNULL(ads_uv,0.0) AS ads_uv, hb_factor, " \
                  "IFNULL(d_uv,0.0) AS d_uv, ((p_uv*clicks)+(IFNULL(ads_uv,0.0)*clicks)+(hb_uv*clicks)+(IFNULL(d_uv,0.0)*clicks)) as final_revenue, " \
                  "(((p_uv*clicks)+(IFNULL(ads_uv,0.0)*clicks)+(hb_uv*clicks)+(IFNULL(d_uv,0.0)*clicks)) - spent) as profit, " \
                  "(hb_uv*hb_factor) as hb_factor_uv, " \
                  "((((p_uv*clicks)+(IFNULL(ads_uv,0.0)*clicks)+(hb_uv*clicks)+(IFNULL(d_uv,0.0)*clicks)) - spent) / spent) as roi " \
                  "FROM skynet_harvester.rt_taboola_final WHERE last_date >= '{0}' AND last_date <= '{1}' AND site_id={2} AND campaign='{3}' " \
                  "ORDER BY last_date DESC) AS cs " \
                  "LEFT JOIN (SELECT website_id, website_name,acronym FROM skynet_harvester.websites) as ws " \
                  "ON ws.website_id = cs.site_id " \
                  "ORDER BY cs.last_date DESC".format(start, end, site, campaign)
            data = self.db.query(sql, json=True)
            return data
        except Exception as e:
            raise e

    def getCampaignDelta(self, site, start, end, campaign):
        '''
        Get Specific Campaign Delta
        :param site:
        :param start:
        :param end:
        :param campaign:
        :return:
        '''
        try:
            sql = "SELECT ws.*, cs.* FROM (SELECT site_id,creation_date, modification_date, last_date, campaign, clicks, cpc, spent, hb_uv, hb_revenue, p_uv,IFNULL(ads_uv,0.0) AS ads_uv, hb_factor, " \
                  "IFNULL(d_uv,0.0) AS d_uv, ((p_uv*clicks)+(IFNULL(ads_uv,0.0)*clicks)+(hb_uv*clicks)+(IFNULL(d_uv,0.0)*clicks)) as final_revenue, " \
                  "(((p_uv*clicks)+(IFNULL(ads_uv,0.0)*clicks)+(hb_uv*clicks)+(IFNULL(d_uv,0.0)*clicks)) - spent) as profit, " \
                  "(hb_uv*hb_factor) as hb_factor_uv, " \
                  "((((p_uv*clicks)+(IFNULL(ads_uv,0.0)*clicks)+(hb_uv*clicks)+(IFNULL(d_uv,0.0)*clicks)) - spent) / spent) as roi " \
                  "FROM skynet_harvester.rt_taboola_final_delta WHERE last_date >= '{0}' AND last_date <= '{1}' AND site_id={2} AND campaign='{3}' " \
                  "ORDER BY last_date DESC) AS cs " \
                  "LEFT JOIN (SELECT website_id, website_name,acronym FROM skynet_harvester.websites) as ws " \
                  "ON ws.website_id = cs.site_id " \
                  "ORDER BY cs.last_date DESC".format(start, end, site, campaign)
            data = self.db.query(sql, json=True)
            return data
        except Exception as e:
            raise e

    def getCampaignsSiteSummary(self, site, start, end):
        '''
        Get Site level Widget Summary
        to-do break into widgets and campaigns rest
        :param site:
        :param start:
        :param end:
        :return:
        '''
        try:
            sql = "SELECT   0 as website_id,'ALL Domains' as website_name,'ALL' as acronym,cs.* FROM (SELECT  0, SUM(clicks) as clicks,MAX(last_date) as max_date, MIN(last_date) as min_date, SUM(cpc*clicks)/SUM(clicks) as cpc, SUM(spent) as spent, " \
                  "SUM(IFNULL(d_uv,0.0)*clicks)/SUM(clicks) as d_uv, SUM(hb_uv*clicks)/SUM(clicks) as hb_uv, SUM(hb_revenue) as hb_revenue, SUM(p_uv*clicks)/SUM(clicks) as p_uv, SUM(IFNULL(ads_uv,0.0)*clicks)/SUM(clicks) as ads_uv, AVG(hb_factor) as hb_factor, " \
                  "(SUM(p_uv*clicks)+SUM(IFNULL(ads_uv,0.0)*clicks) + SUM(hb_uv*clicks)) as final_revenue, " \
                  "((SUM(p_uv*clicks)+SUM(IFNULL(ads_uv,0.0)*clicks)+SUM(hb_uv*clicks))  - SUM(spent)) as profit, " \
                  "(SUM(hb_uv*clicks)/SUM(clicks))*AVG(hb_factor) as hb_factor_uv, " \
                  "(((SUM(p_uv*clicks)+SUM(IFNULL(ads_uv,0.0)*clicks)+SUM(hb_uv*clicks)) - SUM(spent)) / SUM(spent)) as roi " \
                  "FROM skynet_harvester.rt_taboola_slim_final WHERE last_date >= '{0}' AND last_date <= '{1}' AND site_id IN ({2}) AND campaign NOT IN (SELECT campaign_id FROM skynet_harvester.app_campaigns_final_data where data_date='{0}' and device in ('mobile','tablet') group by campaign_id) AND hb_uv <> 0 ) AS cs ".format(start, end, site) + \
                  "UNION " \
                  "SELECT ws.*, cs.* FROM (SELECT  site_id, SUM(clicks) as clicks,MAX(last_date) as max_date, MIN(last_date) as min_date, SUM(cpc*clicks)/SUM(clicks) as cpc, SUM(spent) as spent, " \
                  "SUM(IFNULL(d_uv,0.0)*clicks)/SUM(clicks) as d_uv, SUM(hb_uv*clicks)/SUM(clicks) as hb_uv, SUM(hb_revenue) as hb_revenue, SUM(p_uv*clicks)/SUM(clicks) as p_uv, SUM(IFNULL(ads_uv,0.0)*clicks)/SUM(clicks) as ads_uv, AVG(hb_factor) as hb_factor, " \
                  "(SUM(p_uv*clicks)+SUM(IFNULL(ads_uv,0.0)*clicks) + SUM(hb_uv*clicks)) as final_revenue, " \
                  "((SUM(p_uv*clicks)+SUM(IFNULL(ads_uv,0.0)*clicks)+SUM(hb_uv*clicks))  - SUM(spent)) as profit, " \
                  "(SUM(hb_uv*clicks)/SUM(clicks))*AVG(hb_factor) as hb_factor_uv, " \
                  "(((SUM(p_uv*clicks)+SUM(IFNULL(ads_uv,0.0)*clicks)+SUM(hb_uv*clicks)) - SUM(spent)) / SUM(spent)) as roi " \
                  "FROM skynet_harvester.rt_taboola_slim_final WHERE last_date >= '{0}' AND last_date <= '{1}' AND site_id IN ({2}) AND hb_uv <> 0 AND campaign NOT IN (SELECT campaign_id FROM skynet_harvester.app_campaigns_final_data where data_date='{0}' and device in ('mobile','tablet') group by campaign_id)" \
                  "GROUP BY site_id " \
                  "ORDER BY spent DESC) AS cs " \
                  "LEFT JOIN (SELECT website_id, website_name,acronym FROM skynet_harvester.websites) as ws " \
                  "ON ws.website_id = cs.site_id " \
                  "ORDER BY profit DESC".format(start, end, site)
            data = self.db.query(sql, json=True)
            return data
        except Exception as e:
            raise e


    def getMediums(self, site, start, end, campaign):
        '''
        Get Specific Campaign all entries Unfiltered
        :param site:
        :param start:
        :param end:
        :param campaign:
        :return:
        '''
        try:
            sql = "SELECT ws.*, cs.* FROM (SELECT site_id, creation_date, modification_date, last_date, campaign, medium, visits, clicks, cpc, spent, p_uv, " \
                  "((p_uv*clicks)) as final_revenue, " \
                  "((p_uv*clicks) - spent) as profit, " \
                  "(((p_uv*clicks) - spent) / spent) as roi " \
                  "FROM skynet_harvester.rt_taboola_mediums_final WHERE last_date >= '{0}' AND last_date <= '{1}' AND site_id={2} AND campaign='{3}' " \
                  "ORDER BY last_date DESC) AS cs " \
                  "LEFT JOIN (SELECT website_id, website_name,acronym FROM skynet_harvester.websites) as ws " \
                  "ON ws.website_id = cs.site_id " \
                  "ORDER BY cs.spent DESC".format(start, end, site, campaign)
            data = self.db.query(sql, json=True)
            return data
        except Exception as e:
            raise e