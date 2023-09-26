import json
import requests



def send_message(msg):

    payload = {

                    "sender": "user1",
                    "message": msg
                }
    print("Payload done")
    r = requests.post('https://0ed6-185-127-125-57.ngrok.io/webhooks/rest/webhook', json=payload)
    print("Request done")
    if r.status_code != 200:
        print("reponse non valid du serveur")
    elif len(r.text)==0:
        print("response is empty")
    else:
        data = r.json()    #response from raza chatbot
        #print(type(data))
       
        # Process the response from the Rasa chatbot
        for message in data:
            print("the message to my questions is"+" "+message["text"])
            response = message["text"]
            return response
    
    
    

