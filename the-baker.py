#!/usr/bin/env python
#!*-* coding:utf-8 *-*

from __future__ import with_statement
from fabric.api import *
from crypt import crypt


class baker():
    def __init__(self):
        self.cmds = {'1': self.yum_update, '2': self.yum_cron,
                    '3': self.create_user}
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
            print"Password: %s" % self.mp
            check1 = raw_input("Is this information correct (y/N)? ").lower()

    def general_info(self):
        '''Retrieve server hostname and some general info'''
        print '\n Starting System check: logging in and gather base data.\n'
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("hostname")
            run("df -h")
            run("free -m")

    def yum_update(self):
        '''RedHat update all packages'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("yum update -y")

    def yum_cron(self):
        '''RedHat yum_cron script for nightly updates'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("yum install yum-cron -y")
            run("chkconfig yum-cron on")
            run("service yum-cron start")

    def create_user(self):
        '''Create new user account and set password'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            self.user = prompt('Enter a username to create: ')
            run("adduser %s" % self.user)
            password = prompt('Enter a new password for user %s: ' % self.user)
            crypted_password = crypt(password, 'salt')
            run('usermod -p %s %s' % (crypted_password, self.user), pty=False)

    def menu(self):
        '''Menu of functions to call'''
        while True:
            print '\nOk the system is ready to Rock & Roll...'
            print '\nNow what are we cooking?\n'
            print '[1] -  One time Yum update'
            print '[2] -  Install Yum-cron program'
            print '[3] -  Create user account and set password'
            print '[4] -  Install SSH keys for a standard user account'
            print '[5] -  Set user account to have sudo access'
            print '[6] -  Setup NTPd service'
            print '[7] -  Set server timezone (Central)'
            print '[8] -  Set server MOTD'
            print '[9] -  Setup Logwatch program'
            print '[10] - Lockdown SSH (DO THIS LAST it locks out root access)'
            print '[11] - The Full enchilada build...[ie. 1-10]'
            print '[12] - End program'
            cmd = raw_input("> ")
            if cmd in self.cmds:
                command = self.cmds[cmd]
                command()
            elif cmd == '12':
                print '\nPeace Out...\n'
                break
            else:
                pass

if __name__ == '__main__':
    bake = baker()
    bake.general_info()
    bake.menu()
