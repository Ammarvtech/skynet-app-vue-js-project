from rest.base import *
import libs.dao as dao

Bidder = app()
logger = cfg.set_logger(__name__, __name__ + '.log')


@Bidder.route('/api/bidder/data')
@authorize()
def get():
    resp = {}
    usr = authlayer.current_user
    usr_id = dao.App().getUserID(usr.username)

    resp["websites"] = dict(enumerate(dao.WebsiteSettings().get_website_list_by_user(usr_id), 0))
    resp["advertisers"] = dict(enumerate(dao.Dashboard().get_advertisers(), 0))

    return resp


@Bidder.route('/api/bidder')
@authorize()
def get():
    resp = {}
    args = {}

    # columns to select
    cols = request.query.keys()

    for key in cols:
        try:
            if get_argument(key):
                args[key] = get_argument(key)
        except Exception, e:
            logger.exception(e.message)
            return False

    try:
        resp["data"] = dao.Dashboard().get_bidder_data(cols, args)
        return resp
    except Exception as e:
        logger.exception(e.message)
    return False


# @Tasks.post('/api/tasks')
# @authorize()
# def post():
#     try:
#         user = authlayer.current_user
#         created_by = dao.App().getUserID(user.username)
#         description = post_argument('description')
#         selected_user = post_argument('selected_user')
#         selected_website = post_argument('selected_website')
#         priority = post_argument('priority')
#         campaign = post_argument('campaign')
#         title = post_argument('title')
#         date = post_argument('date')
#         action = post_argument('action')
#         task_id = post_argument('task_id')
#
#         try:
#             success = dao.Tasks().insert_task(description, selected_user, selected_website, priority, campaign, title,
#                                               date, created_by, action, task_id)
#             return str(success)
#
#         except Exception as e:
#             logger.exception(e.message)
#             return False
#     except Exception as o:
#         response.status = 400
#         response.body['error'] = str(o)
#         return response
