from bottle import request, view, app, static_file, response
from config import cfg
from libs.authlayer import authlayer, authorize
import json

def post_form(name):
    return request.forms[name]

def get_argument(name):
    return request.query[name]

def post_argument(name, default=''):
    return request.json.get(name, default)
