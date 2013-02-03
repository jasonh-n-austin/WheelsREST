from peewee import *
from flask_peewee.auth import BaseUser
import datetime
from app import db

#database = MySQLDatabase('rafarafi_wheels', **{'passwd': 'ktd#433', 'host': 'pragmaticapi.com', 'user': 'rafarafi_admin'})

class UnknownFieldType(object):
    pass

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username

    def gravatar_url(self, size=80):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5(self.email.strip().lower().encode('utf-8')).hexdigest(), size)

class Globalconfig(BaseModel):
    key = CharField()
    value = CharField()

    class Meta:
        db_table = 'globalconfig'

class Rides(BaseModel):
    userid = IntegerField()

    class Meta:
        db_table = 'rides'

class Vehiclebrands(BaseModel):
    description = CharField()
    notes = CharField()

    class Meta:
        db_table = 'vehiclebrands'

class Vehiclemodels(BaseModel):
    description = CharField()
    vehiclebrand = ForeignKeyField(rel_model=Vehiclebrands)

    class Meta:
        db_table = 'vehiclemodels'

class Ridesvehicles(BaseModel):
    lastupdated = DateTimeField()
    rides = ForeignKeyField(rel_model=Rides)
    vehiclemodel = ForeignKeyField(rel_model=Vehiclemodels)
    vehiclemodelspec = CharField()
    vehicleyear = IntegerField()

    class Meta:
        db_table = 'ridesvehicles'

class Ridesnotes(BaseModel):
    item = CharField()
    key = CharField()
    ridesvehicles = ForeignKeyField(rel_model=Ridesvehicles)

    class Meta:
        db_table = 'ridesnotes'

class Wheelbrands(BaseModel):
    description = CharField()
    lastupdated = DateTimeField()
    notes = CharField()
    photourl = CharField()
    updatedby = CharField()
    url = CharField()

    class Meta:
        db_table = 'wheelbrands'

class Wheelmfgmethods(BaseModel):
    id = IntegerField(primary_key=True)
    description = CharField()
    lastupdated = DateTimeField()
    updatedby = CharField()

    class Meta:
        db_table = 'wheelmfgmethods'

class Wheelmfglocations(BaseModel):
    description = CharField()
    lastupdated = DateTimeField()
    notes = CharField()
    updatedby = CharField()

    class Meta:
        db_table = 'wheelmfglocations'

class Wheelmodels(BaseModel):
    description = CharField()
    discontinued = IntegerField()
    lastupdated = DateTimeField()
    mfgspecdate = DateTimeField()
    mfgspecurl = CharField()
    notes = CharField()
    photourl = CharField()
    searchterm = CharField()
    similar = ForeignKeyField(rel_model='self')
    updatedby = CharField()
    wheelbrand = ForeignKeyField(Wheelbrands, related_name='brands')
    wheelmfglocation = ForeignKeyField(rel_model=Wheelmfglocations)
    wheelmfgmethod = ForeignKeyField(rel_model=Wheelmfgmethods)

    class Meta:
        db_table = 'wheelmodels'

class Wheelsizes(BaseModel):
    diameter = FloatField()
    lastupdated = DateTimeField()
    units_id = IntegerField()
    updatedby = CharField()
    width = FloatField()

    class Meta:
        db_table = 'wheelsizes'

class Wheelfinishes(BaseModel):
    description = CharField()
    lastupdated = DateTimeField()
    updatedby = CharField()

    class Meta:
        db_table = 'wheelfinishes'

class Wheelpcds(BaseModel):
    lastupdated = DateTimeField()
    lugs = IntegerField()
    spacing = FloatField()
    units_id = IntegerField()
    updatedby = CharField()

    class Meta:
        db_table = 'wheelpcds'

class Wheelspecs(BaseModel):
    backspacing = FloatField()
    backspacingunits_id = IntegerField()
    centerbore = FloatField()
    centerboreunits_id = IntegerField()
    lastupdated = DateTimeField()
    notes = CharField()
    offset = FloatField()
    offsetunits_id = IntegerField()
    photourl = CharField()
    updatedby = CharField()
    weight = FloatField()
    weightunits_id = IntegerField()
    wheelfinish = ForeignKeyField(rel_model=Wheelfinishes)
    wheelmodel = ForeignKeyField(rel_model=Wheelmodels)
    wheelpcd = ForeignKeyField(rel_model=Wheelpcds)
    wheelsize = ForeignKeyField(rel_model=Wheelsizes)

    class Meta:
        db_table = 'wheelspecs'

