import re
import os


"""
Ref emoji
 https://www.w3schools.com/charsets/ref_emoji.asp

pass unicode as:
U"\U0001F441"
, or
u", \u2705"
"""
class UtfSymbols(object):

    def get_eye():
        return U"\U0001F441"

    def green_checkbox():
        return u"\u2705"

    def red_x():
        return u"\u274C"


class Htmlify(object):

    def __init__(self, text):
        self._text = text

    def htmlify(self):
        text = self._text

        text = self.replace_links(text, "http")
        text = self.replace_links(text, "https")
        text = self.replace_spaces(text)

        return text

    def replace_spaces(self, text):
        text = text.replace("\n", "<br/>")
        return text

    def replace_links(self, text, link_type="https"):
        pattern = re.compile("\s")
        hyperlink_format = '<a href="{link}">{text}</a>'

        wh = 0
        while True:
            wh = text.find(link_type+"://", wh+1)
            if wh == -1:
                break

            obj = pattern.search(text, wh+1)
            if obj:
                end = obj.start()
            else:
                end  = len(text)

            link_text = text[wh:end]

            link_text = hyperlink_format.format(link=link_text, text=link_text)

            text = text[:wh] + link_text + text[end:]

            wh = wh + len(link_text)

        return text


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

            if attr is not None:
                attr_text += '{0}="{1}"'.format(attr_key, attr)
            else:
                attr_text += '{0}'.format(attr_key, attr)

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
        if self._text is None:
            self._text = ""

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

    def __init__(self, atype = None, aid = None, default_value = None, default_size = None):
        super().__init__("input")

        if atype:
            self.set_attr("type", atype)
        if aid:
            self.set_attr("id", aid)
            self.set_attr("name", aid)

        if default_value:
            self.set_attr("value", default_value)

        if default_size or default_value:
            if default_size:
                self.set_attr("size", default_size)
            else:
                self.set_attr("size", len(default_value))


class HtmlFormSelect(HtmlContainer):

    def __init__(self, aid = None):
        self.options = []
        super().__init__("select")

        if aid:
            self.set_attr("id", aid)
            self.set_attr("name", aid)

    def add_option(self, aValueId, aValueText, selected = False):
        c = HtmlContainer("option")
        c.set_attr("value", aValueId)
        c.set_text(aValueText)

        if selected:
            c.set_attr("selected", None)

        self.options.append(c)

    def html(self):
        input_html = ""
        for aoption in self.options:
            input_html += aoption.html()

        self.set_text(input_html)
        return super().html()


class HtmlForm(HtmlContainer):

    def __init__(self):
        super().__init__("form")
        self._inputs = []
        self._action = None

    def add_input(self, ainput):
        self._inputs.append(ainput)

    def html(self):
        if len(self._inputs) > 0:
            input_html = ""
            for ainput in self._inputs:
                input_html += ainput.html()

            self.set_text(input_html)
            return super().html()
        else:
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


class HtmlEncapsulaterObject(object):

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
        hto = HtmlOneLiner("hr /")
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

    def form_input(self, itype = None, iid = None, default_value = None, default_size = None):
        return HtmlFormInput(itype, iid, default_value, default_size)

    def form_select(self, aid):
        return HtmlFormSelect(aid)

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

    def button(self, text):
        b = HtmlContainer("button")
        b.set_text(text)
        return b

    def textarea(self, name, rows = 5, cols = 5):
        c = HtmlContainer("textarea")
        c.set_attr("name", name)
        c.set_attr("rows", rows)
        c.set_attr("cols", cols)
        return c

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

    def iframe(self, src):
        cont = HtmlContainer("iframe")
        cont.set_attr("src", src)
        return cont

    def script(self, src):
        cont = HtmlContainer("script")
        cont.set_attr("src", src)
        return cont

    def css_link(self, src):
        cont = HtmlContainer("link")
        cont.set_attr("href", src)
        return cont

    def css_style(self, src):
        cont = HtmlContainer("style")
        cont.set_attr("type", "text/css")
        cont.set_attr("media", "screen")
        return cont


class PageBasic(HtmlEncapsulaterObject):

    def __init__(self, handler = None):
        self._handler = handler
        self._title = "No Title"
        self._method = "GET"
        self._form = None
        self._charset = 'utf-8'
        self._style = ""
        self._path = ""
        self._args = {}
        self.css_files = []
        self.js_files = []

    def get_content_type(self):
        mapping = {
          ".html" : "text/html",
          ".htm"  : "text/html",
          ".js"   : "text/javascript",
          ".css"  : "text/css",
          ".ico"  : "image/x-icon",
          ".jpeg"  : "image/jpeg",
          ".jpg"  : "image/jpg",
          ".png"  : "image/png",
        }

        sp = os.path.splitext(self._path)
        if len(sp) > 1:
            for key in mapping:
                if sp[1] == key:
                    return mapping[key]

        return "text/html"

    def is_binary_content(self):
        mapping = [
                ".jpeg",
                ".jpg",
                ".ico",
                ".png"
        ]
        sp = os.path.splitext(self._path)
        if len(sp) > 1:
            for item in mapping:
                if sp[1] == item:
                    return True
        return False

    def set_title(self, title):
        self._title = title

    def set_charset(self, charset):
        self._charset = charset

    def get_charset(self, charset):
        return self._charset

    def set_style(self, style):
        self._style = style

    def set_method(self, method):
        self._method = method

    def get_method(self):
        return self._method

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    def get_args(self):
        return self._args

    def set_args(self, args):
        self._args = args

    #def get_post_arg(self, key):
    #    if not self._form:
    #        self._form = cgi.FieldStorage(
    #            fp=self._handler.rfile,
    #            headers=self._handler.headers,
    #            environ={'REQUEST_METHOD': 'POST'}
    #        )
    #    return self._form.getvalue(key)

    def get_client_ip(self):
        return self._client_ip

    def set_client_ip(self, client_ip):
        self._client_ip = client_ip

    def get_arg(self, arg):
        return self._args[arg]

    def has_args(self):
        return len(self._args) > 0

    def write_string(self, string):
        self._handler.wfile.write(bytes(string, "utf-8"))

    def get_page_contents(self):
        return self._page_contents

    def set_page_contents(self, page_contents):
        self._page_contents = page_contents

    def write(self, args = None):
        return "Default document"

    def get_css_text(self):
        text = ""
        for css in self.css_files:
            text += '<link rel="stylesheet" href="{0}">'.format(css)

        return text

    def get_js_text(self):
        text = ""
        for js in self.js_files:
            text += '<script type="text/javascript" src="{0}"></script>'.format(js)

        return text

    def write_all(self, args = None):
        text = self.write(args)

        complete_text = """
            <html>
            <head>
               <title>{0}</title>
               <meta charset="{1}">
               <meta name="viewport" content="width=device-width, initial-scale=1">
               <style>{2}</style>
               {3}
               {4}
            </head>
            <body>{5}</body>
            </html>""".format(self._title,
                    self._charset,
                    self._style,
                    self.get_css_text(),
                    self.get_js_text(),
                    text)

        return complete_text

    def super_write(self):
        args = self.get_args()
        complete_text = self.write_all(args)

        self.write_string(complete_text)
