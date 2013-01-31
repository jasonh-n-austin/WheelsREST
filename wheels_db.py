from flask import g
import sqlite3

DATABASE = 'wheels.db'

MODELS_QUERY = '''
		select wb.WheelBrandID, wb.WheelBrandDescription, wm.WheelModelID, 
		wm.WheelModelDescription 
		from wheelmodels wm 
		inner join wheelbrands wb on wm.WheelBrandID = wb.WheelBrandID
		'''


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


def models_all():
	return query_db(MODELS_QUERY)

def models_by_brand(brand):
	query = MODELS_QUERY + "where wb.WheelBrandDescription = ?" 
	return query_db(query, (brand,))

def models_by_id(id):
	return query_db(MODELS_QUERY+' where wm.WheelModelID = ?', (id, ), one=True)