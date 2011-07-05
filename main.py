#!/usr/bin/env python

import os
from base36 import b36encode
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms


template.register_template_library('qrcode')

class Url(db.Model):
	original = db.StringProperty(required=True)
	shortened = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class UrlForm(djangoforms.ModelForm):
	class Meta:
		model = Url
		exclude = ['shortened', 'date']

class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write('<html><body><center>'
								'<form method="POST" '
								'action="/">'
								'<table>')
		self.response.out.write(UrlForm())
		self.response.out.write('</table>'
								'<input type="submit">'
								'</form></center></body></html>')

	def post(self):
		data = UrlForm(data=self.request.POST)
		if data.is_valid():
			original = self.request.get('original')

			url = Url(original=original)
			id = url.put().id()
			shortened = b36encode(id)
			url.shortened = shortened
			url.put()

			values = {
				'original' : original,
				'shortened': shortened,
			}

			path = os.path.join(os.path.dirname(__file__), 'index.html')
			self.response.out.write(template.render(path, values))

class RedirecHandler(webapp.RequestHandler):
	def get(self, shortened):
		url = db.Query(Url).filter("shortened =", shortened).get()
		if not url:
			self.response.out.write('not found')
		else:
			self.redirect(url.original)

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('/(.*)', RedirecHandler),
	], debug=True)

	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()

