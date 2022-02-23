#!/usr/bin/python
# -*- coding: <encoding name> -*-

import unittest
import logging

import simplepythonpage


class TestHtmlElement(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_page_basic_p_empty(self):
        page = simplepythonpage.PageBasic()
        p = page.p()

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == "")

    def test_page_basic_p(self):
        page = simplepythonpage.PageBasic()
        p = page.p("")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == "<p></p>")

    def test_page_basic_p_text(self):
        page = simplepythonpage.PageBasic()
        p = page.p("test_text")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == "<p>test_text</p>")

    def test_page_basic_p_attr(self):
        page = simplepythonpage.PageBasic()
        p = page.p("test_text")
        p.set_attr("id", "attr_test")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == '<p id="attr_test">test_text</p>')

    def test_page_basic_p_insert(self):
        page = simplepythonpage.PageBasic()
        p = page.p("test_text")
        p.insert(",new_text")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == '<p>test_text,new_text</p>')

    def test_page_basic_p_push(self):
        page = simplepythonpage.PageBasic()
        p = page.p("test_text")
        p.push(",new_text")

        print("P HTML: " + p.html())

        self.assertTrue(p.html() == '<p>test_text</p><p>,new_text</p>')

    def test_page_basic_form_input(self):

        page = simplepythonpage.PageBasic()
        f = page.form_input("text", "url")

        print("f HTML: " + f.html())
        self.assertTrue(f.html() == '<input type="text" id="url" name="url">')

    def test_page_basic_form_input_default_value(self):

        page = simplepythonpage.PageBasic()
        f = page.form_input("text", "url", "deeeeedbeaaaf")

        print("f HTML: " + f.html())
        self.assertTrue(f.html() == '<input type="text" id="url" name="url" value="deeeeedbeaaaf" size="13">')

    def test_page_basic_form(self):
        page = simplepythonpage.PageBasic()
        f = page.form()
        f.set_attr("action", "http://example.com")
        f.set_attr("method", "POST")

        f.add_input( page.label("Download link:", "url"))
        f.add_input( page.form_input("text", "url"))
        f.add_input( page.form_input_submit("Download"))

        print("f HTML: " + f.html())

        self.assertTrue(f.html() == '<form action="http://example.com" method="POST"><label for="url">Download link:</label><input type="text" id="url" name="url"><input type="submit" value="Download"></form>')


if __name__ == '__main__':
    unittest.main()
