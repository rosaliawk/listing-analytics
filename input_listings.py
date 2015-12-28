
from flask import Flask, request
import pprint
import sys
import json
from question1 import get_listing  
from question2 import get_stats

app = Flask(__name__)

@app.route('/')
def hello():
    return 'For common stats, send request to /dataset/common_stats/ with city, state and beds specfied\n'

@app.route('/dataset/common_stats/',methods=['GET','POST'])
def get_common_stats():
    if request.headers['Content-Type'] == 'application/json':
        try:
            city = request.get_json(force=True)['city']
            state = request.get_json(force=True)['state']
            beds = request.get_json(force=True)['beds']
            return get_stats(city, state, beds)            
        except KeyError as e:
            print ('Missing %s in input\n'%str(e))
            return ('Missing %s in input\n'%str(e))
        except TypeError as e:
            print ('Get common stats failed: %s\n'%str(e))
            return ('Get common stats failed: %s\n'%str(e))
        except ValueError as e:
            print ('Get common stats failed: %s\n'%str(e))
            return ('Get common stats failed: %s\n'%str(e))
        except:
            print ('Get common stats failed\n')
            return ('Get common stats failed\n')
    else:
        print ("Only json content-type accepted\n")
        return "Only json content-type accepted\n"




if __name__ == "__main__":
    if (len(sys.argv)>1):
        get_listing(*(sys.argv[1:])) 
    else:
        app.run(host='0.0.0.0') 
    
