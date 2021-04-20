import decimal
import logging
from datetime import date, datetime

import json
import pymysql

from config import cfg

db = None
try:
    xrange
except NameError:
    xrange = range


class DataStore(object):
    logger = cfg.set_logger(__name__, 'DataStore.log')

    def __init__(self):

        self.engine = self._create_connection()
        self.cursor = self.engine.cursor()

    def __delete__(self, instance):
        self.cursor.close()
        self.engine.close()

    def init_table(self):
        self.cursor.execute(cfg.DB_TABLE)

    def _create_connection(self):
        conv = pymysql.converters.conversions.copy()
        conv[246] = float  # convert decimals to floats
        conv[10] = str  # convert dates to strings
        sql_rds = pymysql.connect(conv=conv, autocommit=True, cursorclass=pymysql.cursors.DictCursor, **cfg.DB_SETTINGS)
        # very important
        sql_rds.set_charset('utf8')
        return sql_rds

    @staticmethod
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat().replace('T', ' ')
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

    def _upsert(self, db_table, create_fields, update_fields, values, auto_commit=True, static=True, print_sql=False):
        values_sql = []
        values_data = []
        if static:
            for value_lists in values:
                values_sql.append("(%s)" % (','.join(["'%s'" % (
                    self.engine.escape_string(
                        val.encode('ascii', 'ignore') if isinstance(val, basestring) else str(val).encode('ascii',
                                                                                                          'ignore'))) for
                                                      val in value_lists])))
        else:
            for value_lists in values:
                values_sql.append("(%s)" % (','.join(["%s" for i in range(len(value_lists))]),))
                # values_data.extend(map(str,value_lists))
                values_data.extend(value_lists)
        create_fields = [c.replace('optimize', 'opt') for c in create_fields]
        base_sql = "INSERT INTO %s (%s) VALUES " % (db_table, ",".join(create_fields))

        on_duplicates = []

        for field in update_fields:
            on_duplicates.append(field + "=VALUES(" + field + ")")

        sql = "%s %s ON DUPLICATE KEY UPDATE %s" % (base_sql, ", ".join(values_sql), ",".join(on_duplicates))

        if print_sql:
            print(sql)
        try:
            # self.cursor.execute("SET AUTOCOMMIT=0")
            if static:
                self.cursor.execute(sql)
            else:
                self.cursor.executemany(sql, [values_data])

            if auto_commit:
                self.engine.commit()
            self.logger.info('Finished')
            return self.cursor.lastrowid
        except Exception as e:
            self.logger.error(e)
            return False

    def insert_update_many(self, data_list=None, mysql_table=None):

        cursor = self.engine.cursor()
        cursor.execute("SET AUTOCOMMIT=0")
        query = ""
        values = []

        for data_dict in data_list:

            if not query:
                columns = ', '.join('`{0}`'.format(k) for k in data_dict)
                duplicates = ', '.join('{0}=VALUES({0})'.format(k) for k in data_dict)
                place_holders = ', '.join('%s'.format(k) for k in data_dict)
                query = "INSERT INTO {0} ({1}) VALUES ({2})".format(mysql_table, columns, place_holders)
                query = "{0} ON DUPLICATE KEY UPDATE {1}".format(query, duplicates)

            v = data_dict.values()
            values.append(v)

        try:
            cursor.executemany(query, values)
        except Exception, e:
            logging.error(e)
            return False

        db_conn.commit()

    def executeSP(self, *args, **kwargs):
        if kwargs.get('json'):
            json.dumps(self._query(args), default=self.json_serial)
        else:
            return self._executeSP(args)

    def _executeSP(self, *args):
        try:
            sql = str(args[0][0])
            params = tuple(args[0][1:len(args[0])])
            self.logger.info('Executing : [{}]'.format(sql))
            curs = self.engine.cursor()
            curs.execute(sql, params)
            self.engine.commit()
            res = curs.fetchall()
            curs.close()
            return res
        except Exception as e:
            self.logger.exception(e)
            raise e

    def execute(self, *args, **kwargs):
        if kwargs.get('json'):
            json.dumps(self._query(args), default=self.json_serial)
        else:
            return self._execute(args)

    def _execute(self, *args):
        try:
            sql = str(args[0][0])
            params = tuple(args[0][1:len(args[0])])
            self.logger.info('Executing : [{}]'.format(sql))
            curs = self.engine.cursor()
            curs.execute(sql, params)
            self.engine.commit()
            curs.close()
        except Exception as e:
            self.logger.exception(e)
            raise e

    def _query(self, *args):
        try:
            sql = str(args[0][0])
            params = tuple(args[0][1:])
            self.logger.info('Executing : [{}]'.format(sql))
            curs = self.engine.cursor()
            curs.execute(sql, params)
            res = curs.fetchall()
            curs.close()
            return res
        except Exception as e:
            self.logger.exception(e)
            raise e

    def query(self, *args, **kwargs):
        if kwargs.get('json'):
            return json.dumps(self._query(args), default=self.json_serial)
        else:
            return self._query(args)

    @staticmethod
    def _chunks(l, n):
        n = max(1, n)
        return (l[i:i + n] for i in xrange(0, len(l), n))

    def _extract_columns(self, obj={}):
        return obj.keys()

    def _column_replace(self, columns, update_columns, schema={}, entries=[]):

        update_columns = ['country_codes', 'device_targeting', 'language_targeting', 'status', 'ctr', 'utm_codes',
                          'country_targeting', 'bid_type', 'end_date', 'optimize', 'min_bid', 'enabled', 'budget',
                          'targeting_type', 'default_bid', 'max_bid', 'cost', 'start_date']

        json_columns = ['country_codes', 'device_targeting', 'language_targeting']

        meta_columns = ['account_id', 'website_id']

        prv_revcontent_campaigns = {'optimize': 'opt',
                                    'id': 'campaign_id',
                                    'name': 'campaign_name'}

        columns.extend(meta_columns)
        columns = [prv_revcontent_campaigns[field] if (field in prv_revcontent_campaigns.keys()) else field for field in columns]
        update_columns = [prv_revcontent_campaigns[field] if (field in prv_revcontent_campaigns.keys()) else field for field in update_columns]
        # Prepare json values and shipping order
        values = [[params[field] if (field not in json_columns) else json.dumps(params[field]) for field in columns] for params in entries]

    def upsert_dealer_status(self, params_list, status):
        try:
            fields = ['site_id', 'user_id', 'provider_id', 'account_id', 'campaign_id', 'inventory_id', 'targeting_id',
                      'widget_id', 'action', 'params', 'status', 'action_time']
            update_fields = ['status']
            values = [[status if field == 'status' else params[field] for field in fields] for params in params_list]

            batches = self._chunks(values, 1000)
            for batch in batches:
                self._upsert("prv_dealer_status", fields, update_fields, batch, True, False)

        except Exception as e:
            self.logger.exception(e)

    def upsert_many(self, params_list, dest_table):
        '''
        :param db_conn:
        :param params_list:
        :param dst:
        :return:
        '''
        try:
            try:
                fields = params_list[0].keys()
            except:
                fields = []
            update_fields = fields

            values = [[params[field] for field in fields] for params in params_list]

            batches = self._chunks(values, 1000)
            for batch in batches:
                self._upsert(dest_table, fields, update_fields, batch, True, False)

        except Exception as e:
            self.logger.exception(e)
            raise e


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
