import libs.dao as dao


def validate_args(request, args):
    for arg in args:
        if arg not in request.post_data or arg == 'null':
            request.set_status(400)
            request.response["error"] = "Missing {} argument".format(arg)
            return request


def get_account_details(source, campaign_id, site_id=0):
    account = dao.Campaigns().get_campaign_account(source, campaign_id, site_id)[0]
    try:
        # for outbrain budget action
        account['budget_id'] = account['budget_id'].replace('"', '')
    except Exception:
        pass
    try:
        account['client_id'] = account['client_id'].replace('"', '')
        account['client_secret'] = account['client_secret'].replace('"', '')
    except Exception:
        pass

    return account
