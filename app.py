import sys
import json
import logging
from scry import scry

print('loading function')

def main(event): 
    scored_entries = scry("GME", "wallstreetbets")
    print(scored_entries)
    return {
        "statusCode": 200, 
        "body": scored_entries
    }


def handler(event, context):
    print(event)
    payload = main(event)
    return payload 

