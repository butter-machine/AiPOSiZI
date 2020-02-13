#!/usr/bin/python3
import os.path
import http.server
from http.server import BaseHTTPRequestHandler
import socketserver
import argparse
from logger import Logger


parser = argparse.ArgumentParser(description='HTTP 1.1 server')
parser.add_argument('port', type=int, help='port to connections')
parser.add_argument("-o", "--origin",
                    help="Access-Control-Allow-Origin default header",
                    action="store_true")
parser.add_argument("-m", "--methods",
                    help="Access-Control-Allow-Methods default header",
                    action="store_true")

logger = Logger('.log')                    

args = parser.parse_args()

PORT = args.port
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        request_path = os.path.join(BASE_DIR, self.path[1:])
        print(request_path, self.path, BASE_DIR)
        if os.path.isfile(request_path):
            self.send_response(200, 'ok')
            self.end_headers()
            with open(request_path, 'rb') as file: 
                self.wfile.write(file.read())
            logger.log_response(
                'GET',
                str(200),
                str(self.path),
                str(self.headers)
            )
        else:
            self.send_response(404)
            self.end_headers()
            logger.log_response(
                'GET',
                str(404),
                str(self.headers),
                str(self.path),
                ''
            )

    def do_POST(self):
        try:
            self.send_response(200, 'ok')
            length = int(self.headers.get('content-length'))
            body = self.rfile.read(length)
            logger.log_response(
                'POST',
                str(200),
                str(self.headers),
                str(self.path),
                str(body)
            )
            self.wfile.write(str(body))
            self.wfile.close()
        except:
            self.send_response(500)
        

    def do_OPTIONS(self):
        self.send_response(200, 'ok')

        headers = []
        if (args.origin):
            self.send_header(
                'Access-Control-Allow-Origin',
                'http://localhost:' + str(PORT)
            )
            headers.append({'Access-Control-Allow-Origin': 'http://localhost:' + str(PORT)})

        if (args.methods):
            self.send_header(
                'Access-Control-Allow-Methods',
                'GET, POST, OPTIONS'
            )
            headers.append({'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'})

        self.end_headers()
        
        logger.log_response(
            'OPTIONS',
            str(200),
            str(headers),
            str(self.path),
            ''
        )
    

class Server():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5

    def run(self):
        try:
            with socketserver.TCPServer(('', PORT), Handler) as httpd:
                print("Serving at port", PORT)
                logger.log_start(PORT)
                httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
            print('\nServer shutted down')
            logger.log_shutdown()


if __name__ == "__main__":
    Server().run()
