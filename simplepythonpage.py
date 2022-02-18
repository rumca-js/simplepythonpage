import time
import argparse
import urllib
import importlib
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer



class HtmlElement(object):

    def __init__(self, text = ""):
        self._text = text

    def html(self):
        return self._text


class HtmlContainer(HtmlElement):

    def __init__(self, text = None):
        super().__init__()
        self.items = []
        self._text = text
        self._container_text = ""

    def add(self, item):
        self.items.append(item)

    def html(self):
        if self._text:
            return "<{0}>{1}</{0}>".format(self._container_text, self._text)

        html_text = ""

        for item in self.items:
            html_text += "<{0}>{1}</{0}>".format(self._container_text, item.html() )

        return html_text


class HtmlParagraph(HtmlContainer):

    def __init__(self, text = None):
        super().__init__(text)
        self._container_text = "p"


class HtmlDiv(HtmlContainer):

    def __init__(self, text = None):
        super().__init__(text)
        self._container_text = "div"


class HtmlLink(HtmlElement):
    def __init__(self, title, destination):
        super().__init__()
        self._title = title
        self._destination = destination

    def html(self):
        return '<a href="{1}">{0}</a>'.format(self._title, self._destination)


class HtmlLabel(HtmlElement):
    def __init__(self, text, afor=None):
        super().__init__()
        self._text = text
        self._afor = afor

    def html(self):
        if self._afor:
            return '<label for="{0}">{1}</label>'.format(self._afor, self._text)
        else:
            return '<label>{0}</label>'.format(self._text)


class HtmlFormInput(HtmlElement):

    def __init__(self, atype = None, aid = None, default_value = None):
        super().__init__()

        self._items = {}
        if atype:
            self._items["type"] = atype
        if aid:
            self._items["id"] = aid
            self._items["name"] = aid

        if default_value:
            self._items["value"] = default_value
            self._items["size"] = len(default_value)

    def add_key(self, key, value):
        self._items[key] = value

    def html(self):
        input_text = ""
        for item in self._items:
            input_text += '{0}="{1}" '.format(item, self._items[item])

        return "<input {0}>".format(input_text)


class HtmlForm(HtmlElement):

    def __init__(self):
        super().__init__()
        self._inputs = []
        self._action = None

    def add_input(self, ainput):
        self._inputs.append(ainput)

    def add_action(self, action):
        self._action = action

    def html(self):
        input_html = ""
        for ainput in self._inputs:
            input_html += ainput.html()

        if not self._action:
            return """<form>{0}</form>""".format(input_html)
        else:
            return """<form action="{0}">{1}</form>""".format(self._action, input_html)


class HtmlBackForm(HtmlForm):

    def __init__(self):
        super().__init__()
        self.add_input(HtmlFormInput())


class PageBasic(object):

    def __init__(self, handler = None):
        self._handler = handler
        self._title = "SimplePythonPageTitle"
        self._header = ""
        self._footer = ""

    def set_title(self, title):
        self._title = title

    def set_handler(self, handler):
        self._handler = handler

    def get_path_relative(self):
        return self._handler.get_path_relative()

    def get_args(self):
        return self._handler.get_args()

    def get_arg(self, arg):
        return self._handler.get_args()[arg]

    def has_args(self):
        return len(self._handler.get_args()) > 0

    def write_string(self, string):
        self._handler.wfile.write(bytes(string, "utf-8"))

    def get_page_contents(self):
        return self._page_contents

    def set_page_contents(self, page_contents):
        self._page_contents = page_contents

    def set_header(self, header):
        self._header = header

    def set_footer(self, footer):
        self._header = header

    def write(self, args = None):
        if self._header == "":
            self._header = """
            <html><head><title>{0}</title></head>
            <body>
            """.format(self._title)

        if self._page_contents == "":
            self.set_page_contents("Default document")

        if self._footer == "":
            self._footer = """
            </body></html>
            """

        self.write_string(self._header)
        self.write_string(self.get_page_contents() )
        self.write_string(self._footer)

    def super_write(self):
        args = self.get_args()

        self.write(args)

    def p(self, text = None):
        return HtmlParagraph(text)

    def div(self, text = None):
        return HtmlDiv(text)

    def br(self):
        return HtmlElement("<br>")

    def hr(self):
        return HtmlElement("<hr>")

    def link(self, title, src):
        return HtmlLink(title, src)

    def form_input(self, itype = None, iid = None, default_value = None):
        return HtmlFormInput(itype, iid, default_value)

    def form_input_submit(self, text = None):
        ainput = HtmlFormInput()
        ainput.add_key("type","submit")
        if not text:
            ainput.add_key("value","Submit")
        else:
            ainput.add_key("value", text)
        return ainput

    def form(self):
        return HtmlForm()

    def form_go_back(self):

        form = self.form()
        ainput = HtmlFormInput()
        ainput.add_key("type","button")
        ainput.add_key("value","Go back!")
        ainput.add_key("onclick","history.back()")

        form.add_input(ainput)

        return form

    def label(self, text, afor = None):
        return HtmlLabel(text, afor)


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



class SimplePythonPageSuperServer():

    def __init__(self, host_name, port):
        self._host_name = host_name
        self._port = port

        self._webServer = HTTPServer(('', self._port), SimplePythonPageServer)
        self._close_items = []

    def add_close_item(self, closeitem):
        self._close_items.append(closeitem)

    def start_server(self):

        logging.info("Server started http://%s:%s" % (self._host_name, self._port))

        try:
            self._webServer.serve_forever()
        except KeyboardInterrupt:
            pass

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
