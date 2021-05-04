from .util.util import Util
import requests
import json
import time

class API(object):
    """ contains methods for api call conduction """

    session = requests.Session()
    session.headers = {'application': 'PythonWrapper'}

    base_url_data = "https://od-api.oxforddictionaries.com/api/v2/entries/{}/{}{}"
    base_url_translation = "https://od-api.oxforddictionaries.com/api/v2/translations/{}/{}/{}"

    def __init__(self, app_id, app_key, timeout=5, sleep=1.5):
        self.headers = {'app_id': app_id, 'app_key': app_key}
        self.timeout = timeout
        self.sleep = sleep

    def request_data(self, word, language, params, method="GET"):
        """
        calls the oxforddictionary api for word data/information
        returns word data
        """

        time.sleep(self.sleep)
        url = str(self.base_url_data).format(language, word, params)
        try:
            response = self.session.request(method,
                                            url,
                                            timeout=self.timeout,
                                            headers=self.headers)
        except requests.exceptions.ConnectionError as e:
            Util.write(str(e))
            return None
        
        finally:
            self.session.close()

        return response

    def request_translation(self, word, src_language, target_language, method="GET"):
        """
        calls the oxforddictonary api for translations
        returns translation
        """

        time.sleep(self.sleep)
        url = str(self.base_url_translation).format(src_language, target_language, word)

        try:
            response = self.session.request( method,
                                            url,
                                            timeout=self.timeout,
                                            headers=self.headers)
        except requests.exceptions.ConnectionError as e:
            Util.write(str(e))
            return None

        finally:
            self.session.close()

        return response