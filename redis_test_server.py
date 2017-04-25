import sys
import re

from jsonrpc import JSONRPCResponseManager, dispatcher
from jsonrpc.jsonrpc2 import JSONRPC20Response

from msrestazure.azure_active_directory import ServicePrincipalCredentials

from azure.mgmt.redis import RedisManagementClient

def readinput(enforce_lsp=True):
    try:
        content_length = sys.stdin.readline()
        if enforce_lsp:
            content_length = re.match(r"Content-Length:\s*(\d+)", content_length)
            if not content_length:
                raise ValueError("Content-Length must be used in the Language Protocol")
            content_length = int(content_length.group(1))

        # Skip a line
        sys.stdin.readline()

        json_data = sys.stdin.read()
        if enforce_lsp:
            bytes_json_data = json_data.encode(sys.stdin.encoding)
            if len(bytes_json_data) != content_length:
                raise ValueError("Content-Length does not match ({} vs {})".format(
                    len(bytes_json_data),
                    content_length
                ))
        return json_data
    except Exception as err:
        answer = JSONRPC20Response(error={
            "code": -32600,
            "message": str(err)
        })
        writeoutput(answer.json)
        sys.exit(1)

def writeoutput(data_str):
    data_bytes = data_str.encode("utf8")
    print("Content-Length: {}\r".format(len(data_bytes)))
    print("\r")
    print(data_str)

def auth(**kwargs):
    return ServicePrincipalCredentials(
        client_id = kwargs["__reserved"]["credentials"]["clientId"],
        secret = kwargs["__reserved"]["credentials"]["secret"],
        tenant = kwargs["__reserved"]["credentials"]["tenantId"],
    )

def raw_to_json(response):
    return {
        "statusCode": response.status_code,
        "headers": dict(response.headers),
        "response": response.json()
    }

def redis_create(**kwargs):
    credentials = auth(**kwargs)
    subscription_id = kwargs["subscriptionId"]
    client = RedisManagementClient(credentials, subscription_id)
    raw_answer = client.redis.create(
        kwargs["resourceGroupName"],
        kwargs["name"],
        {
            "sku": {
                "name": kwargs["parameters"]["properties"]["sku"]["name"],
                "family": kwargs["parameters"]["properties"]["sku"]["family"],
                "capacity": kwargs["parameters"]["properties"]["sku"]["capacity"]
            },
            "location": kwargs["parameters"]["location"]
        },
        raw=True
    )
    return raw_to_json(raw_answer.response)

def redis_get(**kwargs):
    credentials = auth(**kwargs)
    subscription_id = kwargs["subscriptionId"]
    client = RedisManagementClient(credentials, subscription_id)
    raw_answer = client.redis.get(
        kwargs["resourceGroupName"],
        kwargs["name"],
        raw=True
    )
    return raw_to_json(raw_answer.response)

def redis_list(**kwargs):
    credentials = auth(**kwargs)
    subscription_id = kwargs["subscriptionId"]
    client = RedisManagementClient(credentials, subscription_id)
    list_iterator = client.redis.list(
    )
    first_page = list_iterator.advance_page()
    return raw_to_json(list_iterator._response)

def mymethod(**kwargs):
    return kwargs


def main(enforce_lsp=True):
    # Dispatcher is dictionary {<method_name>: callable}
    # dispatcher["Server.Operations_List"] = mymethod
    dispatcher["Server.Redis_Create"] = redis_create
    # dispatcher["Server.Redis_Update"] = mymethod
    # dispatcher["Server.Redis_Delete"] = mymethod
    dispatcher["Server.Redis_Get"] = redis_get
    dispatcher["Server.Redis_List"] = redis_list
    # dispatcher["Server.Redis_ListByResourceGroup"] = mymethod

    response = JSONRPCResponseManager.handle(readinput(enforce_lsp), dispatcher)
    writeoutput(response.json)


if __name__ == '__main__':
    main(enforce_lsp="--disable-check" not in sys.argv)