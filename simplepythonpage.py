import time
import argparse
import urllib
import importlib
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer


class PageBasic(object):

    def __init__(self, handler = None):
        self._handler = handler

        self.init_default_values()

    def init_default_values(self):

        self._header = """
        <html><head><title>SimplePythonPage</title></head>
        <body>
        """

        self.set_page_contents("Default document")

        self._footer = """
        </body></html>
        """

    def set_handler(self, handler):
        self._handler = handler

    def split_path(self):
        return str(self._handler.path).split("/").pop()

    def write_string(self, string):
        self._handler.wfile.write(bytes(string, "utf-8"))

    def get_page_contents(self):
        return self._page_contents

    def set_page_contents(self, page_contents):
        self._page_contents = page_contents

    def write(self):
        self.write_string(self._header)
        self.write_string(self.get_page_contents() )
        self.write_string(self._footer)


class ExamplePage(PageBasic):
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

    def get_page(self):

        path = self._handler.get_path_relative()

        for item in self._pages:
            if path == item:
                page = self._pages[item]
                page.set_handler(self._handler)
                return page

        else:
            return None



class SimplePythonPageServer(BaseHTTPRequestHandler):

    def do_GET(self):
        _builder.set_handler(self)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        page = _builder.get_page()
        if page:
            page.write()
        else:
            logging.error("No page found")

    def get_path_relative(self):
        text = str(self.path)
        wh = text.find("?")
        if wh != -1:
            return text[:wh]
        return text

    def split_path(self):
        """ Returns last element in path """
        text = str(self.path).split("/").pop()
        wh = text.find("?")
        if wh != -1:
            return text[:wh]
        return text

    def get_GET_arguments(self):
        """ returns GET arguments in map  key = value """
        arguments = {}

        sp = str(self.path).split("?")
        if len(sp) > 1:
            items = sp[1].split("&")

            for item in items:
                inner_sp = item.split("=")

                if len(inner_sp) > 1:
                    arguments[inner_sp[0]] = urllib.parse.unquote(inner_sp[1])

        return arguments



class SimplePythonPageSuperServer():

    def __init__(self, host_name, port):
        self._host_name = host_name
        self._port = port

        self._webServer = HTTPServer(('', self._port), SimplePythonPageServer)

    def start_server(self):

        logging.info("Server started http://%s:%s" % (self._host_name, self._port))

        try:
            self._webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        self._webServer.server_close()

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


def set_page_builder(builder):
    global _builder
    _builder = builder


if __name__ == "__main__":        

    logging.basicConfig(level=logging.INFO)

    cmd = CommandLine()

    superserver = SimplePythonPageSuperServer(cmd.args.host_name, cmd.args.port)

    builder = PageBuilder()
    builder.register_page("/download", ExamplePage() )
    builder.register_page("/download/index.xyz", ExamplePage() )
    set_page_builder(builder)

    superserver.start_server()
