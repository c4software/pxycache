pxyCache
========

PxyCache is a simple Proxy, With offline capacities. pxyCache also provide an Admin Panel to see and manage the cache of the "Proxy".

The term « Proxy » means all request you made (GET, POST) on http://localhost:5000/ are automaticaly send to the real server you have config.

I made this tool to be less dependent from the Back Office in the developpement process. I can work even if the Back office became unavailable.

## Todo
- Make headers « stubbable » from the interface.

## Usage

1. Start the « Proxy ».
2. Acces to http://localhost:5000/ its automatically call the equivalent in the real server.
3. Manage your proxy => http://localhost:5000/api_proxy/
4. Profit!

### Start the "Proxy" in online state
its mean its serve the content of the __real domain__

```bash
python2 serve.py --realdomain yourdomain.tld --realport 80 --cachepath "/tmp/cache" --online
```

### Start the "Proxy" in offline state
its mean its serve the content from your __local cache__ _if exist_

```bash
python2 serve.py --realdomain yourdomain.tld --realport 80 --cachepath "/tmp/cache" --offline
```

### State of the proxy

If the real domain became unavailable during the execution, the proxy will automatically switch in offline state for the request and serve the cached data if available.


## Manage pxyCache

Management can be done via curl call, or most simply with the Interface.

Url to acces it : http://localhost:5000/api_proxy/

![Management Interface](./api_proxy/static/pxyCache.png "Management Interface") 
