import datetime
import decimal
import Queue
from datetime import date, datetime
from time import time
from threading import Thread
import bottle
import numpy as np
import pandas as pd
import math
import libs.dao as dao
from rest.base import *

logger = cfg.set_logger(__name__, __name__ + '.log')

Websites = app()
response.content_type = 'application/json'


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat().replace('T', ' ')
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


def united(data, start, end):
    utd = []
    d = datetime.datetime.strptime(start, "%Y-%m-%d")
    delta = datetime.timedelta(days=1)
    while d < datetime.datetime.strptime(end, "%Y-%m-%d"):  # loop over dates
        formatted_date = datetime.datetime.strftime(d, "%Y-%m-%d")
        items = [x for x in data if x["data_date"] in [formatted_date]]  # get all date items
        data_keys = data[0].keys()
        dic = {
            "data_date": formatted_date,
            "site_id": "all"
        }
        for key in data_keys:
            if key not in ["site_id", "data_date"]:
                dic[key] = sum([float(x[key]) for x in items])
        utd.append(dic)
        d += delta

    return utd


def validate_user_db_access(user_id, login_time):
    try:
        if not dao.App().validate_user_access(user_id, login_time):
            raise ValueError
        result = bottle.HTTPResponse(status=200, body={'allowed_access': True})
    except Exception as e:
        result = bottle.HTTPResponse(status=401, body={'allowed_access': False, 'error': e.message})
    return result


def get_inventory(site_id):
    """Enrich data frame with inventory data"""
    try:
        inventory = dao.WebsiteStatistics().get_inventory_by_site(site_id)
        return pd.DataFrame(inventory)
    except Exception as e:
        logger.exception(e)
        return None


def enqueue_dfp_data(site_id, device, src, start, end, user_id, restrict, queue):
    """Get campaigns DFP data"""
    tic = time()
    data = dao.WebsiteStatistics().get_website_campaigns_dfp_data(site_id, device, src, start, end, user_id, restrict)
    toc = time()
    queue.put(('data', pd.DataFrame(data).fillna({'enable': 1, 'bid': ''}).fillna(0), toc - tic))


def enqueue_rt_data(site_id, device, src, start, end, user_id, restrict, queue):
    """Get campaigns RT data"""
    tic = time()
    data = dao.WebsiteStatistics().get_website_campaigns_rt_data(site_id, device, src, start, end, user_id, restrict)
    toc = time()
    queue.put(('data', pd.DataFrame(data), toc - tic))


def enqueue_chart_data(site_id, device, src, start, end, user_id, queue):
    """Get data frame with chart data"""
    try:
        tic = time()
        chart_data = dao.WebsiteStatistics().get_rt_chart_data(site_id, device, src, start, end, user_id)
        toc = time()
        queue.put(('chart_data', pd.DataFrame(chart_data), toc - tic))
    except Exception as e:
        logger.exception(e)


def enqueue_bidders(user_id, src, site_id, queue):
    """Get data frame with bidders data"""
    try:
        tic = time()
        bidders = dao.Campaigns().get_bidders(user_id, src, site_id)
        toc = time()
        queue.put(('bidders', pd.DataFrame(bidders), toc - tic))
    except Exception as e:
        logger.exception(e)


def enqueue_automation_rules(queue):
    """Get data frame with automation rules"""
    try:
        tic = time()
        automation_rules = dao.Campaigns().get_automation_ruls()
        toc = time()
        queue.put(('automation_rules', pd.DataFrame(automation_rules), toc - tic))
    except Exception as e:
        logger.exception(e)


def run_threads_in_queue(queue, threads):
    """Run multiple threads in parallel, return dictionary of results"""
    res = {}
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # global logger
    while not queue.empty():
        r = queue.get()
        res[r[0]] = r[1]
        # logger.info('Query runtime: {} duration is {}'.format(r[0], r[2]))

    return res


