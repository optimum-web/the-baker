#!/usr/bin/env python
#!*-* coding:utf-8 *-*

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from crypt import crypt


def general_info():
    '''Retrieve hostname and disk infomation'''
    run("hostname")
    run("df -h")


def install_epel_repo():
    '''Setup EPEL repo'''
    run("rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm")


def yum_update():
    '''RedHat update all packages'''
    run("yum update -y")


def ntpd_setup():
    '''RedHat ntpd server setup on Xen VM'''
    run("echo xen.independent_wallclock = 1 >> /etc/sysctl.conf")
    run("chkconfig ntpd on")
    run("service ntpd restart")


def set_timezone_central():
    '''RedHat set timezone to Central'''
    run("rm -f /etc/localtime")
    run("ln -sf /usr/share/zoneinfo/America/Chicago /etc/localtime")


def set_timezone_eastern():
    '''RedHat set timezone to Eastern'''
    run("rm -f /etc/localtime")
    run("ln -sf /usr/share/zoneinfo/America/New_York /etc/localtime")


def yum_cron_setup():
    '''RedHat yum_cron script for nightly RPM updates'''
    run("yum install yum-cron -y")
    run("chkconfig yum-cron on")
    run("service yum-cron start")


def motd_setup():
    '''Install prefab MotD file'''
    run("mv /etc/motd /etc/motd.old")
    put("./files/motd", "/etc/motd")


def create_user(user):
    '''Create new User account'''
    run("adduser %s" % user)


def change_password(user):
    '''Change user account password'''
    password = prompt('Enter a new password for user %s:' % user)
    crypted_password = crypt(password, 'salt')
    run('usermod -p %s %s' % (crypted_password, user), pty=False)


def setup_ssh_keyless_entry(user):
    '''Install inital SSH key pairs for user access'''
    run("mkdir /home/%s/.ssh" % user)
    run("chmod 700 /home/%s/.ssh" % user)
    put("./files/id_rsa.pub", "/home/%s/.ssh/authorized_keys" % user)
    run("chmod 600 /home/%s/.ssh/authorized_keys" % user)


def setup_logwatch():
    '''Install and Configure Logwatch'''
    run("yum install logwatch -y")
    run("rm -f /usr/share/logwatch/default.conf/logwatch.conf")
    put("./files/logwatch.conf", "/usr/share/logwatch/default.conf/logwatch.conf")


def ssh_lockdown():
    '''Configure SSHd to my liking'''
    run("mv /etc/ssh/sshd_config /etc/ssh/sshd_config.old")
    put("./files/sshd_config", "/etc/ssh/sshd_config")
    run("service sshd restart")


def add_user_to_sudo(user):
    '''Add a user to the sudoer file'''
    run("echo '%s ALL=(ALL) ALL' >> /etc/sudoers" % user)


def install_fail2ban():
    '''Install Fail2Ban (requires EPEL)'''
    run("yum install fail2ban -y")
