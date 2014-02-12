import httplib, urllib
import errno
from socket import error as socket_error

def callrest(domain="", port=80,path="/",type="POST",params={},timeout=30, headers = None):
	connection = False

	try:
		port = int(port)
		connection =  httplib.HTTPConnection(domain, port, timeout=30)
		params = urllib.urlencode(params)

		if type == "POST":
			if not headers:
				headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "*/*"}
			connection.request('POST', path, params, headers=headers)

		if type == "GET":
			if not headers:
				headers = {}
			connection.request('GET', path+'?%s' % params, headers=headers)

		if type == "PUT":
			if not headers:
				headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "*/*"}
			connection.request('PUT', path+'?%s' % params, headers=headers)

		result = connection.getresponse()
		return (result.status,result.reason,result.read())

	except socket_error, e:
		if e.errno != errno.ECONNREFUSED:
			return (500,"Internal Error",None)
		else:
			return (None, "Connection refused", None)
	except Exception, e:
		return (500,"Internal Error",None)
	finally:
		if connection:
			connection.close()

	return (500,"Internal Error",None)