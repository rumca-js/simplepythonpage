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


if __name__ == '__main__':
    unittest.main()
