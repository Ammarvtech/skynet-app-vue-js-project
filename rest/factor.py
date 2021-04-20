import libs.dao as dao
from libs.factor import FactorData
from rest.base import *

Factor = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@Factor.post('/api/set_factor')
@authorize(role='admin', fail_redirect='/')
def get():

    factor = post_argument("factor")
    date = post_argument("date")

    resp = {"data": FactorData().set_factor(factor, date)}

    return resp


@Factor.get('/api/get_factor')
@authorize(role='admin', fail_redirect='/')
def get():

    resp = {"data": FactorData().get_factor_data()}

    return resp


