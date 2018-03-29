#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10/28/17 3:26 PM
@author: Saseny Zhou
@File:   configparser_module.py
"""

import configparser


class _CreateConfigFile(object):
    def __init__(self, path=None):
        self.config = configparser.ConfigParser()
        self.file_path = path

    def _write_config_default(self, obj):
        try:
            self.config['DEFAULT'] = obj
            self.config.write(open(self.file_path, 'w'))
        except TypeError as e:
            print('TypeError ', e)

    def _add_others_config(self, sections, obj):
        try:
            self.config[sections] = obj
            self.config.write(open(self.file_path, 'w'))
        except TypeError as e:
            print('TypeError ', e)

    def _remove_config(self, sections):
        try:
            self.config.remove_section(sections)
            self.config.write(open(self.file_path, 'w'))
        except TypeError as e:
            print('TypeError ', e)

    def _read_config(self, sections, key):
        try:
            _read = self.config.read(self.file_path)
            return self.config.get(sections, key)
        except TypeError as e:
            print('TypeError ', e)

    def _set_config_values(self, sections, keys, values):
        try:
            self.config.set(sections, keys, values)
            self.config.write(open(self.file_path, 'w'))
        except TypeError as e:
            print('TypeError ', e)

    def _others(self, keys='DEFAULT'):
        self.sections = self.config.sections()
        self.defaults = self.config.defaults()
        self.items = self.config.items(keys)

        return self.sections, self.defaults, self.items


if __name__ == '__main__':
    pass
