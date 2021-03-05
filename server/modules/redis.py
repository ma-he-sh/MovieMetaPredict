import redis
from config import APP_CONFIG

"""
Handle redis connections for the site, allow to set, update and delete
This file is been used by rq_worker for handling the works jobs
"""

class REDIS():
	def __init__(self):
		self.rd = redis.Redis(host=APP_CONFIG['REDIS']['REDIS_HOST'], port=APP_CONFIG['REDIS']['REDIS_PORT'], password=APP_CONFIG['REDIS']['REDIS_PASS'])

	def conn(self):
		return self.rd

	def set_key( self, key, value ):
		self.rd.set( key, value )

	def get_key( self, key ):
		return self.rd.get( key ).decode("UTF-8")