class Rideswheels(BaseModel):
    frontrear = IntegerField()
    lastupdated = DateTimeField()
    notes = CharField()
    ridesvehicles = ForeignKeyField(rel_model=Ridesvehicles)
    wheelmodel = ForeignKeyField(rel_model=Wheelmodels)
    wheelspec = ForeignKeyField(rel_model=Wheelspecs)

    class Meta:
        db_table = 'rideswheels'

class Ridesphotos(BaseModel):
    lastupdated = DateTimeField(db_column='lastupdated')
    notes = CharField(db_column='notes')
    frontrideswheels = ForeignKeyField(rel_model=Rideswheels)
    order = IntegerField()
    photourl = CharField()
    primary = IntegerField()
    rearrideswheels = ForeignKeyField(rel_model=Rideswheels)
    ridesvehicles = ForeignKeyField(rel_model=Ridesvehicles)
    status = IntegerField()

    class Meta:
        db_table = 'ridesphotos'

class Taggroup(BaseModel):
    lastupdated = DateTimeField()
    name = CharField()
    updatedby = CharField()

    class Meta:
        db_table = 'taggroup'

class Tags(BaseModel):
    lastupdated = DateTimeField()
    name = CharField()
    total = IntegerField()
    updatedby = CharField()

    class Meta:
        db_table = 'tags'

class Taggroups(BaseModel):
    lastupdated = DateTimeField()
    taggroup = ForeignKeyField(rel_model=Taggroup)
    tag = ForeignKeyField(rel_model=Tags)
    updatedby = CharField()

    class Meta:
        db_table = 'taggroups'

class Vehiclemodelphotos(BaseModel):
    credits = CharField()
    lastupdated = DateTimeField()
    notes = CharField()
    photourl = CharField()
    sort = IntegerField()
    updatedby = CharField()
    wheelmodel = ForeignKeyField(rel_model=Wheelmodels)

    class Meta:
        db_table = 'vehiclemodelphotos'

class Wheelbrandlinks(BaseModel):
    description = CharField()
    lastupdated = DateTimeField()
    updatedby = CharField()
    url = CharField()
    wheelbrand = ForeignKeyField(rel_model=Wheelbrands)

    class Meta:
        db_table = 'wheelbrandlinks'

class Wheelbrandstracking(BaseModel):
    count = IntegerField()
    lastvisited = DateTimeField()
    period = IntegerField()
    wheelbrandid = ForeignKeyField(rel_model=Wheelbrands)

    class Meta:
        db_table = 'wheelbrandstracking'

class Wheelmodellinks(BaseModel):
    description = CharField()
    lastupdated = DateTimeField()
    updatedby = CharField()
    url = CharField()
    wheelmodel = ForeignKeyField(rel_model=Wheelmodels)

    class Meta:
        db_table = 'wheelmodellinks'

class Wheelmodelphotos(BaseModel):
    lastupdated = DateTimeField()
    sort = IntegerField()
    updatedby = CharField()
    url = CharField()
    wheelmodel = ForeignKeyField(rel_model=Wheelmodels)

    class Meta:
        db_table = 'wheelmodelphotos'

class Wheelmodelstracking(BaseModel):
    count = IntegerField()
    lastvisited = DateTimeField()
    period = IntegerField()
    wheelmodelid = ForeignKeyField(rel_model=Wheelmodels)

    class Meta:
        db_table = 'wheelmodelstracking'

class Wheeltags(BaseModel):
    lastupdated = DateTimeField()
    tag = ForeignKeyField(rel_model=Tags)
    updatedby = CharField()
    wheelmodel = ForeignKeyField(rel_model=Wheelmodels)

    class Meta:
        db_table = 'wheeltags'

def create_tables():
    User.create_table()