def merge_enqueued_data(data, res):
    """Merge enqueued data in res to data"""
    try:
        data = pd.merge(data, res['bidders'], how='left', on=['campaign_id']).fillna(0)
    except KeyError:
        pass
    try:
        data = pd.merge(data, res['automation_rules'], how='left', on=['campaign_id'])
    except KeyError:
        pass
    try:
        data['automation_active'] = data['automation_active'].apply(lambda x: 1 if math.isnan(x) else x)
    except KeyError:
        pass

    return {'data': json.dumps(data.T.to_dict().values(), default=json_serial)}


@Websites.post('/api/website/validate')
@authorize()
def validate():
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = request.json.get('params').get('login_time')
    return validate_user_db_access(user_id, login_time)


@Websites.get('/api/website/user_campaigns_dfp')
@authorize()
def campaigns():
    site_id = get_argument('site_id')
    device = get_argument('device')
    src = get_argument('source')
    start = get_argument('start')
    end = get_argument('end')
    restrict = get_argument('restrict')
    login_time = get_argument('login_time')
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow
    res = {}

    try:
        queue = Queue.Queue()
        threads = (
            Thread(target=enqueue_dfp_data, name='dfp_data',
                   args=(site_id, device, src, start, end, user_id, restrict, queue)),
            Thread(target=enqueue_bidders, name='dfp_bidders', args=(user_id, src, site_id, queue)),
            Thread(target=enqueue_automation_rules, name='dfp_automation', args=(queue,)))

        res = run_threads_in_queue(queue, threads)
        data = res['data']
        res = merge_enqueued_data(data, res)
    except Exception as e:
        global logger
        logger.exception(e)
        res = {}
    finally:
        return res


