#!/usr/bin/env python
#!*-* coding:utf-8 *-*

from __future__ import with_statement
from fabric.api import *
import sys

vic = ""
master_u = ""
master_p = ""
add_user = ""


def general_info():
    '''Retrieve hostname and some general server info'''
    with settings(host_string=vic, user=master_user, password=master_pass):
        run("hostname")
        run("df -h")
        run("free -m")


if __name__ == '__main__':
    print 'Welcome to "The Baker Model IV" - '
    print 'I am ready to cook up a new server.'
    vic = raw_input("Enter new server IP: ")
    master_u = raw_input("Enter super-user login: ")
    master_p = raw_input("Password for super-user: ")
    print "Ok so I got:"
    print "IP: %s" % vic
    print "Super User: %s" % master_u
    print"Password:%s" % master_p
    check1 = raw_input("Is this information correct (Y/n)?")
    general_info()
