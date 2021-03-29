import sys
import json
import logging
from scry import scry

print('loading function')

def main(event): 

        # routed through API gateway
    if event.get('body') != None:
        req = json.loads(event["body"])
        key = req["keyword"]
        sub = req["subreddit"]
    else: 
        # lambda test response
        req = event 
        key = req["keyword"]
        sub = req["subreddit"]

    try: 
        if len(key) < 3: 
            return {
                "statusCode": 400, 
                "body": "a keyword of at least 3 letters is required"
            }
        scored_entries = scry(key, sub)
        
        return {
            "statusCode": 200, 
            "body": json.dumps(scored_entries)
        }

    except Exception as e:
        print('Error', e)
        return {
            "statusCode": 500, 
        }


def handler(event, context):
    print(event)
    payload = main(event)
    return payload 


