from flask_peewee.rest import RestAPI, RestResource, UserAuthentication, AdminAuthentication, RestrictOwnerResource

from app import app
from auth import auth
from models import *


user_auth = UserAuthentication(auth)
admin_auth = AdminAuthentication(auth)

# instantiate our api wrapper
api = RestAPI(app, default_auth=user_auth)

image_host = 'http://wheelspecs.com'
model_vdir = Globalconfig.select().where(Globalconfig.key == 'WheelModelPhotoVDir')[0].value
brand_vdir = Globalconfig.select().where(Globalconfig.key == 'WheelBrandPhotoVDir')[0].value
def tweak_model_photourl(data):
	for item in data:
		if (item == 'photourl' and data[item]):
			data[item] = '%s%s%s' % (image_host,model_vdir,data[item])
	return data

def tweak_brand_photourl(data):
	for item in data:
		if (item == 'photourl' and data[item]):
			data[item] = '%s%s%s' % (image_host,brand_vdir,data[item])
	return data

# register our models so they are exposed via /api/<model>/
api.register(Rides)
api.register(Ridesphotos)
api.register(Ridesvehicles)
api.register(Rideswheels)
#api.register(Tags)
class TaggroupResource(RestResource):
	exclude = ('id', 'updatedby',)
api.register(Taggroup, TaggroupResource)
class TagsResource(RestResource):
	exclude = ('id','updatedby', 'lastupdated', 'total', )
class TagsgroupResource(RestResource):
	exclude = ('id','updatedby', 'lastupdated', )
class TaggroupsResource(RestResource):
	exclude = ('updatedby', )
	include_resources = {
		'tag': TagsResource,
		'taggroup': TagsgroupResource
	}
api.register(Tags, TaggroupsResource)
api.register(Vehiclebrands)
api.register(Vehiclemodelphotos)
class VehiclebrandsSummaryResource(RestResource):
	exclude = ('url' 'lastupdated', 'notes', 'updatedby')
	def prepare_data(self, obj, data):
		return tweak_brand_photourl(data)
class VehiclemodelsResource(RestResource):
	include_resources = {
		'vehiclebrand': VehiclebrandsSummaryResource
	}
api.register(Vehiclemodels, VehiclemodelsResource)

class WheelbrandsResource(RestResource):
    exclude = ('updatedby')
    def prepare_data(self, obj, data):
    	return tweak_brand_photourl(data)    
api.register(Wheelbrands, WheelbrandsResource)

api.register(Wheelbrandlinks)
api.register(Wheelmfglocations)
api.register(Wheelmfgmethods)
api.register(Wheelmodellinks)
api.register(Wheelmodelphotos)

class WheelmfgmethodSummaryResource(RestResource):
	exclude = ('lastupdated', 'updatedby', )
class WheelmfglocationSummaryResource(RestResource):
	exclude = ('lastupdated', 'updatedby', )	
class WheelbrandsSummaryResource(RestResource):
	exclude = ('url', 'notes', 'lastupdated', 'updatedby')
	def prepare_data(self, obj, data):
		return tweak_brand_photourl(data)
#class WheelmodelsSimilarResource(RestResource):
#	exclude = ('discontinued','lastupdated','mfgspecdate', 'mfgspecurl', 'notes', 'searchterm', 'similar', 'updatedby', 'wheelbrand', 'wheelmfglocation', 'wheelmfgmethod',)
class WheelmodelsResource(RestResource):
	#delete_recursive = True
	include_resources = {
		'wheelbrand': WheelbrandsSummaryResource,
		'wheelmfgmethod': WheelmfgmethodSummaryResource,
		'wheelmfglocation': WheelmfglocationSummaryResource,
#		'similar': WheelmodelsSimilarResource,
	}
	exclude = ('wheelmfglocation', 'searchterm')
	def prepare_data(self, obj, data):
		return tweak_model_photourl(data)
api.register(Wheelmodels, WheelmodelsResource, allowed_methods=['GET','PUT','POST'])

api.register(Wheelsizes)
api.register(Wheelpcds)
api.register(Wheelspecs)
class WheelmodelSummaryResource(RestResource):
	exclude = ('discontinued','lastupdated','mfgspecdate', 'mfgspecurl', 'notes', 'searchterm', 'similar', 'updatedby', 'wheelbrand', 'wheelmfglocation', 'wheelmfgmethod',)
class WheeltagsResource(RestResource):
	exclude = ('updatedby', )
	include_resources = {
		'wheelmodel': WheelmodelSummaryResource,
		'tag': TagsResource,
	}
api.register(Wheeltags, WheeltagsResource)

api.register(Globalconfig)
