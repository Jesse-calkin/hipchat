import unittest
import hipchat

ROOM = '8675309'
token = '9b4f2a8c9db85063c5b8a5307f29a15d' # Just a placeholder: MD5 ("shenannigans") = 9b4f2a8c9db85063c5b8a5307f29a15d

class TestMessageFormat(unittest.TestCase):
    """
    test message_formats
    """ 
    
    def test_message_formats(self):
        for i in hipchat.Notification.message_formats:
            notification = hipchat.Notification('message_format test', message_format=i)
            self.assertTrue(dict(vars(notification))['message_format'] == i)

    def test_invalide_message_format(self):
        with self.assertRaises(Exception):
            notification = hipchat.Notification('invalid message_format', message_format='hamsammich')

class TestColors(unittest.TestCase):
    """
    test message colors
    """

    def test_valid_colors(self):
        for i in hipchat.Notification.color_list:
            notification = hipchat.Notification('color test', color=i)
            self.assertTrue(dict(vars(notification))['color'] == i)

    def test_invalid_color(self):
        with self.assertRaises(Exception):
            notification = hipchat.Notification('invalid color', color='potato')

class TestMessageLength(unittest.TestCase):
    """
    test message length
    """
    def test_below_min_message_length(self):
        """test below minimum message length"""
        with self.assertRaises(Exception):
            notification = hipchat.Notification('')
        
    def test_above_max_message_length(self):
        """test above max message length"""
        with self.assertRaises(Exception):
            test_string = ''
            for i in range(0,hipchat.Notification.max_message_length+1):
                test_string += 'T'
                notification = hipchat.Notification(test_string)
    
    def test_min_message_length(self):
        """test minimum message length"""
        notification = hipchat.Notification('1')
        self.assertTrue(dict(vars(notification))['message']=='1')
        
    def test_max_message_length(self):
        """test max message length"""
        test_string = ''
        for i in range(0,hipchat.Notification.max_message_length):
            test_string += 'T'
            notification = hipchat.Notification(test_string)
        self.assertTrue(dict(vars(notification))['message']==test_string)

class TestRoomLength(unittest.TestCase):
    """
    Test the room length
    """
    
    def test_over_max(self):
        """ test over the max room length """
        room_string = ''
        for i in range(0,hipchat.API.room_length+1):
            room_string += 'R'
        with self.assertRaises(Exception):
            hipchat.API(auth_token=token, room=room_string)

    def test_max_room_length(self):
        """ test the max room length """
        room_string = ''
        for i in range(0,hipchat.API.room_length):
            room_string += 'R'
        api = hipchat.API(auth_token=token, room=room_string)
        self.assertTrue(dict(vars(api))['room'] == room_string)

if __name__ == '__main__':
    unittest.main()