import RazaBot
import socket
import json
# from concurrent.futures import ThreadPoolExecutor

def checkForSwitch(msg):
    print("function chechk language")

    keyword_list = ["change", "talk", "switch"]
    keyword_list_arabic = ["حول", "غير", "احكي", "تكلم"]
    words = msg.lower().split()
    print("check for switch")

    if "انجليزي" in words :
        for keyword in keyword_list_arabic:
            if keyword in words:
                print("Switching to English")
                lang = "en-IN"
                return lang
        print("No action needed for English")
        return None
    elif "arabic" in words:
        for keyword in keyword_list:
            if keyword in words:
                print("Switching to Arabic")
                lang = "ar-XA"
                return lang
        print("No action needed for Arabic")
        return None
    else:
        print("No action needed")
        return None   
    
def main(x):
    global expecting_input_detection

    print("THE MESSAGE SENT IS",x)

    
    print("recieving the message")
    response1 = RazaBot.send_message(x)
    print('after Razabot and send message')
   
    try:

        data=json.loads(response1)
        print(type(data))
        print("la chaine est un objet json valide")
        gpt_response=data["gpt_response"]
        #print("the gpt response is:"+gpt_response)
        return gpt_response
    except json.JSONDecodeError as e:
        print("la chaine n est pas json")
        return response1
           

        
        
        
