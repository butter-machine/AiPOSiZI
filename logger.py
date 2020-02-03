import os.path
import logging
from time import gmtime, strftime


class Logger:
    def __init__(self, filename):
        self.port = 0
        if not os.path.exists(filename):
            open(filename, "w")
        logging.basicConfig(
            filename=filename,
            level=logging.DEBUG,
            format='%(asctime)s %(message)s'
        )

    def log_start(self, port):
        self.port = port
        message = 'start with {} port'.format(port)
        logging.info(message)

    def log_shutdown(self):
        message = 'shutdown {} port'.format(self.port)
        self.port = 0
        logging.info(message)

    def log_response(self, request_type: str, path: str, headers: str):
        headers = headers.replace('\n', ' ')
        message = "{} request\n\tPath: {}\n\t{}".format(
            request_type,
            path,
            headers
        )
        logging.info(message)
