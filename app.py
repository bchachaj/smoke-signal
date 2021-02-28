import sys
import scry

print('loading function')

def main(): 
    Scry = scry.init()
    return "params"


def handler():
    main()
    return 'Hello from AWS Lambda using Python' + sys.version + '!' 

# setup only
handler()

