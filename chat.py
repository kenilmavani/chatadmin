#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("queryResult").get("action") != "year_detail":
        return {}
    result = req.get("queryResult")
    parameters = result.get("parameters")
    zone = (parameters.get("be_year"))
    print(zone)
    cost = {'1st':'50000', '2nd':'47000', '3rd':'46000', '4th':'45000'}    
    speech = "fees of year "+str(result.get("queryText")) + " is " + str(cost[str(zone[0])])
    print(speech)
    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [
            {
            "text": {   
                "text": [speech]
            }
            }
        ],
        #"data": {},
        #"contextOut": [],
        "source": "SCET-BOTT"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
