import logging
import argparse
from pathlib import Path

from aiohttp import web

import simplepythonpage


"""
https://docs.aiohttp.org/en/stable/web_quickstart.html

https://docs.aiohttp.org/en/stable/web_reference.html
"""


class DefaultPage(simplepythonpage.html.PageBasic):

    def write_all(self, args):
        text = ""

        path = Path(self.get_path()[1:])
        file_name = self.get_path()[1:]

        if path.is_file():
            with open(file_name, encoding='utf-8') as fh:
                data = fh.read()
                text = data
        else:
            text = "You're lost!"

        return text


class ExamplePage(simplepythonpage.html.PageBasic):

    def write(self, args):
        text = '<link rel="shortcut icon" type="image/x-icon" href="favicon.ico" />'
        text += "Example page"
        return text

    def set_path(self, path):
        pass

    def set_method(self, method):
        pass

    def set_reference(self, aobj):
        pass


class PageBuilder(object):

    def __init__(self):
        self._pages = {}
        self._default_page = DefaultPage

    def register_page(self, url, page):
        self._pages[url] = page

    def init_page(self, page, path, method, request):
        page.set_path(path)
        page.set_method(method)
        page.set_args(request.query)
        page.set_client_ip(request.remote)
        return page

    def get_page(self, path, method, request):
        for item in self._pages:
            if path == item:
                page = self._pages[item]()

                self.init_page(page, path, method, request)

                return page

        else:
            return None

    def get_default_page(self, path, method, request):
        page = self._default_page()
        self.init_page(page, path, method, request)
        return page

    def set_default_page(self, page_handler):
        self._default_page = page_handler


builder = PageBuilder()


async def handle(request):

    page = builder.get_page(request.path, request.method, request)
    page_text = page.write_all(page.get_args())

    return web.Response(text=page_text, content_type=page.get_content_type() )


async def default_handle(request):
    page = builder.get_default_page(request.path, request.method, request)
    page_text = page.write_all(page.get_args())

    return web.Response(text=page_text, content_type=page.get_content_type() )


class IOSimplePythonPageSuperServer(object):

    def __init__(self, host_name, port):
        self._host_name = host_name
        self._port = port

        self._webServer = web.Application()
        self._close_items = []
        self._register_default_page = False

    def register_page(self, route, page):
        builder.register_page(route, page)

        self._webServer.add_routes([web.get(route, handle),
                                    web.post(route, handle)])

    def set_default_page(self, page):
        builder.set_default_page(page)
        self._register_default_page = True

    def start_server(self):
        try:
            if self._register_default_page:
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


class CommandLine(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Download server')
        self.parser.add_argument('-H', '--host-name', dest='host_name', default = 'localhost', help = "Host Name")
        self.parser.add_argument('-P', '--port', dest='port', default = 8080, type=int,
            help='Port')
        self.parser.add_argument('-d', '--default', action="store_true", dest='default_handling', default=False,
            help='Default handling page')
        self.args = self.parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO)

    cmd = CommandLine()

    superserver = IOSimplePythonPageSuperServer(cmd.args.host_name, cmd.args.port)

    superserver.register_page("/download", ExamplePage )

    if cmd.args.default_handling:
        superserver.set_default_page(DefaultPage)

    superserver.start_server()


if __name__ == '__main__':
    main()
