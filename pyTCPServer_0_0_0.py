import socketserver
import json
import os
import traceback
def replace(s):
    ls = []
    for i in s:
        if ord(b'a') <= i <= ord(b'z') or \
           ord(b'A') <= i <= ord(b'Z') or \
           ord(b'0') <= i <= ord(b'9'):
            ls.append(chr(i))
        else:
            ls.append('%' + hex(i)[2:])
    return ''.join(ls)
def errorDisplay(code, content):
    return b'HTTP/1.1 %s\n\
Content-Type: text/plain\n\nERROR: MISSING %s FILE.' % \
(code + b' ' + content, code)
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip()
        try:
            if data != b'':
                path = data.split(b'\n')[0].split()[1][1:]
                path = 'server' + os.sep + replace(path)
                if os.path.isfile(path):
                    file = open(path)
                    self.request.sendall(b'HTTP/1.1 200 OK\n' +
                                         trans[path.split('%2e')[-1]].encode() +
                                         b'\n' + file.read().encode())
                elif os.path.isfile(path + '%SUF'):
                    file = open(path + '%SUF')
                    self.request.sendall(b'HTTP/1.1 200 OK\n' +
                                         file.read().encode())
                else:
                    path = 'error/404'
                    if os.path.isfile(path):
                        file = open(path)
                        self.request.sendall(file.read().encode())
                    else:
                        self.request.sendall(errorDisplay(b'404', b'Not Found'))
        except Exception:
            print(traceback.format_exc())
            path = 'error/500'
            if os.path.isfile(path):
                file = open(path)
                self.request.sendall(file.read().encode())
            else:
                self.request.sendall(errorDisplay(b'500', b'Internal Server Error'))
                
if __name__ == '__main__':
    file = open('suffix.json')
    trans = json.load(file)
    file.close()
    host = "localhost", 9999
    with socketserver.TCPServer(host, MyTCPHandler) as server:
        server.serve_forever()
