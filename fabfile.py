#!/usr/bin/env python
#!*-* coding:utf-8 *-*

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm


def general_info():
    '''Retrieve hostname and disk infomation'''
    run("hostname")
    run("df -h")


def yum_update():
    '''Update all RPM packages'''
    run("yum update -y")


def apt_get_upgrade():
    '''apt-get upgrade of ubuntu server'''
    run("apt-get update")
    run("apt-get upgrade -y")


def rh_ntpd_setup():
    run("echo xen.independent_wallclock = 1 >> /etc/sysctl.conf")
    run("chkconfig ntpd on")
    run("service ntpd restart")


def rh_timezone_setup():
    run("ln -sf /usr/share/zoneinfo/America/Chicago /etc/localtime")


def yum_cron_setup():
    '''Setup yum_cron script for nightly RPM updates'''
    run("yum install yum-cron -y")
    run("chkconfig yum-cron on")
    run("service yum-cron start")


def motd_setup():
    '''Install prefab MotD file'''
    run("mv /etc/motd /etc/motd.old")
    put("./files/motd", "/etc/motd")
