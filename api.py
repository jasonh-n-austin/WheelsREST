from flask_peewee.rest import RestAPI, RestResource, UserAuthentication, AdminAuthentication, RestrictOwnerResource

from app import app
from auth import auth
from models import *


user_auth = UserAuthentication(auth)
admin_auth = AdminAuthentication(auth)

# instantiate our api wrapper
api = RestAPI(app, default_auth=user_auth)

# register our models so they are exposed via /api/<model>/
api.register(Rides)
api.register(Ridesphotos)
api.register(Ridesvehicles)
api.register(Rideswheels)
api.register(Taggroup)
api.register(Taggroups)
api.register(Vehiclebrands)
api.register(Vehiclemodelphotos)
api.register(Vehiclemodels)
api.register(Wheelbrands)
api.register(Wheelbrandlinks)
api.register(Wheelmfglocations)
api.register(Wheelmfgmethods)
api.register(Wheelmodellinks)
api.register(Wheelmodelphotos)
api.register(Wheelmodels)
api.register(Wheelsizes)
api.register(Wheelpcds)
api.register(Wheelspecs)
api.register(Wheeltags)

api.register(Globalconfig)
