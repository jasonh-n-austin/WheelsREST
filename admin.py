import datetime
from flask import request, redirect

from flask_peewee.admin import Admin, ModelAdmin, AdminPanel
from flask_peewee.filters import QueryFilter

from app import app, db
from auth import auth

from models import *

admin = Admin(app, auth)
auth.register_admin(admin)

admin.register(Vehiclebrands)
admin.register(Vehiclemodels)

admin.register(Wheelbrands)
admin.register(Wheelbrandlinks)
class WheelmodelsAdmin(ModelAdmin):
	columns = ('wheelbrand', 'description')
	foreign_key_lookups = {'wheelbrand': 'name'}
admin.register(Wheelmodels)
class WheelmodellinksAdmin(ModelAdmin):
	columns = ('wheelmodel', 'url')
admin.register(Wheelmodellinks, WheelmodellinksAdmin)
class WheelmodelphotosAdmin(ModelAdmin):
	columns = ('wheelmodel', 'url')
admin.register(Wheelmodelphotos, WheelmodelphotosAdmin)

admin.register(Wheelmfgmethods)
admin.register(Wheelmfglocations)
admin.register(Wheelfinishes)
admin.register(Wheelsizes)
admin.register(Wheelpcds)

admin.register(TagItems)
admin.register(Taggroup)
class TaggroupsAdmin(ModelAdmin):
	columns = ('taggroup', 'tag')
admin.register(Tags, TaggroupsAdmin)
class WheeltagsAdmin(ModelAdmin):
	columns = ('wheelmodel', 'tag')
admin.register(Wheeltags, WheeltagsAdmin)

admin.register(User)
class GlobalconfigAdmin(ModelAdmin):
    columns = ('key', 'value',)
admin.register(Globalconfig, GlobalconfigAdmin)