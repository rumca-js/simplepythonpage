import logging
import argparse
from aiohttp import web

import simplepythonpage


"""
https://docs.aiohttp.org/en/stable/web_quickstart.html
"""


class PageBuilder(object):

    def __init__(self):
        self._pages = {}

    def register_page(self, url, page):
        self._pages[url] = page

    def get_page(self, path, method):
        for item in self._pages:
            if path == item:
                page = self._pages[item]()
                page.set_path(path)
                page.set_method(method)
                return page

        else:
            return None


builder = PageBuilder()


async def handle(request):

    name = request.match_info.get('name', "Anonymous")

    #request.method == 'POST':

    #page = builder.get_page(request.path, request.method)
    page = builder.get_page(request.path, request.method)
    args = {}
    page_text = page.write(args)

    text = "Hello, " + name + request.method + " " + request.path + " " + page_text

    return web.Response(text=text)


class IOSimplePythonPageSuperServer(object):

    def __init__(self, host_name, port):
        self._host_name = host_name
        self._port = port

        self._webServer = web.Application()

    def register_page(self, route, page):
        builder.register_page(route, page)

        self._webServer.add_routes([web.get(route, handle),
                                    web.post(route, handle)])

    def start_server(self):
        web.run_app(self._webServer)


class ExamplePage(object):
    pass

    def write(self, args):
        return "Example page"

    def set_path(self, path):
        pass

    def set_method(self, method):
        pass

    def set_reference(self, aobj):
        pass


class CommandLine(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Download server')
        self.parser.add_argument('-H', '--host-name', dest='host_name', default = 'localhost', help = "Host Name")
        self.parser.add_argument('-P', '--port', dest='port', default = 8080, type=int,
                                help='Server port')
        self.args = self.parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    cmd = CommandLine()

    superserver = IOSimplePythonPageSuperServer(cmd.args.host_name, cmd.args.port)

    superserver.register_page("/download", ExamplePage )

    superserver.start_server()
