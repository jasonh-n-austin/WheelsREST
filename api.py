from flask_peewee.rest import RestAPI, RestResource, UserAuthentication, AdminAuthentication, RestrictOwnerResource, url_for, request

from app import app
from auth import auth
from models import *
from socket import gethostname

user_auth = UserAuthentication(auth)
admin_auth = AdminAuthentication(auth)

allowed_verbs=['GET','PUT','POST']
no_attrib=('lastupdated', 'updatedby')
no_id_or_attrib=('id', 'lastupdated', 'updatedby')

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


def model_subs_count(model_sub, model_parent, id):
	return model_sub.select().join(model_parent).where(model_parent.id == id).count()

def add_wheelbrand_links(data, id):
	data['links'] = {
		'wheelmodels': get_sub_link('wheelmodels', 'wheelbrand', id)
	}
	if model_subs_count(Wheelbrandlinks, Wheelbrands, id):
		data['links']['links'] = get_sub_link('wheelbrandlinks', 'wheelbrand', id) 
	return data

def add_wheelmodel_links(data, id):
	data['links'] = {
		'wheelbrand': get_link('wheelbrands', data['wheelbrand']['id']),
	}
	links_ct = model_subs_count(Wheelmodellinks, Wheelmodels, id)
	if links_ct:
		data['links']['links'] = get_sub_link('wheelmodellinks', 'wheelmodel', id)
	photos_ct = model_subs_count(Wheelmodelphotos, Wheelmodels, id)
	if photos_ct:
		data['links']['photos'] = get_sub_link('wheelmodelphotos', 'wheelmodel', id)
	specs_ct = model_subs_count(Wheelspecs, Wheelmodels, id)
	if specs_ct:
		data['links']['specs'] = get_sub_link('wheelspecs', 'wheelmodel', id)
	data = tweak_model_photourl(data)
	return data

def get_sub_link(name, parent, parentid):
	return 'http://%s/%s/%s?%s=%s' % (request.host, api.blueprint.name, name, parent, parentid)

def get_link(name, id):
	return 'http://%s/%s/%s/%s' % (request.host, api.blueprint.name, name, id)

# register our models so they are exposed via /api/<model>/
class UnitResource(RestResource):
	exclude = ('id',)
#api.register(Rides)
#api.register(Ridesphotos)
#api.register(Ridesvehicles)
#api.register(Rideswheels)
#api.register(Tags)
class TaggroupResource(RestResource):
	exclude = no_id_or_attrib
api.register(Taggroup, TaggroupResource, allowed_methods=allowed_verbs)
class TagsResource(RestResource):
	exclude = no_id_or_attrib+('total', )
class TagsgroupResource(RestResource):
	exclude = no_id_or_attrib
class TaggroupsResource(RestResource):
	exclude = no_id_or_attrib
	include_resources = {
		'tag': TagsResource,
		'taggroup': TagsgroupResource
	}
api.register(Tags, TaggroupsResource, allowed_methods=allowed_verbs)
#api.register(Vehiclebrands)
#api.register(Vehiclemodelphotos)
class VehiclebrandsSummaryResource(RestResource):
	exclude = no_id_or_attrib+('url', 'notes',)
	def prepare_data(self, obj, data):
		return tweak_brand_photourl(data)
class VehiclemodelsResource(RestResource):
	include_resources = {
		'vehiclebrand': VehiclebrandsSummaryResource
	}
#api.register(Vehiclemodels, VehiclemodelsResource, allowed_methods=allowed_verbs)

class WheelmodelSummaryResource(RestResource):
	exclude = ('discontinued','lastupdated','mfgspecdate', 'mfgspecurl', 'notes', 'searchterm', 'similar', 'updatedby', 'wheelbrand', 'wheelmfglocation', 'wheelmfgmethod', 'photourl', )

class WheelbrandsResource(RestResource):
	exclude = no_attrib
	def prepare_data(self, obj, data):
		ret = tweak_brand_photourl(data)
		ret = add_wheelbrand_links(data, data['id'])
		return ret
api.register(Wheelbrands, WheelbrandsResource, allowed_methods=allowed_verbs)

class WheelbrandSummaryResource(RestResource):
	exclude = no_attrib+('url', 'notes', 'photourl' )
	def prepare_data(self, obj, data):
		return tweak_brand_photourl(data)

class WheelbrandlinksResource(RestResource):
	include_resources={
		'wheelbrand': WheelbrandSummaryResource,
	}
api.register(Wheelbrandlinks)
#api.register(Wheelmfglocations)
#api.register(Wheelmfgmethods)
class WheelmodellinksResource(RestResource):
	exclude = no_id_or_attrib
	include_resources={
		'wheelmodel': WheelmodelSummaryResource,
	}
api.register(Wheelmodellinks, WheelmodellinksResource, allowed_methods=allowed_verbs)

class WheelmodelphotosResource(RestResource):
	exclude = no_id_or_attrib
	include_resources={
		'wheelmodel': WheelmodelSummaryResource,
	}
api.register(Wheelmodelphotos, WheelmodelphotosResource, allowed_methods=allowed_verbs)

class WheelmfgmethodSummaryResource(RestResource):
	exclude = no_attrib
class WheelmfglocationSummaryResource(RestResource):
	exclude = no_attrib
#class WheelmodelsSimilarResource(RestResource):
#	exclude = ('discontinued','lastupdated','mfgspecdate', 'mfgspecurl', 'notes', 'searchterm', 'similar', 'updatedby', 'wheelbrand', 'wheelmfglocation', 'wheelmfgmethod',)
class WheelmodelsResource(RestResource):
	#delete_recursive = True
	include_resources = {
		'wheelbrand': WheelbrandSummaryResource,
		'wheelmfgmethod': WheelmfgmethodSummaryResource,
		'wheelmfglocation': WheelmfglocationSummaryResource,
#		'similar': WheelmodelsSimilarResource,
	}
	exclude = ('wheelmfglocation', 'searchterm')
	def prepare_data(self, obj, data):
		ret = add_wheelmodel_links(data, data['id'])
		return ret
api.register(Wheelmodels, WheelmodelsResource, allowed_methods=allowed_verbs)

class WheelsizesResource(RestResource):
	exclude = no_id_or_attrib 
	include_resources = {
		'units': UnitResource,
	}
api.register(Wheelsizes, WheelsizesResource, allowed_methods=allowed_verbs)

class WheelfinishesResource(RestResource):
	exclude = no_id_or_attrib
class WheelpcdsResource(RestResource):
	exclude = no_id_or_attrib
api.register(Wheelpcds, WheelpcdsResource, allowed_methods=allowed_verbs)

class WheelspecsResource(RestResource):
	exclude = no_id_or_attrib 
	include_resources = {
		'wheelsize': WheelsizesResource,
		'wheelpcd': WheelpcdsResource,
		'wheelfinish': WheelfinishesResource,
		'wheelmodel': WheelmodelSummaryResource,
	}
api.register(Wheelspecs, WheelspecsResource, allowed_methods=allowed_verbs)

class WheeltagsResource(RestResource):
	exclude = ('updatedby', )
	include_resources = {
		'wheelmodel': WheelmodelSummaryResource,
		'tag': TagsResource,
	}
api.register(Wheeltags, WheeltagsResource, allowed_methods=allowed_verbs)

class GlobalconfigResource(RestResource):
	exclude = no_id_or_attrib
api.register(Globalconfig, GlobalconfigResource, allowed_methods=allowed_verbs)
