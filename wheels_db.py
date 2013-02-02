from flask import g
import sqlite3

DATABASE = 'wheels.db'

BRANDS_QUERY = '''
	select WheelBrandID, WheelBrandDescription, WheelBrandURL, WheelBrandPhotoURL, 
	WheelBrandNotes, LastUpdated, UpdatedBy
	from wheelbrands wb
	'''
BRANDS_ORDER = 'order by wb.WheelBrandDescription'

MODELS_QUERY = '''
	select wb.WheelBrandID, wb.WheelBrandDescription, wm.WheelModelID, 
	wm.WheelModelDescription 
	from wheelmodels wm 
	inner join wheelbrands wb on wm.WheelBrandID = wb.WheelBrandID
	'''
MODELS_ORDER = ' order by wb.WheelBrandDescription, wm.WheelModelDescription'


def close():
	if hasattr(g, 'db'):
		g.db.close()

def connect():
	g.db = sqlite3.connect(DATABASE)

def query_db(query, args=(), one=False):
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value)
			for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv

def brands_all():
	return query_db(BRANDS_QUERY + BRANDS_ORDER);

def brands_by_brand(brand):
	return query_db(BRANDS_QUERY + " where WheelBrandDescription = ? " + BRANDS_ORDER, (brand,), one=True);

def brands_by_id(brandid):
	return query_db(BRANDS_QUERY + " where WheelBrandID = ? " + BRANDS_ORDER, (brandid,), one=True);

def models_all():
	return query_db(MODELS_QUERY + MODELS_ORDER)

def models_by_brand(brand):
	return query_db(MODELS_QUERY + " where wb.WheelBrandDescription = ?" + MODELS_ORDER, (brand,) );

def models_by_id(id):
	return query_db(MODELS_QUERY + " where wm.WheelModelID = ?" + MODELS_ORDER, (id, ), one=True)