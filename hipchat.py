import requests
import json

HIPCHAT_API_ENDPOINT = 'https://api.hipchat.com'
HIPCHAT_API_VERSION = 'v2'


class Notification:
    """This is the notification object to send to the HipChat API"""
    
    max_message_length = 10000
    color_list = ['yellow','green', 'red', 'purple', 'gray', 'random']
    message_formats = ['text', 'html']
    
    def __init__(self, message=None, color='purple', notify=False, message_format='text', debug=True):
        if message is None or len(message) <= 0:
            raise Exception("You must provide a message to send!")
        if len(message) > Notification.max_message_length:
            raise Exception("Your message must be less than {} characters".format(Notification.max_message_length))
        if color not in Notification.color_list:
            raise Exception('{} is not a valid color.\ncolor must be one of the following: {}'.format(color, ', '.join(map(str, Notification.color_list))))
        if message_format not in Notification.message_formats:
            raise Exception('{} is not a valid message_format.\nmessage_format must be one of the following: {}'.format(message_format, ', '.join(map(str, Notification.message_formats))))

        self.message = message
        self.message_format = message_format
        self.notify = notify
        self.color = color
        self.debug = debug

    def debug_msg(self,message):
        if self.debug:
            print message

    def test(self):
        for attr in dir(self):
            print '{}.{} = {}'.format(self.__class__.__name__, attr, getattr(self, attr))

class API:
    """this is the HipChat API object that will send your notifications"""
    
    room_length = 100
    notification_url = HIPCHAT_API_ENDPOINT+'/'+HIPCHAT_API_VERSION+'/room/{}/notification'
    headers = {'content-type': 'application/json'}

    def __init__(self, auth_token=None, room=None, debug=True):
        if auth_token is None or len(auth_token) <= 0:
            raise Exception('You must provide an auth_token!')
        if room is None or len(room) <= 0:
            raise Exception('You must provide a room!')
        if len(room) > API.room_length:
            raise Exception('room must be less than {} characters'.format(API.room_length))

        self.debug = debug
        self.auth_token = auth_token
        self.room = room
        self.base_url = HIPCHAT_API_ENDPOINT+'/'+HIPCHAT_API_VERSION+'/room/{room_id}/{method}'+'?auth_token={token}'.format(token=self.auth_token)
        self.notification_url = API.notification_url.format(self.room)+'?auth_token={}'.format(self.auth_token)

    def test(self):
        """ just prints out the class attributes"""
        for attr in dir(self):
            print '{}.{} = {}'.format(self.__class__.__name__, attr, getattr(self, attr))

    def post_notification(self, notification=None):
        """ 
        Posts a notification to a room
        """
        if notification is None:
            raise Exception('You must provide a notification to send!')

        self.debug_msg('Attempting to post notification: \n{}\nTo room:\n{}'.format(vars(notification),self.notification_url))
        r = requests.post(self.notification_url, data=json.dumps(vars(notification)),headers=self.headers)
        self.debug_msg(str(r.status_code)+'\n'+r.text)

    def debug_msg(self,message):
        if self.debug:
            print message

    def get_rooms(self):
        """Returns dictionary of available rooms for your auth_token"""
        url = HIPCHAT_API_ENDPOINT+'/'+HIPCHAT_API_VERSION+'/room'+'?auth_token={}'.format(self.auth_token)
        r = requests.get(url)
        if r.status_code is 200:
            rooms = {}
            for i in dict(r.json())['items']:
                rooms[i['id']] = i['name']
            return rooms
        else:
            raise Exception('Received unexpected response code: {}\n{}'.format(r.status_code, r.text))

    def set_topic(self, topic=None, room=None):
        """Sets the topic in a room"""
        
        if topic is None or type(topic) is not str or len(topic) > 250:
            raise Exception('Invalid topic: {}\nTopics must be a string of between 0 and 250 characters'.format(topic))
        
        if room is not None:
            url = self.base_url.format(room_id=room, method='topic')
        else:    
            url = self.base_url.format(room_id=self.room, method='topic')

        self.debug_msg('Setting topic: {}\n{}'.format(topic, url))
        body = json.dumps({'topic':topic})
        
        r = requests.put(url, data=body, headers=self.headers)
        
        if r.status_code != 204:
            raise Exception('Received unexpected status_code: {}\n{}'.format(r.status_code, r.text))
        
        self.debug_msg('{}\n{}'.format(r.status_code,r.text))

if __name__ == '__main__':
    api = API(room="Your room_id", auth_token="Your auth_token", debug=True)