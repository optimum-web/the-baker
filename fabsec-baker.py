#!/usr/bin/env python
#!*-* coding:utf-8 *-*

from __future__ import with_statement
from fabric.api import *


class baker:
    def __init__(self):
        print 'Welcome to "The Baker Model IV" - '
        print 'I am ready to cook up a new server.'
        check1 = ""
        while check1 != 'y':
            self.vic = raw_input("Enter new server IP: ")
            self.mu = raw_input("Enter super-user login: ")
            self.mp = raw_input("Password for super-user: ")
            print "\nOk so I got:\n"
            print "IP: %s" % self.vic
            print "Super User: %s" % self.mu
            print"Password:%s" % self.mp
            check1 = raw_input("Is this information correct (y/N)?").lower()

    def general_info(self):
        '''Retrieve hostname and some general server info'''
        print '\n Starting System check: logging in and gather base data.\n'
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("hostname")
            run("df -h")
            run("free -m")


if __name__ == '__main__':
    bake = baker()
    bake.general_info()
