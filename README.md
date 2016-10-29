
**[EXPERIMENTAL]** Create Lets Encrypt Certificates with
[acme.sh](https://github.com/Neilpang/acme.sh)
and [inwx.de](https://www.inwx.de/) [API](https://github.com/inwx/python2.7-client) via DNS Challenge Validation.

## Installation

```
cp inwxcredentials.py.skel inwxcredentials.py
nano inwxcredentials.py # Your login inwx data
ln -s ~/letsencrypt-acme.sh-inwx/dns_inwx.sh ~/.acme.sh/dns_inwx.sh
```

## Use it

```
./acme.sh --issue --dns dns_inwx -d some.awesome.example.com
```

## Files

* `inwx.py` API lib by inwx.de
* `acme-inwx.py` acme.sh plugin
* `dns_inwx.sh` wrapper for acme.sh
* `inwxcredentials.py.skel` inwx Credentials

## API Code by inwx

https://github.com/inwx/python2.7-client

