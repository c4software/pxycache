import httplib, urllib

def callrest(domain="", port=80,path="/",type="POST",params={},timeout=30):
	connection = False

	try:
		port = int(port)
		connection =  httplib.HTTPConnection(domain, port, timeout=30)
		params = urllib.urlencode(params)

		if type == "POST":
			headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
			connection.request('POST', path, params, headers=headers)

		if type == "GET":
			headers = {}
			connection.request('GET', path+'?%s' % params, headers=headers)

		if type == "PUT":
			headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
			connection.request('PUT', path+'?%s' % params, headers=headers)

		result = connection.getresponse()
		return (result.status,result.reason,result.read())

	except Exception, e:
		print e
		return (500,"Internal Error",None)
	finally:
		if connection:
			connection.close()

	return (500,"Internal Error",None)