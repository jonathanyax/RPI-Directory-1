from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import cgi
import re
import webapp2
import string

from google.appengine.ext import blobstore
from google.appengine.ext import db

from google.appengine.ext.webapp import blobstore_handlers

from mapreduce.lib import files
from google.appengine.api import taskqueue
from google.appengine.api import users

from mapreduce import base_handler
from mapreduce import mapreduce_pipeline
from mapreduce import operation as op
from mapreduce import shuffler

from models import Person
from models import SuggestObject
from models import StatsObject

from datetime import datetime

#to store the dates of the user
personDateAttributes = [
	'email',
	'first_name',
	'prefered_name',
	'middle_name',
	'rcsid',
	'last_name',
	'date_crawl',
	'date_second_crawl',
	'three_months_passed'
]

class Reaper(webapp2.RequestHandler):
	def mark_three_months(self):
		person = Person.get_by_id(rcsid)
		first_crawl = Person.date_crawl
		secnod_crawl = Person.second_crawl
		if (((secnod_crawl.year - first_crawl.year) * 12) + (first_crawl.month - secnod_crawl.month)) >= 3:
			Person.three_months_passed == True

