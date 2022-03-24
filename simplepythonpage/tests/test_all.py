#!/usr/bin/python
# -*- coding: <encoding name> -*-

import unittest
import logging

import simplepythonpage


class TestHtmlify(unittest.TestCase):

    def setUp(self):
        pass

    def test_new_lines(self):
        text = "text\nnewline"
        htmlify = simplepythonpage.html.Htmlify(text)

        self.assertTrue(htmlify.htmlify() == "text<br/>newline")

    def test_http_link(self):
        text = "text http://instagram.com/arteconcert newline"
        htmlify = simplepythonpage.html.Htmlify(text)

        self.assertTrue(htmlify.htmlify() == 'text <a href="{0}">{0}</a> newline'.format("http://instagram.com/arteconcert"))

    def test_https_link(self):
        text = "text https://instagram.com/arteconcert newline"
        htmlify = simplepythonpage.html.Htmlify(text)

        self.assertTrue(htmlify.htmlify() == 'text <a href="{0}">{0}</a> newline'.format("https://instagram.com/arteconcert"))

    def test_http_2_links(self):
        text = "text http://instagram.com/arteconcert http://instagram.com/arteconcert newline"
        htmlify = simplepythonpage.html.Htmlify(text)

        self.assertTrue(htmlify.htmlify() == 'text <a href="{0}">{0}</a> <a href="{0}">{0}</a> newline'.format("http://instagram.com/arteconcert"))

    def test_http_new_line(self):
        text = "text http://instagram.com/arteconcert\n\nhttp://instagram.com/arteconcert newline"
        htmlify = simplepythonpage.html.Htmlify(text)

        self.assertTrue(htmlify.htmlify() == 'text <a href="{0}">{0}</a><br/><br/><a href="{0}">{0}</a> newline'.format("http://instagram.com/arteconcert"))

    def test_http_near_end(self):
        text = "text http://instagram.com/arteconcert"
        htmlify = simplepythonpage.html.Htmlify(text)

        self.assertTrue(htmlify.htmlify() == 'text <a href="{0}">{0}</a>'.format("http://instagram.com/arteconcert"))
        

class TestHtmlElement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_page_basic_p_empty(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        p = page.p()

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == "")

    def test_page_basic_p(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        p = page.p("")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == "<p></p>")

    def test_page_basic_p_text(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        p = page.p("test_text")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == "<p>test_text</p>")

    def test_page_basic_p_attr(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        p = page.p("test_text")
        p.set_attr("id", "attr_test")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == '<p id="attr_test">test_text</p>')

    def test_page_basic_p_attr_no_value(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        p = page.p("test_text")
        p.set_attr("nofullscreen", None)

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == '<p nofullscreen>test_text</p>')

    def test_page_basic_p_insert(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        p = page.p("test_text")
        p.insert(",new_text")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == '<p>test_text,new_text</p>')

    def test_page_basic_p_push(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        p = page.p("test_text")
        p.push(",new_text")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == '<p>test_text</p><p>,new_text</p>')

    def test_page_basic_form_input(self):

        page = simplepythonpage.html.HtmlEncapsulaterObject()
        f = page.form_input("text", "url")

        print("f HTML: " + f.html())
        self.assertTrue(f.html() == '<input type="text" id="url" name="url">')

    def test_page_basic_form_input_default_value(self):

        page = simplepythonpage.html.HtmlEncapsulaterObject()
        f = page.form_input("text", "url", "deeeeedbeaaaf")

        print("f HTML: " + f.html())
        self.assertTrue(f.html() == '<input type="text" id="url" name="url" value="deeeeedbeaaaf" size="13">')

    def test_page_basic_3_form_inputs(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        f = page.form()
        f.set_attr("action", "http://example.com")
        f.set_attr("method", "POST")

        f.add_input( page.label("Download link:", "url"))
        f.add_input( page.form_input("text", "url"))
        f.add_input( page.form_input_submit("Download"))

        print("f HTML: " + f.html())

        self.assertTrue(f.html() == '<form action="http://example.com" method="POST"><label for="url">Download link:</label><input type="text" id="url" name="url"><input type="submit" value="Download"></form>')

    def test_page_form_options(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        f = page.form()
        f.set_attr("action", "http://example.com")
        f.set_attr("method", "POST")

        s = page.form_select("car")
        s.add_option("volvo", "Volvo")
        s.add_option("fiat", "Fiat")

        f.add_input(s)

        f.add_input( page.form_input_submit("Download"))

        print("f HTML: " + f.html())

        self.assertTrue(f.html() == '<form action="http://example.com" method="POST"><select id="car" name="car"><option value="volvo">Volvo</option><option value="fiat">Fiat</option></select><input type="submit" value="Download"></form>')

    def test_page_form_options(self):
        page = simplepythonpage.html.HtmlEncapsulaterObject()
        f = page.form()
        f.set_attr("action", "http://example.com")
        f.set_attr("method", "POST")

        s = page.form_select("car")
        s.add_option("volvo", "Volvo")
        s.add_option("fiat", "Fiat", True)

        f.add_input(s)

        f.add_input( page.form_input_submit("Download"))

        print("f HTML: " + f.html())

        self.assertTrue(f.html() == '<form action="http://example.com" method="POST"><select id="car" name="car"><option value="volvo">Volvo</option><option value="fiat" selected>Fiat</option></select><input type="submit" value="Download"></form>')


class PageTest(simplepythonpage.html.PageBasic):

    def __init__(self):
        super().__init__()
        self.strings = ""

    def write_string(self, string):
        self.strings += string

    def write(self, args):
        self.set_title("Test Page Title")
        return "Test Page Contents"


class TestHtmlPage(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_page_basic_meta(self):

        page = PageTest()
        text = page.write_all({})
        self.assertTrue(text.find("<meta charset") > 0)

    def test_page_basic_title(self):

        page = PageTest()
        text = page.write_all({})

        self.assertTrue( len(text) > 0)
        self.assertTrue(text.find("<title>Test Page Title</title>") >= 0)

    def test_page_content_type_html(self):

        page = PageTest()
        self.assertTrue(page.get_charset().toLower() == "utf-8")

    def test_page_content_type_html(self):

        page = PageTest()
        page.set_method("GET")
        page.set_path("download/file.html")
        self.assertTrue(page.get_content_type() == "text/html")

    def test_page_content_type_htm(self):

        page = PageTest()
        page.set_method("GET")
        page.set_path("download/file.htm")
        self.assertTrue(page.get_content_type() == "text/html")

    def test_page_content_type_js(self):

        page = PageTest()
        page.set_method("GET")
        page.set_path("download/file.js")
        self.assertTrue(page.get_content_type() == "text/javascript")

    def test_page_content_type_css(self):

        page = PageTest()
        page.set_method("GET")
        page.set_path("download/file.css")
        self.assertTrue(page.get_content_type() == "text/css")




if __name__ == '__main__':
    unittest.main()
