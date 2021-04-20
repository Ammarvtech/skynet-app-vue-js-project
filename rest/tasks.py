from rest.base import *
import libs.dao as dao
Tasks = app()
logger = cfg.set_logger(__name__,__name__+'.log')


@Tasks.route('/api/tasks')
@authorize()
def get():
    try:
        action = get_argument('action')
        user = authlayer.current_user
        user_id = dao.App().getUserID(user.username)
        if action == "tasks":
            res = dict(enumerate(dao.Tasks().get_tasks(user_id), 0))
            for item in res.keys():
                res[item]['due_date'] = str(res[item]['due_date'])
                res[item]['created_on'] = str(res[item]['created_on'])
            return res

        elif action == "users":
            response = dict(enumerate(dao.App().getUsersList(),0))
            return response

        elif action == "websites":

            response = dict(enumerate(dao.WebsiteSettings().get_website_list_by_user(user_id), 0))
            return response

        elif action == "delete" or action == "close":
            item_id = get_argument('item_id')
            status_id = get_argument('status_id')
            success = dao.Tasks().change_task(action, item_id,status_id)
            return success

    except Exception as e:
        logger.exception(e.message)
        return False

@Tasks.post('/api/tasks')
@authorize()
def post():
    try:
        user = authlayer.current_user
        created_by = dao.App().getUserID(user.username)
        description = post_argument('description')
        selected_user = post_argument('selected_user')
        selected_website = post_argument('selected_website')
        priority = post_argument('priority')
        campaign = post_argument('campaign')
        title = post_argument('title')
        date = post_argument('date')
        action = post_argument('action')
        task_id = post_argument('task_id')

        try:
            success = dao.Tasks().insert_task(description, selected_user, selected_website, priority, campaign, title, date, created_by, action, task_id)
            return str(success)

        except Exception as e:
            logger.exception(e.message)
            return False
    except Exception as o:
        response.status = 400
        response.body['error'] = str(o)
        return response