@Websites.get('/api/website/campaigns_rt_validation')
@authorize()
def campaigns():
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')
    device = get_argument('device')
    src = get_argument('source')
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    try:
        # Get all websites
        website_list = pd.DataFrame(dict(enumerate(dao.WebsiteSettings().get_website_list_by_user(user_id), 0))).T

        # Get all Real-Time campaigns data
        data_rt = pd.DataFrame(
            dao.WebsiteStatistics().get_website_campaigns_rt_data_valid(site_id, device, src, start, end, user_id))

        # Get all DFP campaigns data
        data_dfp = dao.WebsiteStatistics().get_website_campaigns_dfp_data_valid(site_id, device, src, start, end,
                                                                                user_id)
        data_dfp = pd.DataFrame(dict(enumerate(data_dfp, 0))).T

        # Casting Columns
        data_rt['data_date'] = data_rt['data_date'].astype(str)
        data_rt['site_id'] = data_rt['site_id'].astype(int)
        website_list.rename(columns={'website_id': 'site_id'}, inplace=True)
        website_list['site_id'] = website_list['site_id'].astype(int)
        data_dfp['site_id'] = data_dfp['site_id'].astype(int)
        data_rt['campaign_id'] = data_rt['campaign_id'].astype(str)
        # Adjust date to be serializable
        # data_rt['data_date'] = data_rt['data_date'].map(lambda val: val.split(' ')[0])
        data_dfp['data_date'] = data_rt['data_date'].map(lambda val: val.split(' ')[0])
        # Merging DFP data with RT data
        mrg = pd.merge(data_dfp, data_rt, how='left', on=['campaign_id', 'data_date', 'site_id'])

        # Merging [ RT & DFP ] with website name
        final_data = pd.merge(mrg, website_list, how='left', on=['site_id'])
        final_data.fillna(0, inplace=True)
        final_data.rename(columns={'source_x': 'source', 'device_x': 'device', 'creation_date_x': 'creation_date',
                                   'name_x': 'name'}, inplace=True)

        # calculating difference in data X as dfp and Y as RT
        # Manipulating data to Percentage
        final_data['clicks_diff'] = (1 - (
            final_data['clicks_x'].astype(int).divide(final_data['clicks_y'].astype(int)))) * 100
        # Handling NaN and infinity
        final_data['clicks_diff'] = final_data['clicks_diff'].replace([np.inf, -np.inf], np.nan)
        final_data['clicks_diff'] = final_data['clicks_diff'].fillna(0).abs()

        final_data['revenue_diff'] = (1 - (final_data['revenue_x'].astype(float).round(4).divide(
            final_data['revenue_y'].astype(float).round(4)))) * 100
        final_data['revenue_diff'] = final_data['revenue_diff'].replace([np.inf, -np.inf], np.nan)
        final_data['revenue_diff'] = final_data['revenue_diff'].fillna(0).abs()

        final_data['cost_diff'] = (1 - (
            final_data['cost_x'].astype(float).round(2).divide(final_data['cost_y'].astype(float).round(2)))) * 100
        final_data['cost_diff'] = final_data['cost_diff'].replace([np.inf, -np.inf], np.nan)
        final_data['cost_diff'] = final_data['cost_diff'].fillna(0).abs()

        # final_data['profit_diff'] = (1 - (
        #    final_data['profit_x'].astype(float).round(2).divide(final_data['profit_y'].astype(float).round(2)))) * 100
        # final_data['profit_diff'] = final_data['profit_diff'].replace([np.inf, -np.inf], np.nan)
        # final_data['profit_diff'] = final_data['profit_diff'].fillna(0).abs()

        final_data['final_uv_diff'] = (1 - (final_data['final_uv_x'].astype(float).round(4).divide(
            final_data['final_uv_y'].astype(float).round(4)))) * 100
        final_data['final_uv_diff'] = final_data['final_uv_diff'].replace([np.inf, -np.inf], np.nan)
        final_data['final_uv_diff'] = final_data['final_uv_diff'].fillna(0).abs()

        final_data['avg_bid_diff'] = (1 - (final_data['avg_bid_x'].astype(float).round(2).divide(
            final_data['avg_bid_y'].astype(float).round(2)))) * 100
        final_data['avg_bid_diff'] = final_data['avg_bid_diff'].replace([np.inf, -np.inf], np.nan)
        final_data['avg_bid_diff'] = final_data['avg_bid_diff'].fillna(0).abs()

        # Dropping all unneeded columns
        # final_data.drop(final_data.columns.difference(['campaign_id', 'site_id', 'data_date', 'clicks_diff', 'clicks_x',
        #                                                'clicks_y', 'revenue_x', 'revenue_y', 'revenue_diff',
        #                                                'website_name', 'cost_diff', 'cost_x', 'cost_y', 'profit_diff',
        #                                                'profit_x', 'profit_y', 'final_uv_diff', 'final_uv_x',
        #                                                'final_uv_y', 'avg_big_x', 'avg_big_y', 'avg_big_diff', 'device',
        #                                                'source', 'name', 'creation_date']), 1, inplace=True)

        # Sorting By clicks dfp
        final_data.drop(columns='rt_creation_date', inplace=True)
        final_data = final_data.sort_values('clicks_x')
        # final_data.to_csv('~/Downloads/difference_rt_dfp.csv')
        data = dict(enumerate(final_data.to_dict(orient='records'), 0))
        return data
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Websites.get('/api/website/action_log')
@authorize()
def campaigns():
    src = get_argument('source')
    site_id = get_argument('site_id')
    start = get_argument('start')
    end = get_argument('end')
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    try:
        website_list = pd.DataFrame(dict(enumerate(dao.WebsiteSettings().get_website_list_by_user(user_id), 0))).T
        website_list.rename(columns={'website_id': 'site_id'}, inplace=True)
        df_action_log = pd.DataFrame(
            dao.WebsiteStatistics().get_website_campaigns_action_log(site_id, src, start, end, user_id))

        df_action_log['site_id'] = df_action_log['site_id'].astype(int)
        website_list['site_id'] = website_list['site_id'].astype(int)

        final_data = pd.merge(df_action_log, website_list, how='left', on=['site_id'])

        # Adjust date to be serializable
        dates = ['creation_date', 'data_date']
        for d in dates:
            final_data[d] = final_data[d].astype(str)
            final_data[d] = final_data[d].map(lambda val: val.split(' ')[0])

        final_data['est_time'] = final_data['est_time'].astype(str)

        final_data['is_auto'] = final_data['is_auto'].apply(lambda x: 'Yes' if x == 1 else 'No')

        data = dict(enumerate(final_data.to_dict(orient='records'), 0))
        return json.dumps(data, indent=4, sort_keys=True, default=str)
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Websites.get('/api/website/user_campaigns_rt')
@authorize()
def campaigns():
    site_id = get_argument('site_id')
    src = get_argument('source')
    device = get_argument('device')
    start = get_argument('start')
    end = get_argument('end')
    restrict = get_argument('restrict')
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow
    res = {}

    try:
        queue = Queue.Queue()

        threads = (
            Thread(target=enqueue_rt_data, name='rt_data',
                   args=(site_id, device, src, start, end, user_id, restrict, queue)),
            Thread(target=enqueue_chart_data, name='rt_chart_data',
                   args=(site_id, device, src, start, end, user_id, queue)),
            Thread(target=enqueue_bidders, name='rt_bidders', args=(user_id, src, site_id, queue)),
            Thread(target=enqueue_automation_rules, name='rt_automation', args=(queue,)))

        res = run_threads_in_queue(queue, threads)
        data = res['data']
        data = pd.merge(data, res['chart_data'], how='left', on=['campaign_id']).fillna(0)
        res = merge_enqueued_data(data, res)
    except Exception as e:
        global logger
        logger.exception(e)
    finally:
        return res


