#!/usr/bin/env python3

from collections import defaultdict

class Browser:
  def __init__(self, primary, md5sum, big_data_url ):
    self.primary      = primary
    self.md5sum       = md5sum
    self.big_data_url = big_data_url
 
  def get_browser_data(self):
    '''
    Create Browser block for the JSON hub
    '''
    browser = defaultdict(dict)
    browser['md5sum']       = self.md5sum
    browser['primary']      = self.primary
    browser['big_data_url'] = self.big_data_url
    return browser
