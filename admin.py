import datetime
from flask import request, redirect

from flask_peewee.admin import Admin, ModelAdmin, AdminPanel
from flask_peewee.filters import QueryFilter

from app import app, db
from auth import auth

from models import *

admin = Admin(app, auth)
auth.register_admin(admin)
admin.register(Globalconfig)