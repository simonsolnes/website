#!/usr/bin/env python3
import httplayer as http
from urllib.parse import parse_qs
import os
import logging

class StaticServer():
    def __init__(self, debug = False):
        self.s = http.socket_init()
        self.debug = debug
        logging.basicConfig(filename='log.txt', filemode='a', datefmt='%H:%M:%S', level=logging.DEBUG)

        self.logger = logging.getLogger(__name__)

    def run(self):
        while True:
            con, raw_req = http.recv(self.s)
            try:
                req = http.RequestHandler(raw_req)
                res = self.fufill_request(req)
                http.send(con, res)
            except Exception as error:
                print('[!!!] There was an error.')
                try:
                    print('\n--- Start Request ---')
                    print(raw_req.decode('utf-8'))
                    print('--- End Request ---\n')
                except:
                    pass
                self.logger.exception(error)
                try:
                    http.send(con, http.fucked_up())
                except:
                    print('[!!] Could not send error msg')

    def fufill_request(self, req):
        if req.met == 'GET':
            ref = [i for i in req.referer.split('/') if i]
            arg = [i for i in req.arg.split('/') if i]
            root = []
            while ref and arg and ref[0] == arg[0]:
                root.append(ref.pop(0))
                arg.pop(0)

            path = 'public/' + '/'.join(root + ref + arg)
            print(path)

            if os.path.isdir(path) and os.path.isfile(path + '/index.html'):
                path = path + '/index.html'
            elif os.path.isfile(path):
                path = path
            else:
                print('could not find the file')
                return http.fucked_up()
                
            doc = open(path, 'rb')
            body = doc.read()
            doc.close()

            if path[-5:] == '.html':
                return http.ResponseGenerator('OK', ['Content-Type: text/html'], body)
            else:
                return http.ResponseGenerator('OK', body = body)
        else:
            return fucked_up()

if __name__ == "__main__":
    staticserver = StaticServer(debug = True)
    staticserver.run()
