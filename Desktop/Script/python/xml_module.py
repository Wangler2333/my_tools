#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/28/17 5:56 PM
@author: Saseny Zhou
@File:   xml_module.py
"""

import xml.etree.ElementTree as ET  # read
import xml.sax
import xml


# tree = ET.parse("movies.xml")
# root = tree.getroot()
# #print(root.tag)
#
# # for node in root.iter('year'):
# #     new_year = int(node.text) + 1
# #     node.text = str(new_year)
# #     node.set("updated", "yes")
# #
# # tree.write("test.xml")
# #
# for child in root:
#     print(child.tag, child.attrib)
#     for i in child:
#         print(i.tag, i.text)

class MovieHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.type = ""
        self.format = ""
        self.year = ""
        self.rating = ""
        self.stars = ""
        self.description = ""

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "movie":
            print("*****Movie*****")
            title = attributes["title"]
            print("Title: ", title)

    def endElement(self, tag):
        if self.CurrentData == "type":
            print("Type: ", self.type)
        elif self.CurrentData == "format":
            print("Format: ", self.format)
        elif self.CurrentData == "year":
            print("Year: ", self.year)
        elif self.CurrentData == "rating":
            print("Rating: ", self.rating)
        elif self.CurrentData == "stars":
            print("Stars: ", self.stars)
        elif self.CurrentData == "description":
            print("Description: ", self.description)
        self.CurrentData = ""

    def characters(self, content):
        if self.CurrentData == "type":
            print("Type: ", content)
        elif self.CurrentData == "format":
            print("Format: ", content)
        elif self.CurrentData == "year":
            print("Year: ", content)
        elif self.CurrentData == "rating":
            print("Rating: ", content)
        elif self.CurrentData == "stars":
            print("Stars: ", content)
        elif self.CurrentData == "description":
            print("Description: ", content)


if __name__ == '__main__':
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = MovieHandler()
    parser.setContentHandler(Handler)
    parser.parser("movies.xml")
