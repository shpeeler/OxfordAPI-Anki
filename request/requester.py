from .util.util import Util
from .api import API
import json

class Requester(API):
    """ contains methods for api calls """
    
    def __init__(self, app_id, app_key, timeout=5, sleep=1.5):
        super().__init__(app_id, app_key)

    def get_information(self, word, language, params=None):
        """ 
        calls the underlying api for information with param: 'path'
        returns the reponse as json
        """

        fields = ''

        if params != None and len(params) < 0:
            fields = fields + '?fields='

            for param in params:
                fields = fields + ',{}'.format(param)
        
        response = self.request_data(word, language, fields)
        if response == None or response.status_code != 200:
            return None
        
        json_obj = json.loads(response.content.decode('utf-8'))

        return json_obj

    def get_translation(self, word, src_language="en", target_language="de"):
        """
        calls the underlying api for translations
        returns response as json
        """

        response = self.request_translation(word, src_language, target_language)
        if response == None or response.status_code != 200:
            Util.write('response is {}'.format(response))
            return None

        json_obj = json.loads(response.content.decode('utf-8'))

        return json_obj
