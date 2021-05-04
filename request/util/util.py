import queue
import os
import datetime
import json

class Util(object):
    """ container class for utility methods """

    @staticmethod
    def find(obj, key):
        """
        iterates through the dict in param: 'obj' and looks for the param: 'key'
        returns the values of the found param: 'key'
        """

        q = queue.Queue()
        q.put(obj)

        while not(q.empty()):
            item = q.get()

            if isinstance(item, (dict)):
                for k, v in item.items():
                    if k == key:
                        result = v
                        while(type(result) is dict) or (type(result) is list):    
                            if type(result) is dict:
                                result = result['text']
                            if type(result) is list:
                                result = result[0]
                        return v
                    if isinstance(v, list):
                        q.put(v)
            elif isinstance(item, list):
                for i in item:
                    q.put(i)
            q.task_done()

    @staticmethod
    def get_base_directory():
        """
        returns the modules base directory
        """

        directory = os.path.dirname(os.path.abspath(__file__))
        results = directory.split('\\')
        tail = results[-1].lower()

        while tail != 'oxfordapi':
            directory = os.path.dirname(os.path.abspath(directory))
            results = directory.split('\\')
            tail = results[-1].lower()

        return directory

    @staticmethod
    def read_config():
        """ 
        reads the config file located in the resources directory
        """

        content = None

        baseDir = Util.get_base_directory()
        configDir = baseDir + '/resources/config.json'

        try:
            with open(configDir) as json_file:
                content = json.load(json_file)

        except IOError:
            Util.write('Config nicht gefunden unter dem Dateipfad: {}'.format(configDir))

        return content

    @staticmethod
    def write(message):
        """
        writes exception-messages in the log.txt file located in the modules base directory
        """

        baseDir = Util.get_base_directory()
        logFile = baseDir + '/log.txt'

        with open(logFile, "a") as log:
            log.write(str('{0} | {1}\n').format(datetime.datetime.now(), message))
        