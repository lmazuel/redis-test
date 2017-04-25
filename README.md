# Redis auto-generated test - proof-of-concept

## Prerequisite

Examples on Windows, but can be easily adapted to Ubuntu or Mac.

- Use Python >= 3.5 (to simplify the next steps)
- Create an local execution environment (called virtual environment)

```console
    > py -3.5 -m venv testingpyenv
```
    
- You should now have Python 3.5 local environment:

```console
    > .\testingpyenv\Scripts\python.exe --version
    Python 3.5.1
```

- Update the package management system

```console
     > .\testingpyenv\Scripts\python.exe -m pip install -U pip setuptools
     Successfully installed appdirs-1.4.3 packaging-16.8 pip-9.0.1 pyparsing-2.2.0 setuptools-35.0.1 six-1.10.0
```

- Install the dependencies

```console
    > .\testingpyenv\Scripts\python.exe -m pip install -r requirements.txt
    Successfully installed PyJWT-1.5.0 adal-0.4.5 asn1crypto-0.22.0 azure-common-1.1.5 azure-mgmt-nspkg-2.0.0 azure-mgmt-redis-4.1.0 azure-nspkg-2.0.0 certifi-2017.4.17 cffi-1.10.0 cryptography-1.8.1 idna-2.5 isodate-0.5.4 json-rpc-1.10.3 keyring-10.3.2 msrest-0.4.7 msrestazure-0.4.7 oauthlib-2.0.2 pycparser-2.17 python-dateutil-2.6.0 pywin32-ctypes-0.0.1 requests-2.13.0 requests-oauthlib-0.8.0
```

## Using the script

The basic command is:

```console
     > .\testingpyenv\Scripts\python.exe .\redis_test_server.py
```
- Output is in stdout. Stderr might be used by Python for error messages.
- The `--disable-check` option will disable the `Content-Length` check (could be useful for testing if like me you want to send files you write manually to stdin).

Example of test with my input in a file in PowerShell:

```console
     > Get-Content D:\redis_list_in.txt | python .\redis_test_server.py --disable-check
Content-Length: 1442

{"result": {"statusCode": 200, "headers": {"Cache-Control": "no-cache", "Pragma": "no-cache", "Transfer-Encoding": "chunked", "Content-Type": "application/json; charset=utf-8", "Content-Encoding": "gzip", "Expires": "-1", "Vary": "Accept-Encoding", "x-ms-request-id": "54fedc13-5755-46fc-af95-cf2984257b5d", "x-rp-server-mvid": "5a0a88c0-0183-48c7-85e3-df64396b7fab", "Strict-Transport-Security": "max-age=31536000; includeSubDomains", "Server": "Microsoft-HTTPAPI/2.0", "x-ms-ratelimit-remaining-subscription-reads": "14998", "x-ms-correlation-request-id": "1b43ef65-1b9c-4e78-9267-cb445524d971", "x-ms-routing-request-id": "WESTUS2:20170425T202558Z:1b43ef65-1b9c-4e78-9267-cb445524d971", "Date": "Tue, 25 Apr 2017 20:25:57 GMT"}, "response": {"value": [{"id": "/subscriptions//resourceGroups/TestRedisAutomatic/providers/Microsoft.Cache/Redis/accountname", "location": "West US", "name": "accountname", "type": "Microsoft.Cache/Redis", "tags": {}, "properties": {"provisioningState": "Succeeded", "redisVersion": "3.2", "sku": {"name": "Premium", "family": "P", "capacity": 1}, "enableNonSslPort": false, "redisConfiguration": {"maxclients": "7500", "maxmemory-reserved": "200", "maxfragmentationmemory-reserved": "300", "maxmemory-delta": "200"}, "accessKeys": null, "hostName": "accountname.redis.cache.windows.net", "port": 6379, "sslPort": 6380}}]}}, "id": "0", "jsonrpc": "2.0"}
```


