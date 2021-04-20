from libs import dao
from libs.authlayer import initialize_storage
from rest.base import *

BackStage = app()
logger = cfg.set_logger(__name__, __name__ + '.log')


# @BackStage.get('/')
# def index():
#     return static_file("index.html", root='www')

@BackStage.post('/api/login')
def login():
    """Authenticate users"""
    initialize_storage()
    response.content_type = 'application/json'
    # body=request.json
    username = post_argument('username')
    password = post_argument('password')
    res = authlayer.login(username, password)
    if res:
        user = authlayer.current_user
        username = user.username
        settings = dao.App().getUserSettings(dao.App().getUserID(user.username))
    else:
        username = ''
        settings = []
    response.status = 200
    return {'success': res, 'user': {'username': username, 'settings': settings}}


@BackStage.route('/api/logout')
def logout():
    try:
        authlayer.logout()
        response.status = 200
        return {}
    except Exception as e:
        logger.exception(e)


@BackStage.route('/api/me')
def me():
    response.content_type = 'application/json'
    res = {}
    try:
        user = authlayer.current_user
        res['user'] = {
            'username': user.username,
            'role': user.role,
            'settings': dao.App().getUserSettings(dao.App().getUserID(user.username)),
        }
        return res
    except Exception as e:
        response.status = 401
        logger.warning(e)
        res['user'] = None
        return res


@BackStage.post('/api/create_user')
def create_user():
    try:
        authlayer.create_user(post_argument('username'), post_argument('role'), post_argument('password'), post_argument('email'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e)


@BackStage.post('/register')
def register():
    """Send out registration email"""
    authlayer.register(post_form('username'), post_form('password'), post_form('email_address'))
    return 'Please check your mailbox.'


@BackStage.route('/validate_registration/:registration_code')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    authlayer.validate_registration(registration_code)
    return 'Thanks. <a href="/login">Go to login</a>'


@BackStage.post('/api/reset_password')
def send_password_reset_email():
    """Send out password reset email"""
    try:
        initialize_storage()
        body = request.json
        authlayer.send_password_reset_email(
            username=body.get('username'),
            email_addr=body.get('email'),
            email_template=cfg.PROJECT_PATH + '/views/password_reset_email'
        )
        return {'success': True}
    except Exception as e:
        return {'error': str(e)}


@BackStage.post('/api/change_password')
def change_password():
    """Change password"""
    try:
        initialize_storage()
        body = request.json
        authlayer.reset_password(body.get('reset_code'), body.get('password'))
        authlayer._refresh()
        return {'success': True}
    except Exception as e:
        return {'error': str(e)}


# Admin-only pages

@BackStage.route('/my_role')
def show_current_user_role():
    """Show current user role"""
    session = BackStage.request.environ.get('beaker.session')
    print("Session from simple_webapp", repr(session))
    authlayer.require(fail_redirect='/login')
    return authlayer.current_user.role


@BackStage.route('/admin')
@view('admin_page')
def admin():
    """Only admin users can see this"""
    # aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user=authlayer.current_user,
        users=authlayer.list_users(),
        roles=authlayer.list_roles()
    )


@BackStage.post('/delete_user')
def delete_user():
    try:
        authlayer.delete_user(post_argument('username'))
        authlayer._refresh()
        return dict(ok=True, msg='')
    except Exception as e:
        print(repr(e))
        return dict(ok=False, msg=e.message)


@BackStage.post('/create_role')
def create_role():
    try:
        authlayer.create_role(post_argument('role'), post_argument('level'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@BackStage.post('/delete_role')
def delete_role():
    try:
        authlayer.delete_role(post_argument('role'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@BackStage.get('/api/role')
@authorize(role='admin')
def get_role():
    response.content_type = 'application/json'
    try:
        res = authlayer.list_roles()
        return dict(res)
    except Exception as e:
        return {}


@BackStage.get('/api/alert')
def get_alert():
    response.content_type = 'application/json'
    try:
        res = dao.App().getAlert()
        if res:
            return res[0]['alert']
        else:
            return None
    except Exception as e:
        return dict(ok=False, msg=e.message)


@BackStage.post('/api/setalert')
def set_alert():
    if request.json:
        try:
            dao.App().setAlert(request.json['alert'])
            return "true"
        except Exception as e:
            return dict(ok=False, msg=e.message)


@BackStage.get('/api/currency')
def get_currency():
    response.content_type = 'application/json'
    try:
        res = dao.App().getCurrency()
        if res:
            return res[0]['currency']
        else:
            return 1
    except Exception as e:
        return dict(ok=False, msg=e.message)
