# coding=utf-8
import os
from Config.directory import case_dir, bus_dir


class InitSuite(object):
    def __init__(self, casetag, bustag, funtag, suitename):
        self.dir = os.path.join(case_dir, casetag, funtag, suitename)
        self.casetag = casetag
        self.bustag = bustag
        self.funtag = funtag
        self.suitetag = suitename.split('.')[0]


