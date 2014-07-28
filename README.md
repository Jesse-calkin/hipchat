# hipchat

A partial implementation of the HipChat v2 API in Python

## Dependencies

You'll need to have the [Requests](http://docs.python-requests.org/en/latest/) module and be able to [authenticate](https://www.hipchat.com/docs/apiv2/auth) with the HipChat v2 API

## Examples

### Posting a Notification
```python
import hipchat
 
ROOM = '8675309'
token = '9b4f2a8c9db85063c5b8a5307f29a15d'
 
api = hipchat.API(auth_token=token, room=ROOM)
notification = hipchat.Notification('I am Jack\'s HipChat notification')
api.post_notification(notification)
```

### Setting a Room Topic
```python
import hipchat
 
ROOM = '8675309'
token = '9b4f2a8c9db85063c5b8a5307f29a15d'
 
api = hipchat.API(auth_token=token, room=ROOM)
api.set_topic('I am Jack\'s room topic') 
```

### Listing Available Rooms
```python
import hipchat
 
ROOM = '8675309'
token = '9b4f2a8c9db85063c5b8a5307f29a15d'
 
api = hipchat.API(auth_token=token)
api.get_rooms()
```
