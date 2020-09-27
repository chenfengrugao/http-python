#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import re
import json
import os
import urllib.parse

class myHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    
    def param_handle(self, requestline):
        #print(type(requestline))
        #print(requestline)
        #GET /index.html?a=b&c=d HTTP/1.1
        #GET /favicon.ico HTTP/1.1

        print(requestline)
        get_string = requestline.split(' ')[1]
        
        #urldecode
        get_string = urllib.parse.unquote(get_string)

        #parse url
        self.get_data = {}
        if re.search(r'\?', get_string):
            get_str_list = get_string.split('?')
            self.get_data['page'] = get_str_list[0]
            self.get_data['param'] = get_str_list[1]
            get_param = {}
            get_param_list = self.get_data['param'].split('&')
            for param in get_param_list:
                if re.search(r'=', param):
                    param_item_list = param.split('=')
                    k = param_item_list[0]
                    get_param[k] = param_item_list[1]
            self.get_data['param_dict'] = get_param
        else:
            self.get_data['page'] = get_string
            self.get_data['param_dict'] = {}
            
    def do_GET(self):
        #get parameters
        self.param_handle(self.requestline)
        #print(self.get_data)

        #
        #router
        #

        #default page
        if self.get_data['page'] == '/':
            self.get_data['page'] = '/index.html'
        
        #html, css, js, ico, jpg, png
        mime = {
            'html': ['text/html', 'text'],
            'css': ['text/css', 'text'],
            'js': ['application/x-javascript', 'text'],
            'ico': ['image/x-icon', 'bin'],
            'jpg': ['image/jpeg', 'bin'],
            'jpeg': ['image/jpeg', 'bin'],
            'png': ['image/png', 'bin']
        }

        #
        #static file
        #
        if re.search(r'\.(html|css|js|ico|jpg|png)$', self.get_data['page']):
            filetype = self.get_data['page'].split('.')[-1]
        
            if mime[filetype][1] == 'text':
                fileaccess = "r"
            else:
                fileaccess = "rb"
            
            try:
                f = open('.' + self.get_data['page'], fileaccess).read()
                self.send_response(200)
                self.send_header('Content-type', mime[filetype][0]);
                self.end_headers()
                if mime[filetype][1] == 'text':
                    self.wfile.write(f.encode('utf-8'))
                else:
                    self.wfile.write(f)
            except FileNotFoundError:
                self.send_response(200)
                self.send_header('Content-type', 'text/html');
                self.end_headers()
                self.wfile.write("File Not Found".encode('utf-8'))
            except PermissionError:
                self.send_response(200)
                self.send_header('Content-type', 'text/html');
                self.end_headers()
                self.wfile.write("Permission denied".encode('utf-8'))

        #
        # dynamic page
        #
        elif re.search(r'\.py$', self.get_data['page']):
            #call handle() from external py file
            m = re.search(r'/(.*)\.py$', self.get_data['page'])
            
            import importlib
            h = importlib.import_module(m.group(1))
            data = h.handle(self.get_data['param_dict'])
            
            # data is the result, to be send to browser.
            # list and dict will be converted to json,
            #   and str will be sent directly.
            if isinstance(data, (list, dict)):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
            elif isinstance(data, str):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(data.encode('utf-8'))
            
        else:
            #Unknow File Type
            self.send_response(200)
            self.send_header('Content-type', 'text/html');
            self.end_headers()
            self.wfile.write("Unknow File Type".encode('utf-8'))
            
        
    def do_POST(self):
        pass

    
if __name__ == '__main__':
    print("starting verification platform ...")
    httpd = HTTPServer(('0.0.0.0', 8006), myHTTPServer_RequestHandler)
    print('done.')
    print('Please visit http://192.168.0.116:8006 in your browser.')
    httpd.serve_forever()
    
