from rest.base import *
import libs.dao as dao
from rest.websites.website import validate_user_db_access

Revenue = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@Revenue.get('/api/revenue')
@authorize()
def get():
    resp = {}
    date_start = get_argument("date_start")
    date_end = get_argument("date_end")
    device = get_argument("device")
    yesterday = get_argument("date_yesterday")
    login_time = get_argument('login_time')
    usr = authlayer.current_user
    user_id = dao.App().getUserID(usr.username)
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    groups = dao.App().getUserGroup(usr.username)[0]['groups_ids']

    resp["report"] = dao.Revenue().get_report(date_start, date_end, groups)
    resp["device_report"] = dao.Revenue().get_device_report(date_start, date_end, groups)
    if date_start == date_end:
        if device in ['null']:
            resp["yesterday_report"] = dao.Revenue().get_yesterday_report(yesterday, groups)
        else:
            resp["yesterday_report"] = dao.Revenue().get_device_report(yesterday, yesterday, groups)
        if not resp["yesterday_report"]:
            resp["yesterday_report"] = resp["report"]
    else:
        resp["yesterday_report"] = resp["report"]
    return resp


@Revenue.post('/api/revenue')
@authorize()
def post():
    post_data = dict(request.json)
    login_time = post_data['login_time']
    usr = authlayer.current_user
    user_id = dao.App().getUserID(usr.username)
    allow = validate_user_db_access(user_id, login_time)
    if allow.status_code != 200:
        return allow

    # validate args
    resp = {}
    for arg in ["date", "site_id", "key", "val"]:
        if arg not in post_data:
            response.status = 400
            resp["error"] = "Missing {} argument".format(arg)
            return resp

    resp["status"] = dao.Revenue().setCustomAmount(
        post_data.get("site_id"), post_data.get("key"),
        post_data.get("val"), post_data.get("date"))

    return resp


@Revenue.get('/api/init_revenue')
@authorize()
def get():
    data = {}
    date_start = get_argument("start")
    date_end = get_argument("end")
    source = get_argument("source")
    device = get_argument("device")

    data['website_sum'] = dao.Revenue().get_revenue_report_by_site(date_start, date_end, source, device)
    data['source_sum'] = dao.Revenue().get_revenue_report_by_source(date_start, date_end, source, device)
    data['devices'] = dao.Revenue().get_revenue_report_by_device(date_start, date_end, source, device)

    # Provider chart
    if data['source_sum']:
        data['source_sum'] = build_chart(data['source_sum'])
    if data['devices']:
        data['devices'] = build_chart(data['devices'])

    return data


def build_chart(data):
    final_data = []
    inited = []
    for i in data:
        if i['site_id'] not in inited:
            website_data = [d for d in data if d['site_id'] == i['site_id']]
            item = {}
            for j in website_data:
                if j['revenue'] > 1 and j['spent'] > 1:
                    item['income_' + j['type']] = j['revenue']
                    item['spent_' + j['type']] = j['spent']

            item['site_id'] = i['site_id']
            inited.append(i['site_id'])
            if len(item) > 1:
                final_data.append(item)

    return final_data
