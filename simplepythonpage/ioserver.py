import logging
import argparse
from aiohttp import web

import simplepythonpage


"""
https://docs.aiohttp.org/en/stable/web_quickstart.html

https://docs.aiohttp.org/en/stable/web_reference.html
"""


class PageBuilder(object):

    def __init__(self):
        self._pages = {}

    def register_page(self, url, page):
        self._pages[url] = page

    def get_page(self, path, method, request):
        for item in self._pages:
            if path == item:
                page = self._pages[item]()
                page.set_path(path)
                page.set_method(method)
                page.set_args(request.query)
                page.set_client_ip(request.remote)

                return page

        else:
            return None


builder = PageBuilder()


async def handle(request):

    page = builder.get_page(request.path, request.method, request)
    page_text = page.write_all(page.get_args())

    return web.Response(text=page_text, content_type="text/html")


async def default_handle(request):
    page_text = 'Error'
    return web.Response(text=page_text, content_type="text/html")


class IOSimplePythonPageSuperServer(object):

    def __init__(self, host_name, port):
        self._host_name = host_name
        self._port = port

        self._webServer = web.Application()
        self._close_items = []

    def register_page(self, route, page):
        builder.register_page(route, page)

        self._webServer.add_routes([web.get(route, handle),
                                    web.post(route, handle)])

    def start_server(self):
        try:
            self._webServer.add_routes([web.get('/{tail:.*}', default_handle)])

            web.run_app(self._webServer, host = self._host_name, port = self._port)
        except Exception as E:
            print(str(E))

    def add_close_item(self, closeitem):
        self._close_items.append(closeitem)

    def close(self):
        logging.info("Closing")

        for item in self._close_items:
            item.close()


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
