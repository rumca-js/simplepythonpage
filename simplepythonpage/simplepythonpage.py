import time
import argparse
import urllib
import cgi
import os
import importlib
import logging
import simplepythonpage.html

from http.server import BaseHTTPRequestHandler, HTTPServer


__version__ = '1.0.1'


class ExamplePage(simplepythonpage.html.PageBasic):
    def __init__(self):
        super().__init__()

        self.set_page_contents("""<p>List page</p>""")


class PageBuilder(object):
    def __init__(self, handler = None):
        self._handler = handler
        self._pages = {}

    def set_handler(self, handler):
        self._handler = handler

    def register_page(self, url, page):
        self._pages[url] = page

    def get_page(self, method):

        path = self._handler.get_path_relative()

        for item in self._pages:
            if path == item:
                page = self._pages[item]()
                page.set_path(path)
                page.set_handler(self._handler)
                page.set_method(method)
                page.set_args(self._handler.get_args())
                page.set_client_ip(self._handler.client_address[0])
                return page

        else:
            return None


class SimplePythonPageServer(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("Request:\t{0}\t{1}\t{2}".format("GET", self.client_address, self.get_path_relative()))

        _builder.set_handler(self)

        self._set_headers()

        page = _builder.get_page('GET')
        if page:
            page.super_write()
        else:
            logging.error("Page not supported: {0}".format(self.get_path_relative() ) )

    def do_POST(self):
        logging.info("Request:\t{0}\t{1}\t{2}".format("POST", self.client_address, self.get_path_relative()))

        _builder.set_handler(self)

        self._set_headers()

        page = _builder.get_page('POST')
        if page:
            page.super_write()
        else:
            logging.error("Page not supported: {0}".format(self.get_path_relative() ) )

    def get_path_relative(self):
        text = str(self.path)
        wh = text.find("?")
        if wh != -1:
            return text[:wh]
        return text

    def get_args(self):
        """ returns GET arguments in map  key = value """
        arguments = {}

        sp = str(self.path).split("?")
        if len(sp) > 1:
            items = sp[1].split("&")

            for item in items:
                inner_sp = item.split("=")

                if len(inner_sp) > 1:
                    arguments[inner_sp[0]] = urllib.parse.unquote_plus(inner_sp[1])

        return arguments


_builder = None


class SimplePythonPageSuperServer():

    def __init__(self, host_name, port):
        self._host_name = host_name
        self._port = port

        self._webServer = HTTPServer(('', self._port), SimplePythonPageServer)
        self._close_items = []

    def get_builder(self):
        global _builder
        return _builder

    def create_builder(self):
        global _builder
        _builder = PageBuilder()

    def add_close_item(self, closeitem):
        self._close_items.append(closeitem)

    def register_page(self, url, page):
        if self.get_builder() is None:
            self.create_builder()
        self.get_builder().register_page(url, page)

    def start_server(self):

        logging.info("Server started http://%s:%s" % (self._host_name, self._port))

        try:
            self._webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        self.close()

    def close(self):
        self._webServer.server_close()

        for item in self._close_items:
            item.close()

        logging.info("Server stopped.")

    def get_server(self):
        return self._webServer


class CommandLine(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Download server')
        self.parser.add_argument('-H', '--host-name', dest='host_name', default = 'localhost', help = "Host Name")
        self.parser.add_argument('-P', '--port', dest='port', default = 8080, type=int,
                                help='Server port')
        self.args = self.parser.parse_args()


if __name__ == "__main__":        

    logging.basicConfig(level=logging.INFO)

    cmd = CommandLine()

    superserver = SimplePythonPageSuperServer(cmd.args.host_name, cmd.args.port)
    superserver.register_page("/download", ExamplePage() )
    superserver.register_page("/download/index.xyz", ExamplePage() )

    superserver.start_server()
