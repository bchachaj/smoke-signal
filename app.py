import sys
import json
import logging
from scry import scry

print('loading function')

def main(event): 
    scry()
    return {
        "statusCode": 200, 
        "body": json.dumps('successful request')
    }


def handler(event, context):
    print(event)
    payload = main(event)
    return payload 


main("hi")