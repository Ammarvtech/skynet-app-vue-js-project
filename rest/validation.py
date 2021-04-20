import libs.dao as dao
from libs.validation import ValidationData
from rest.base import *

Validation = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@Validation.get('/api/validation')
@authorize()
def get():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)

    date = get_argument("date")

    resp = {"data": ValidationData().get_data(date, usr_id)}
    for i in resp["data"]:
        i["diff"] = i["campaigns_revenue"] + i["dfp_nc_revenue"] + i['taboola_rt_nc_revenue'] + i["other"] + i['ad_sense_dfp'] + i['hb_dfp'] - i["website_revenue"]

    return resp


@Validation.get('/api/cost_validation')
@authorize()
def get():
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)

    date = get_argument("date")

    resp = {"data": ValidationData().get_cost_data(date, usr_id)}

    return resp


