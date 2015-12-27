
from flask import Flask, request
import pprint
import sys
import json
from question1 import get_listing  
from question2 import get_stats

app = Flask(__name__)

@app.route('/dataset/common_stats/',methods=['POST'])
def get_common_stats():
    if request.headers['Content-Type'] == 'application/json':
        try:
            city = request.get_json(force=True)['city']
            state = request.get_json(force=True)['state']
            beds = request.get_json(force=True)['beds']
            return get_stats(city, state, beds)            
        except KeyError as e:
            return ('Missing %s in input\n'%str(e))
        except:
            return ('Get common stats failed: %s\n'%str(e))
    else:
        return "Only json content-type accepted"




if __name__ == '__main__':

    if (len(sys.argv)>1):
        get_listing(*(sys.argv[1:])) 
    else:
        app.run()
    
