import urllib
from django import template

register = template.Library()

@register.simple_tag
def qrcode(data, size = 150):
	url = "http://chart.apis.google.com/chart?"
	url += urllib.urlencode({
		'chl' : data,
		'cht' : 'qr',
		'chs' : str(size),
		'choe' : 'UTF-8'
	})

	return """<img src="%s" width="%s" height="%s" alt="QR Code" border="0" />""" % (url, size, size)