@Websites.get('/api/website/chart_data')
def chart():
    site_id = get_argument('site_id')
    device = get_argument('device')
    src = get_argument('source')
    start = get_argument('start')
    end = get_argument('end')

    resp = dao.WebsiteSettings().get_chart_data(site_id, device, src, start, end)

    if site_id in ['all']:
        resp = united(resp, start, end)
    for item in response:
        item['revenue'] = sum(((float(val) for key, val in item.iteritems() if key.startswith('income_'))))
        item['cost'] = sum(((float(val) for key, val in item.iteritems() if key.startswith('spent_'))))
        item['uv'] = item['revenue'] / item['sessions']
        item['profit'] = item['revenue'] - item['cost']

        if float(item['cost']) > 0:
            item['roi'] = item['profit'] / item['cost']
        else:
            item['roi'] = 0

    return dict(enumerate(resp, 0))


@Websites.get('/api/website/source')
def source():
    return dict(enumerate(dao.App().getSources(), 0))


@Websites.get('/api/website/user_websites')
@authorize()
def websites():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)

    res = dict(enumerate(dao.WebsiteSettings().get_website_list_by_user(usr_id), 0))
    return res


@Websites.get('/api/website/keys')
def keys():
    return dict(enumerate(dao.SiteConfiguration().get_website_settings_keys(), 0))


@Websites.get('/api/website/themes')
def themes():
    return dict(enumerate(dao.SiteConfiguration().get_themes(), 0))


@Websites.get('/api/website/site_config')
def site_config():
    site_id = get_argument('site_id').lower()
    device = get_argument('device').lower()
    key = get_argument('key').lower()
    resp = {
        'result': dict(enumerate(dao.SiteConfiguration().get_website_settings_by_site(site_id, device, key), 0)),
        'data': {
            'site_id': site_id,
            'device': device,
            'key': key,
        }
    }
    return resp


