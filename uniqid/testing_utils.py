
class MessageTestMixin(object):
    """
    Helper functions for accessing messages from the django messages framework
    during testing
    """
    @classmethod
    def getmessage(cls, response):
        """Helper method to return message from response """
        for c in response.context:
            message = [m for m in c.get('messages')][0]
            if message:
                return message

    @classmethod
    def getallmessages(cls, response):
        """Helper method to return message from response """
        for c in response.context:
            messages = [m for m in c.get('messages')]
            if messages:
                return messages
