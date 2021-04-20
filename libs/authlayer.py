import os
import shutil
import sys

from cork import Cork
from cork.base_backend import BackendIOException

from config import cfg
from datastore.sql import DataStore

try:
    import json
except ImportError:  # pragma: no cover
    import simplejson as json

log = cfg.set_logger(__name__, __name__ + '.log')
is_py3 = (sys.version_info.major == 3)

try:
    dict.iteritems
    py23dict = dict
except AttributeError:
    class py23dict(dict):
        iteritems = dict.items


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_py3 and isinstance(obj, bytes):
            return obj.decode()
        return json.JSONEncoder.default(self, obj)


class JsonBackend(object):
    """JSON file-based storage backend."""

    def __init__(self, directory, users_fname='users',
                 roles_fname='roles', pending_reg_fname='register', initialize=False):
        """Data storage class. Handles JSON files

        :param users_fname: users file name (without .json)
        :type users_fname: str.
        :param roles_fname: roles file name (without .json)
        :type roles_fname: str.
        :param pending_reg_fname: pending registrations file name (without .json)
        :type pending_reg_fname: str.
        :param initialize: create empty JSON files (defaults to False)
        :type initialize: bool.
        """
        self.ds = DataStore()
        assert directory, "Directory name must be valid"
        self._directory = directory
        self.users = py23dict()
        self._users_fname = users_fname
        self.roles = py23dict()
        self._roles_fname = roles_fname
        self._mtimes = py23dict()
        self._pending_reg_fname = pending_reg_fname
        self.pending_registrations = py23dict()
        if initialize:
            self._initialize_storage()
        self._refresh()  # load users and roles

    def _initialize_storage(self):
        """Create empty JSON files"""

        db_roles = {}
        db_users = {}
        # add user is acitve = 1
        for user in self.ds.query('SELECT * FROM users where active = 1'):
            user.pop('creation_date')
            user.pop('modification_date')
            db_users[user['username']] = user
        for role in self.ds.query('SELECT * FROM roles'):
            db_roles[role['role']] = role['level']

        self._savejson(self._users_fname, db_users)
        self._savejson(self._roles_fname, db_roles)
        self._savejson(self._pending_reg_fname, {})

    def _refresh(self):
        """Load users and roles from JSON files, if needed"""
        self._loadjson(self._users_fname, self.users)
        self._loadjson(self._roles_fname, self.roles)
        self._loadjson(self._pending_reg_fname, self.pending_registrations)

    def _loadjson(self, fname, dest):
        """Load JSON file located under self._directory, if needed

        :param fname: short file name (without path and .json)
        :type fname: str.
        :param dest: destination
        :type dest: dict
        """
        try:
            fname = "%s/%s.json" % (self._directory, fname)
            mtime = os.stat(fname).st_mtime

            if self._mtimes.get(fname, 0) == mtime:
                # no need to reload the file: the mtime has not been changed
                return

            with open(fname) as f:
                json_data = f.read()
        except Exception as e:
            raise BackendIOException("Unable to read json file %s: %s" % (fname, e))

        try:
            json_obj = json.loads(json_data)
            dest.clear()
            dest.update(json_obj)
            self._mtimes[fname] = os.stat(fname).st_mtime
        except Exception as e:
            raise BackendIOException("Unable to parse JSON data from %s: %s" \
                                     % (fname, e))

    def _savejson(self, fname, obj):
        """Save obj in JSON format in a file in self._directory"""
        fname = "%s/%s.json" % (self._directory, fname)
        try:
            with open("%s.tmp" % fname, 'w') as f:
                json.dump(obj, f, cls=BytesEncoder)
                f.flush()
            shutil.move("%s.tmp" % fname, fname)
        except Exception as e:
            raise BackendIOException("Unable to save JSON file %s: %s" \
                                     % (fname, e))

    def save_users(self):
        """Save users in a JSON file"""
        self._savejson(self._users_fname, self.users)
        self._sql_save_users()
        self._refresh()

    def _sql_save_users(self):
        """Save users in a JSON file"""

        def usrnm(key, dic):
            dic['username'] = key
            return dic

        try:
            params_list = [usrnm(k, v) for k, v in self.users.iteritems()]
        except:
            params_list = [usrnm(k, v) for k, v in self.users.items()]
        try:
            fields = ['username', 'first_name', 'last_name', 'role', 'hash',
                      'email_addr', '`desc`', 'creation_date', 'last_login', 'active', 'revenue_report', 'groups_ids']
            update_fields = ['hash', 'role', 'email_addr']
            values = [[params.get(field, None) for field in fields] for params in params_list]
            batches = self.ds._chunks(values, 1000)
            for batch in batches:
                self.ds._upsert(self._users_fname, fields, update_fields, batch, True, False)

        except Exception as e:
            print(e)

    def save_roles(self):
        """Save roles in a JSON file"""
        self._savejson(self._roles_fname, self.roles)

    def save_pending_registrations(self):
        """Save pending registrations in a JSON file"""
        self._savejson(self._pending_reg_fname, self.pending_registrations)


# Init hybrid backend
jb = JsonBackend(directory=cfg.CACHE_PATH, initialize=True)
cfg.set_logger('cork.cork', 'cork.log', level=10)
authlayer = Cork(backend=jb,
                 email_sender='app@skyneto.com',
                 smtp_url='starttls://{0}:{1}@{2}'.format(cfg.AWS_SMTP['Username'],
                                                          cfg.AWS_SMTP['Password'],
                                                          cfg.AWS_SMTP['Server']))
# Alias the authorization decorator with defaults
authorize = authlayer.make_auth_decorator(role="user")


def initialize_storage():
    try:
        jb.ds = DataStore()
        jb._initialize_storage()
        jb._refresh()
    except Exception as e:
        log.exception(e)
