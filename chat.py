#!/usr/bin/env python

import urllib
import json
import os
from flask import request
from flask import make_response
from flask import Flask, request, jsonify, render_template    
import dialogflow
import requests
import json
import pusher

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def detect_intent_texts(project_id, session_id, text, language_code):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        if text:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)
            query_input = dialogflow.types.QueryInput(text=text_input)
            response = session_client.detect_intent(
                session=session, query_input=query_input)

            return response.query_result.fulfillment_text
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }

    return jsonify(response_text)

def makeWebhookResult(req):
    if req.get("queryResult").get("action") == "accurate_be_year_detail":
        result = req.get("queryResult")
        parameters = result.get("parameters")
        zone = (parameters.get("be_year"))
        print(zone)
        cost = {'1st':'50000', '2nd':'47000', '3rd':'46000', '4th':'45000'}    
        if isinstance(zone, list):            
            speech = "fees of bachelor's "+ result.get("queryText") + " year is " + str(cost[str(zone[0])])            
        else:
            speech = "fees of  bachelor's "+ zone + " year is " + str(cost[str(zone)])          

    elif req.get("queryResult").get("action") == "accurate_me_year_detail":
        result = req.get("queryResult")
        parameters = result.get("parameters")
        zone = (parameters.get("be_year"))
        print(zone)
        cost = {'1st':'50000', '2nd':'47000'}   
        if isinstance(zone, list):            
            speech = "fees of master's "+ result.get("queryText") + " year is " + str(cost[str(zone[0])])            
        else:
            if(zone in cost): speech = "fees of  master's "+ zone + " year is " + str(cost[str(zone)])  
            else : speech = "Enter valid year"

    
    elif req.get("queryResult").get("action") == "accurate:exam:form:bachelors":
        result = req.get("queryResult")
        parameters = result.get("parameters")
        zone = (parameters.get("be_year"))
        cost = {'1st':'18/8/2017', '2nd':'26/9/2016', '3rd':'10/9/2019', '4th':'19/10/2018'} 
        if isinstance(zone, list):           
            speech = "Exam form of "+ result.get("queryText")  + " year BE will arrive on " + str(cost[str(zone[0])])
        else : speech = "Exam form of "+ zone + " year BE will arrive on " + str(cost[str(zone)])
    elif req.get("queryResult").get("action") == "accurate:exam:form:masters":
        result = req.get("queryResult")
        parameters = result.get("parameters")
        zone = (parameters.get("be_year"))         
        cost = {'1st':'20/7/2017', '2nd':'1/9/2016'}    
        if isinstance(zone, list):           
            speech = "Exam form of "+ result.get("queryText") + " year ME will arrive on " + str(cost[str(zone[0])])
        else : speech = "Exam form of "+ zone + " year ME will arrive on " + str(cost[str(zone)])
    elif req.get("queryResult").get("action") == "fees:last_day":               
        result = req.get("queryResult")
        speech = "pay fee before 2/5/2019" 
    elif req.get("queryResult").get("action") == "how:pay:fees":
        result = req.get("queryResult")
        speech = "here is the payment link of fees" 
    elif req.get("queryResult").get("action") == "input.unknown":
        speech = "Answer will be added soon try anoher questions"
        file = open('abc.txt','a+')
        file.write('"'+req.get("queryResult").get("queryText")+'",\n')    
        file.close()                                         
    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [
            {
            "text": {   
                "text": [speech]
            }   
            }
        ],
        "source": "SCET-BOTT"
    }

if __name__ == "__main__":
        app.run()
