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

    print 'Ok the system is ready to Rock & Roll...'
    print '\nNow what are we cooking?\n'
    print '[1] -  One time Yum update run'
    print '[2} -  Yum update and Yum-cron install'
    print '[3] -  Create user account and set password'
    print '[4] -  Install SSH keys for a standard user account'
    print '[5] -  Set user account to have sudo access'
    print '[6] -  Setup NTPd service'
    print '[7] -  Set server timezone (Central)'
    print '[8] -  Set server timezone (Eastern)'
    print '[9] -  Set server MOTD'
    print '[10] - Setup Logwatch program'
    print '[11] - Lockdown SSH (DO THIS LAST it locks out root access)'
    print '[12] - End program'
