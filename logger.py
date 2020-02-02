import os.path
import logging
from time import gmtime, strftime


class Logger:
    def __init__(self, filename):
        self.port = 0
        if not os.path.exists(filename):
            open(filename, "w")
        logging.basicConfig(filename=filename, level=logging.DEBUG)

    def __form_date(self):
        time = str(strftime("%d %b %Y %H:%M:%S", gmtime()))
        return '[{}]'.format(time)

    def log_start(self, port):
        self.port = port
        message = '{} -- start with {} port'.format(self.__form_date(), port)
        logging.info(message)

    def log_shutdown(self):
        message = '{} -- shutdown {} port'.format(self.__form_date(), self.port)
        self.port = 0
        logging.info(message)

    def log_response(self, request_type: str, path: str, headers: str):
        headers = headers.replace('\n', ' ')
        message = "{} -- {} request\n\tPath: {}\n\t{}".format(
            self.__form_date(),
            request_type,
            path, headers
        )
        logging.info(message)
