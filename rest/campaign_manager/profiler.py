import json
import libs.dao as dao
from rest.base import *
from libs.campaign_manager.profiler import ProfilerData
from libs.campaign_manager.campaigns import CampaignsData

Profiler = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@Profiler.get('/api/profiler')
@authorize()
def get():
    resp = {}
    usr = authlayer.current_user
    user_id = dao.App().getUserID(usr.username)
    resp["sets"] = ProfilerData().get_sets()
    resp["profiles"] = ProfilerData().get_profiles()
    resp["w_list"] = ProfilerData().get_w_lists()
    resp["countries"] = CampaignsData().get_countries()
    resp["user"] = user_id

    return resp


@Profiler.post('/api/profiler/profile')
@authorize()
def post():
    resp = {}

    post_data = dict(request.json)
    data = post_data["data"]
    usr = authlayer.current_user
    user_id = dao.App().getUserID(usr.username)
    resp["last_id"] = ProfilerData().set_profile(data, user_id)

    return resp


@Profiler.post('/api/profiler/set')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    data = post_data["data"]
    last_id = ProfilerData().set_item(data)
    resp["last_id"] = last_id if last_id else data["id"]
    return resp


@Profiler.post('/api/profiler/list')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    name = post_data["name"]
    list = post_data["list"]
    resp["last_id"] = ProfilerData().set_list(name, list)

    return resp

@Profiler.post('/api/profiler/list/update')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    resp = ProfilerData().update_list(post_data)

    return resp


@Profiler.post('/api/profiler/deletes')
@authorize()
def post():
    resp = {}

    post_data = dict(request.json)
    set_id = post_data["id"]
    resp["success"] = ProfilerData().delete_set(set_id)

    return resp


@Profiler.post('/api/profiler/deletel')
@authorize()
def post():
    resp = {}

    post_data = dict(request.json)
    list_id = post_data["id"]
    resp["success"] = ProfilerData().delete_list(list_id)

    return resp


@Profiler.post('/api/profiler/deletep')
@authorize()
def post():
    resp = {}

    post_data = dict(request.json)
    profile_id = post_data["id"]

    resp["success"] = ProfilerData().delete_profile(profile_id)

    return resp
