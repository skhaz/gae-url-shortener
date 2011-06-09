
"""
http://en.wikipedia.org/wiki/Base_36
"""

def b36encode(number, alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
	if not isinstance(number, (int, long)):
		raise TypeError('number must be an integer')
	
	if number == 0:
		return '0'
	
	base36 = ''
	
	sign   = ""
	if number < 0:
		sign  ='-'
		number=-number
	
	while number != 0:
		number, i = divmod(number, len(alphabet))
		base36 = alphabet[i] + base36
	
	return sign + base36

