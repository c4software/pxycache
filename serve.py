import json
import shutil
import hashlib
import argparse
import logging
import os

from extended_BaseHTTPServer import serve,route,redirect, override
from rest import callrest
import param

logging.basicConfig(level=logging.INFO, format="%(message)s")

def get_path(elem):
	hash_dict = hashlib.md5(json.dumps(elem)).hexdigest()
	# hash_dict = base64.b64encode(json.dumps(elem))
	return "{0}{1}".format(param.params['cache_path'], hash_dict)

# Populate the json of all cached url.
def saveCacheHistory(elem):
	param.params['inCache'][elem[0]] = elem
	path_file = "{0}{1}".format(param.params['cache_path'], "cacheHistory.json")
	with open(path_file, 'w') as f:
		f.write(json.dumps(param.params['inCache']))
	f.close()

def initCacheHistory():
	try:
		path_file = "{0}{1}".format(param.params['cache_path'], "cacheHistory.json")
		with open(path_file, 'r') as f:
			param.params['inCache'] = json.loads(f.read())
		f.close()
	except Exception, e:
		logging.error("Cache history can't be loaded. ({0})".format(e))


def save_return(elem, ret, ret_headers):
	path_file = get_path(elem)
	logging.info("WRITE CACHE {0}".format(path_file))
	data = {"ret": ret, "ret_headers": ret_headers, "extra": elem}
	with open(path_file, 'w') as f:
		f.write(json.dumps(data))
	f.close()

	saveCacheHistory(elem)

def get_return(elem):
	path_file = get_path(elem)
	try:
		ret = ""
		with open(path_file, 'r') as f:
			ret = json.loads(f.read())
		f.close()
		logging.info("READ CACHE {0}".format(path_file))
		return ret
	except:
		logging.info("NOT CACHE {0}".format(path_file))
		raise Exception("Not Available.")

def change_state(state):
	param.online = state

@override("404")
def handler(o, arguments, action, headers):
	ret = ""
	arguments = prepare_args(arguments)

	if param.params['online']:
		ret = callrest(domain=param.params['real_domain'], port=param.params['real_port'], path=o.path, type=action,params=arguments,timeout=30, headers=headers)
		if not ret[0]:
			# Server Not available, serve from cache (if available).
			logging.info("Server not available : Read from cache.")
			return build_response_from_cache(o, arguments, action, headers)
		elif ret[0] == 200:
			save_return([o.path, arguments, action, headers], ret[2], ret[3])
		else:
			logging.info('Got {0} from the server, not an error but...'.format(ret[0]))

		code = int(ret[0])
		return_headers = ret[3]
		ret = ret[2]
		ret = {"content": ret, "code": code}
		return dict(ret.items()+return_headers.items())
	else:
		return build_response_from_cache(o, arguments, action, headers)

def build_response_from_cache(o, arguments, action, headers):
	try:
		ret 		= get_return([o.path, arguments, action, headers])
		extra 		= ret.get("extra", [o.path, arguments, action, {}])
		ret_headers = ret.get("ret_headers", {})
		ret 		= {"content":ret.get("ret", ret),"code":200}
		ret 		= dict(ret.items()+ret_headers.items())
		return ret
	except:
		return {"content":"Not Available","code":404}

def prepare_args(arguments):
	for argument in arguments:
		arguments[argument] = arguments[argument].pop()
	return arguments

def get_template(file):
	with open("template/{0}".format(file)) as f:
		return f.read()
	return ""

@route("/api_proxy")
@route("/api_proxy/")
def api_index():
	return redirect("/api_proxy/index.html")

@route("/api_proxy/getCacheData")
def internal_getCacheData():
	inCache = param.params['inCache']
	return json.dumps([inCache[f] for f in inCache])

@route("/api_proxy/state")
def internal_state():
	if param.params['online']:
		return "Online"
	else:
		return "Offline"

@route("/api_proxy/online")
def internal_online():
	param.params['online'] = True
	return redirect("/api_proxy/index.html")

@route("/api_proxy/offline")
def internal_offline():
	param.params['online'] = False
	return redirect("/api_proxy/index.html")

@route("/api_proxy/cache_it", ["POST"])
def cache_it(**args):
	args = prepare_args(args)
	if "arguments" in args:
		from urlparse import parse_qs
		arguments = prepare_args(parse_qs(args.get("arguments")))
	else:
		arguments = {}

	save_return([args.get("path", ""), arguments, args.get("action", "")], args.get("data","").encode("utf-8"))
	return redirect("/api_proxy/index.html")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='API Proxy')
	parser.add_argument('--port', default=5000, type=int, help='Listen port of the proxy (default 5000)')
	parser.add_argument('--realdomain', type=str, required=True, help='Real domain of the targeted API')
	parser.add_argument('--realport', type=int, required=True, help='Real port of the targeted API')
	parser.add_argument('--cachepath', type=str, required=True, help='Target folder for cache (used when the system is in offline mode, ex: /tmp/api/) ')
	parser.add_argument('--offline' ,action='store_true', help='Put the proxy in the offline mode')
	parser.add_argument('--online' ,action='store_true', help='Put the proxy in the online mode')
	args = parser.parse_args()

	if args.cachepath[-1] != "/":
		args.cachepath = args.cachepath+"/"

	if not os.path.exists(args.cachepath):
		os.makedirs(args.cachepath)

	param.params['real_domain'] = args.realdomain
	param.params['real_port'] = args.realport
	param.params['cache_path'] = args.cachepath
	if args.offline:
		param.params['online'] = False
	if args.online:
		param.params['online'] = True

	initCacheHistory()

	logging.info("Server listen 0.0.0.0:{0} => {1}:{2}".format(args.port, args.realdomain, args.realport))
	serve(ip="0.0.0.0", port=args.port)
