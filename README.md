pxycache
========

PxyCache is a simple Proxy, With offline capacities.

## Usage


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

### Change the state during the execution of the proxy.

#### Put Online

```bash
curl http://localhost:5000/api_proxy/online
```

#### Put Offline

```bash
curl http://localhost:5000/api_proxy/offline
```