@Websites.post('/api/website/site_config')
@authorize()
def update_site_config():
    post_data = request.json['params']
    site_id = post_data['site_id']
    key = post_data['key']
    device = post_data['device']
    value = post_data['value']
    ab_testing_percentage = post_data['ab_testing_percentage']
    ab_testing_config = post_data['ab_testing_config']
    group_vals = post_data['group_vals'] if post_data['group_vals'] else '{}'
    use_group_vals = post_data['use_group_vals']
    group_country_settings = post_data['group_country_settings'] if post_data['group_country_settings'] else '{}'
    user_id = dao.App().getUserID(authlayer.current_user.username)
    login_time = post_data['login_time']
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    resp = {
        'status': dao.SiteConfiguration().update_website_settings_by_site(site_id, key, device, value,
                                                                          ab_testing_percentage, ab_testing_config,
                                                                          group_vals, use_group_vals,
                                                                          group_country_settings),
        'data': {
            'site_id': site_id,
            'key': key,
            'device': device,
            'value': value,
            'ab_testing_percentage': ab_testing_percentage,
            'ab_testing_config': ab_testing_config,
            'group_vals': group_vals,
            'use_group_vals': use_group_vals,
            'group_country_settings': group_country_settings
        }
    }

    return resp


@Websites.post('/api/website/batch/site_config')
@authorize()
def update_batch_site_config():
    post_data = request.json['params']
    user_id = dao.App().getUserID(authlayer.current_user.username)
    login_time = post_data['login_time']
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    fields = ','.join([f for f in post_data['fields'] if post_data['fields'][f]])
    sites = post_data['sites'].split(',')

    resp = {
        'status': dao.SiteConfiguration().update_website_settings_batch(post_data['source'], sites, fields,
                                                                        post_data['device'], post_data['key']),
        'data': {
            'source': post_data['source'],
            'fields': fields,
            'device': post_data['device'],
            'key': post_data['key'],
            'sites': sites,
        },
    }

    return resp


@Websites.get('/api/website/config_history')
def history():
    site_id = get_argument('site_id').lower()
    device = get_argument('device').lower()
    key = get_argument('key').lower()
    result = dict(enumerate(dao.SiteConfiguration().get_website_settings_history(site_id, device, key), 0))
    resp = {
        'result': json.loads(json.dumps(result, default=lambda obj: (obj.isoformat() if isinstance(obj, datetime)
                                                                             or isinstance(obj, date) else None))),
        'data': {
            'site_id': site_id,
            'device': device,
            'key': key,
        }
    }
    return resp


@Websites.get('/api/website/colors')
def colors():
    device = get_argument('device').lower()
    src = get_argument('source').lower()
    page_type = get_argument('page_type').lower()

    res = dict(enumerate(dao.Dashboard().get_colors(src, device, page_type), 0))
    return res


@Websites.get('/api/website/last_update')
def get_last_update():
    site_id = get_argument('site_id').lower()
    res = dict(enumerate(dao.Dashboard().get_last_update(site_id), 0))
    return res


@Websites.get('/api/bidder/remove_bidder')
@authorize()
def remove_bidder():
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    try:
        bidder_id = get_argument('id')
        res = dao.Campaigns().delete_bidder(bidder_id)
        return {'res': res}
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Websites.get('/api/bidder/save_bidders')
@authorize()
def save_bidder():
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    bidders = json.loads(get_argument('bidders'))
    bidders = [dict(item, user_id=user_id) for item in bidders]

    site_id = get_argument('site_id')
    src = get_argument('source')
    campaign_id = get_argument('campaign_id')

    try:
        dao.Campaigns().save_bidders(bidders)
        bidders = dao.Campaigns().get_bidders(user_id, src, site_id, campaign_id)
        return {'res': bidders}

    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Websites.get('/api/website/campaign/duplicate_templates')
@authorize()
def get_duplicate_templates():
    user = authlayer.current_user
    user_id = dao.App().getUserID(user.username)
    login_time = get_argument('login_time')
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow
    try:
        site_id = get_argument('site_id')
        res = dao.WebsiteSettings().get_duplicate_templates('taboola', site_id, user_id)
        return {'res': res}
    except Exception as e:
        global logger
        logger.exception(e)
        return {}


@Websites.get('/api/website/audience_mapping')
@authorize()
def get_duplicate_audience_mapping():
    try:
        src = get_argument('source')
        res = dao.WebsiteSettings().get_duplicate_audience_mapping(src)
        return {'res': res}
    except Exception as e:
        global logger
        logger.exception(e)
        return {}
