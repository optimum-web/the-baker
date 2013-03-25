#!/usr/bin/env python
#!*-* coding:utf-8 *-*
#
#Copyright 2013 nomad@cybermerc.org
#
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
#


from __future__ import with_statement
from fabric.api import *
from crypt import crypt


class baker():
    def __init__(self):
        self.cmds = {'1': self.yum_update, '2': self.yum_cron,
                    '3': self.create_user, '4': self.keys,
                    '5': self.ntpd, '6': self.motd, '7': self.logwatch,
                    '8': self.ssh_lockdown, '9': self.enchilada}
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
        print '\n Starting System check: logging in and gather base data.\n'
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("hostname")
            run("df -h")
            run("free -m")
        print '\nOk the system is ready to Rock & Roll...'

    def yum_update(self):
        '''RedHat update all packages'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("yum update -y")
        print'\n Done...Want some Fries with that?'

    def yum_cron(self):
        '''RedHat yum_cron script for nightly updates'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("yum install yum-cron -y")
            run("chkconfig yum-cron on")
            run("service yum-cron start")
        print'\nCompleted...Like a Boss...'

    def create_user(self):
        '''Create new user account and set password'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            self.user = prompt('Enter a username to create: ')
            run("adduser %s" % self.user)
            password = prompt('Enter a new password for user %s: ' % self.user)
            crypted_password = crypt(password, 'salt')
            run('usermod -p %s %s' % (crypted_password, self.user), pty=False)
            run("echo '%s ALL=(ALL) ALL' >> /etc/sudoers" % self.user)
        print'\nBoom...%s setup as requested. ' % self.user

    def keys(self):
        '''Install SSH keypairs (must be ran as user)'''
        self.user = prompt('Enter the username for key install: ')
        self.up = prompt('Enter password for user account: ')
        with settings(host_string=self.vic, user=self.user, password=self.up):
            run("mkdir /home/%s/.ssh" % self.user)
            run("chmod 700 /home/%s/.ssh" % self.user)
            put("./files/id_rsa.pub", "/home/%s/.ssh/authorized_keys"
               % self.user)
            run("chmod 600 /home/%s/.ssh/authorized_keys" % self.user)
        print '\nDone...Keep in mind it wont work till you configure SSH'

    def ntpd(self):
        '''Setup ntpd server, set timezone to Central'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("chkconfig ntpd on")
            run("service ntpd restart")
            run("rm -f /etc/localtime")
            run("ln -sf /usr/share/zoneinfo/America/Chicago /etc/localtime")
        print"\nIts Hammer time now..."

    def motd(self):
        '''Install prefab MotD file'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("mv /etc/motd /etc/motd.old")
            put("./files/motd", "/etc/motd")
        print"\n MOTD in the house..."

    def logwatch(self):
        '''Install and Configure Logwatch'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("yum install logwatch -y")
            run("rm -f /usr/share/logwatch/default.conf/logwatch.conf")
            put("./files/logwatch.conf",
               "/usr/share/logwatch/default.conf/logwatch.conf")
        print'\n Da Logs be getting watched...'

    def ssh_lockdown(self):
        '''Configure SSHd to my liking'''
        with settings(host_string=self.vic, user=self.mu, password=self.mp):
            run("mv /etc/ssh/sshd_config /etc/ssh/sshd_config.old")
            put("./files/sshd_config", "/etc/ssh/sshd_config")
            print"Rebooting server in 1 minutes"
            run("shutdown -r now")
        print 'This cake is BAKED...enjoy'

    def enchilada(self):
        '''Run all in one go'''
        bake.yum_update()
        bake.yum_cron()
        bake.create_user()
        bake.keys()
        bake.ntpd()
        bake.motd()
        bake.logwatch()
        bake.ssh_lockdown()
        print"All Done..."

    def menu(self):
        '''Menu of functions to call'''
        while True:
            print '\nNow what are we cooking?\n'
            print '[1] -  One time Yum update'
            print '[2] -  Install Yum-cron program'
            print '[3] -  Create user account, set passwd, add sudoer access'
            print '[4] -  Install SSH keys for a standard user account'
            print '[5] -  Setup NTPd and set timezone to Central'
            print '[6] -  Set server MOTD'
            print '[7] -  Setup Logwatch program'
            print '[8] -  Lockdown SSH (DO THIS LAST it locks out root access)'
            print '[9] -  The full enchilada build...[run process 1-8]'
            print '[10] - Nevermind, Let me out of here\n'
            cmd = raw_input("> ")
            if cmd in self.cmds:
                command = self.cmds[cmd]
                command()
            elif cmd == '10':
                print '\nPeace Out...\n'
                break
            else:
                pass

if __name__ == '__main__':
    bake = baker()
    bake.menu()
