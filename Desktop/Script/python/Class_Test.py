#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Account(object):
    num_accounts = 0

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        Account.num_accounts += 1

    def __del__(self):
        Account.num_accounts -= 1

    def deposit(self, amt):
        self.balance = self.balance + amt

    def withdraw(self, amt):
        self.balance = self.balance - amt

    def inquiry(self):
        return self.balance


a = Account("Guido", 1000.00)
b = Account("Bill", 10.00)

a.deposit(100.00)
b.deposit(50.00)

name = a.name