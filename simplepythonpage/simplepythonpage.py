import time
import argparse
import urllib
import cgi
import importlib
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer



class HtmlElement(object):

    def __init__(self, container_text = "p", text = "", attrs = {}):
        self._container_text = container_text
        self._text = text
        self._attrs = {}

    def html(self):
        return self._text

    def set_attr(self, key, value):
        self._attrs[key] = value

    def get_attr(self, key, value):
        return self._attrs[key]

    def attrs(self):
        return self._attrs

    def get_attr_text(self):
        attr_text = ""
        for attr_key in self._attrs:
            attr = self._attrs[attr_key]
            if attr_text != "":
                attr_text += " "
            attr_text += '{0}="{1}"'.format(attr_key, attr)
        return attr_text

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text


class HtmlOneLiner(HtmlElement):

    def __init__(self, container_text = "img", attrs = {}):
        super().__init__(container_text, "", attrs)

    def html(self):
        attr_text = ""
        if self.get_attr_text():
            attr_text = " " + self.get_attr_text()

        return "<{0}{1}>".format(self._container_text, attr_text, self._text)


class HtmlContainer(HtmlElement):

    def __init__(self, container_text = "p", text = "", attrs = {}):
        super().__init__(container_text, text, attrs)
        self.items = []

    def push(self, item):
        self.items.append(item)

    def insert(self, text):
        if text:
            if isinstance(text, str):
                self._text += text
            else:
                self._text += text.html()

    def html(self):
        attr_text = ""
        if self.get_attr_text():
            attr_text = " " + self.get_attr_text()

        if self._text is None:
            all_text = ""
        else:
            all_text = "<{0}{1}>{2}</{0}>".format(self._container_text, attr_text, self._text)

        for item in self.items:
            if isinstance(item, str):
                item_text = item
            else:
                item_text = item.html()
            all_text += "<{0}{1}>{2}</{0}>".format(self._container_text, attr_text, item_text )

        return all_text


class HtmlFormInput(HtmlOneLiner):

    def __init__(self, atype = None, aid = None, default_value = None):
        super().__init__("input")

        if atype:
            self.set_attr("type", atype)
        if aid:
            self.set_attr("id", aid)
            self.set_attr("name", aid)

        if default_value:
            self.set_attr("value", default_value)
            self.set_attr("size", len(default_value))


class HtmlForm(HtmlContainer):

    def __init__(self):
        super().__init__("form")
        self._inputs = []
        self._action = None

    def add_input(self, ainput):
        self._inputs.append(ainput)

    def html(self):
        input_html = ""
        for ainput in self._inputs:
            input_html += ainput.html()

        self.set_text(input_html)
        return super().html()


class HtmlTable(HtmlElement):

    def __init__(self, table_arg, with_header=False):
        super().__init__()
        self._data = table_arg
        self._with_header = with_header
        self._align = None
        self._valign = None

    def set_align(self, align):
        self._align = align

    def set_valign(self, valign):
        self._valign = valign

    def html(self):
        if self._with_header:
            return self.html_with_header()
        else:
            return self.html_no_header()

    def html_no_header(self):
        text = ""

        tab = HtmlContainer("table")
        for row in self._data:
            tr = HtmlContainer("tr")
            for cell in row:
                td = HtmlContainer("td", cell)
                if self._align:
                    td.set_attr("align", self._align)
                    td.set_attr("valign", self._valign)
                tr.insert(td)
            tab.insert(tr)
        return tab.html()

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
        self._method = "GET"
        self._form = None

    def set_title(self, title):
        self._title = title

    def set_handler(self, handler):
        self._handler = handler

    def set_method(self, method):
        self._method = method

    def get_method(self):
        return self._method

    def get_path_relative(self):
        return self._handler.get_path_relative()

    def get_args(self):
        return self._handler.get_args()

    def get_post_arg(self, key):
        if not self._form:
            self._form = cgi.FieldStorage(
                fp=self._handler.rfile,
                headers=self._handler.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
        return self._form.getvalue(key)

    def get_client_address(self):
        return self._handler.client_address

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
        self.set_page_contents("Default document")

    def write_page_contents(self, args = None):
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
        self.write_page_contents(args)

    def p(self, text = None):
        return HtmlContainer("p", text)

    def h1(self, text = None):
        return HtmlContainer("h1", text)

    def h2(self, text = None):
        return HtmlContainer("h2", text)

    def h3(self, text = None):
        return HtmlContainer("h3", text)

    def h4(self, text = None):
        return HtmlContainer("h4", text)

    def h5(self, text = None):
        return HtmlContainer("h5", text)

    def h6(self, text = None):
        return HtmlContainer("h6", text)

    def div(self, text = None):
        return HtmlContainer("div", text)

    def span(self, text = None):
        return HtmlContainer("span", text)

    def pre(self, text = None):
        return HtmlContainer("pre", text)

    def br(self):
        hto = HtmlOneLiner("br")
        return hto

    def hr(self):
        hto = HtmlOneLiner("hr")
        return hto

    def table(self, table, with_header = False):
        return HtmlTable(table, with_header)

    def img(self, src, width = None, height = None):
        hto = HtmlOneLiner("img")
        hto.set_attr("src", src)
        if width:
            hto.set_attr("width", width)
        if height:
            hto.set_attr("height", height)
        return hto

    def link(self, title, dst):
        cont = HtmlContainer("a")
        cont.set_attr("href", dst)
        cont.set_text(title)
        return cont

    def form_input(self, itype = None, iid = None, default_value = None):
        return HtmlFormInput(itype, iid, default_value)

    def form_input_submit(self, text = None):
        ainput = HtmlFormInput()
        ainput.set_attr("type","submit")
        if not text:
            ainput.set_attr("value","Submit")
        else:
            ainput.set_attr("value", text)
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
        cont = HtmlContainer("label")
        cont.set_attr("for", afor)
        cont.set_text(text)
        return cont


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

    def get_page(self, method):

        path = self._handler.get_path_relative()

        for item in self._pages:
            if path == item:
                page = self._pages[item]
                page.set_handler(self._handler)
                page.set_method(method)
                return page

        else:
            return None


class SimplePythonPageServer(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        _builder.set_handler(self)

        self._set_headers()

        page = _builder.get_page('GET')
        if page:
            page.super_write()
        else:
            logging.error("Page not supported: {0}".format(self.get_path_relative() ) )

    def do_POST(self):
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
