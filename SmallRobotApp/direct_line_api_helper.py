
import json
import  requests
class DirectLineAPI(object):
    def __init__(self, direct_line_secret):
        self.direct_line_secret = direct_line_secret
        self.base_url = 'https://directline.botframework.com/v3/directline'
        self.headers = self.set_headers()
        self.last_message_id = None
        self.response = None

    def set_headers(self):
        headers = {'Content-Type': 'application/json'}
        value = ' '.join(['Bearer', self.direct_line_secret])
        headers.update({'Authorization': value})
        return headers

    def start_conversation(self):
        url = '/'.join([self.base_url, 'conversations'])
        bot_response = requests.post(url, headers=self.headers)
        json_response = bot_response.json()

        if 'error' in json_response:
            print("Conversation ID not available [request failed]")
            return None
        else:
            print("succed")
            self.conversationid = json_response['conversationId']
            return self.conversationid

    def send_message(self, text):
        print("Entered send message")
        print(self.conversationid)
        url = '/'.join([self.base_url, 'conversations', self.conversationid, 'activities'])
        text = json.dumps(text)
        json_payload = {
            'locale': 'en-EN',
            'type': 'message',
            'from': {'id': 'user1'},
            'text': text
        }
        print(url,json_payload)
        bot_response = requests.post(url, headers=self.headers, json=json_payload)
        print(bot_response)
        if bot_response.status_code == 200:
            print("success send message")
            return "message sent"
        return "error contacting bot"

    def get_messages(self):
        url = '/'.join([self.base_url, 'conversations', self.conversationid, 'activities'])
        bot_response = requests.get(url, headers=self.headers)
        if bot_response.status_code == 200:
            json_response = bot_response.json()
            self.response = json_response['activities'][-1]['text']
            data = json.loads(self.response)
            data['inputHint'] = json_response['activities'][-1]['inputHint']
            return data
        else:
            print("Error contacting bot for response")