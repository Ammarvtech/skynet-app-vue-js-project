import json
import libs.dao as dao
import logging
from rest.base import *
from libs.optimization import OptimizationData
from libs.campaign_manager.campaigns import CampaignsData
Optimization = app()
response.content_type = 'application/json'
logger = cfg.set_logger(__name__, __name__ + '.log')


@Optimization.get('/api/optimization')
@authorize()
def get():
    resp = {}
    resp["data"] = OptimizationData().get_rules()
    resp["websites"] = CampaignsData().get_websites_list()
    resp["providers"] = CampaignsData().get_providers()
    resp["campaigns"] = OptimizationData().get_campaigns()

    return resp


@Optimization.post('/api/optimization')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    data = post_data["data"]
    action = 'create' if post_data["create"] else 'update'
    data["rules"] = rules_json(data, action)
    campaign_data = OptimizationData().get_single_campaign(data["campaign_id"])
    if data["campaign_id"] in ['All']:
        data['website_id'] = post_data["website_id"]
    resp = execute(action, data, campaign_data)
    return json.dumps(resp)


@Optimization.post('/api/optimization/rule/delete')
@authorize()
def post():
    resp = {}
    data = {}
    post_data = dict(request.json)
    row = post_data["row"]
    campaign = post_data["campaign"]
    updated_rules = remove_rule(row, campaign)
    data["record_id"] = campaign["id"]
    data["rules"] = updated_rules
    resp["success"] = OptimizationData().update_rule(data)
    return json.dumps(resp)


@Optimization.post('/api/optimization/multiple/switch')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    ids = post_data["ids"]
    status = post_data["status"]
    resp["success"] = OptimizationData().switch_multiple(ids, status)
    if resp["success"]:
        for opt_id in ids:
            set_rules_active(opt_id, status)
    return resp


@Optimization.post('/api/optimization/multiple/delete')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    ids = post_data["ids"]
    resp["success"] = OptimizationData().delete_multiple(ids)
    return resp


@Optimization.post('/api/optimization/switch')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    opt_id = post_data["id"]
    status = 1 if post_data["active"] else 0
    resp["success"] = OptimizationData().set_opt_active(opt_id, status)
    if resp["success"]:
        set_rules_active(opt_id, status)
    return resp


@Optimization.post('/api/optimization/rule/switch')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    data = post_data["data"]
    record_id = post_data["record_id"]
    rule_id = data["id"]
    status = 1 if data["active"] else 0
    if status:
        OptimizationData().activate_campaign(record_id)
    resp["success"] = set_single_rule_active(rule_id, record_id, status)
    return resp


@Optimization.post('/api/optimization/rule/run')
@authorize()
def post():
    resp = {}
    post_data = dict(request.json)
    campaign = post_data["campaign"]
    resp["success"] = CampaignRules().run(campaign)
    return resp


def execute(action, data, campaign_data):
    resp = {}
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)
    try:
        if action in ["create"]:
            resp = OptimizationData().set_rules(data, campaign_data, usr_id)
        elif action in ["update"]:
            if data["isNew"]:
                OptimizationData().activate_campaign(data["record_id"])
                data["rules"] = append_rule(data)
            else:
                data["rules"] = update_rule(data)
            resp["success"] = OptimizationData().update_rule(data)
        return resp
    except Exception as e:
        logging.exception(e.message)
        return -1, e.message


def rules_json(data, action):
    json = {}
    if action in ["create"]:
        json["id"] = '1'
        json["active"] = '1'
        json["roi"] = data["roi"]
        json["rule"] = "medium"
        json["spread"] = data["spread"]
        json["sessions"] = data["sessions"]
        json["time_period"] = [str(x) for x in data["dataPeriod"] if x is not None]
    else:
        json["id"] = data["id"]
        json["active"] = '1'
        json["roi"] = data["roi"]
        json["rule"] = "medium"
        json["spread"] = data["spread"]
        json["sessions"] = data["sessions"]
        json["time_period"] = [str(x) for x in data["dataPeriod"] if x is not None]
    return [json]


def append_rule(data):
    new_rule = {}
    current_rules = json.loads(OptimizationData().get_campaign_rules(data["record_id"])[0]["rules"])
    if len(current_rules):
        new_rule["id"] = str(int(current_rules[len(current_rules) - 1]["id"]) + 1)
    else:
        new_rule["id"] = '1'
    new_rule["active"] = '1'
    new_rule["roi"] = data["roi"]
    new_rule["rule"] = "medium"
    new_rule["spread"] = data["spread"]
    new_rule["sessions"] = data["sessions"]
    new_rule["time_period"] = [str(x) for x in data["dataPeriod"] if x is not None]
    current_rules.append(new_rule)

    return current_rules


def update_rule(data):
    data["rules"] = json.loads(OptimizationData().get_campaign_rules(data["record_id"])[0]["rules"])
    for rule in data["rules"]:
        if int(rule["id"]) == int(data["id"]):
        # if int(rule["id"]) == int(data["rules"][0]["id"]):
            rule["roi"] = data["roi"]
            rule["spread"] = data["spread"]
            rule["sessions"] = data["sessions"]
            rule["time_period"] = [str(x) for x in data["dataPeriod"] if x is not None]
    return data["rules"]


def remove_rule(row, campaign):
    current_rules = json.loads(OptimizationData().get_campaign_rules(campaign["id"])[0]["rules"])
    current_rules = [x for x in current_rules if x["id"] not in [str(row["id"]), row["id"]]]

    return current_rules


def set_rules_active(opt_id, status):
    data = {}
    data["record_id"] = opt_id
    data["rules"] = json.loads(OptimizationData().get_campaign_rules(opt_id)[0]["rules"])
    for rule in data["rules"]:
        rule["active"] = str(status)
    resp = OptimizationData().update_rule(data)
    return resp


def set_single_rule_active(rule_id, record_id, status):
    data = {}
    data["record_id"] = record_id
    data["rules"] = json.loads(OptimizationData().get_campaign_rules(record_id)[0]["rules"])
    for rule in data["rules"]:
        if int(rule["id"]) == int(rule_id):
            rule["active"] = str(status)
            resp = OptimizationData().update_rule(data)
            return resp
    return False


