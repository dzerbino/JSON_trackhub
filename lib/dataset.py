#!/usr/bin/env python3

import re,sys
from collections import defaultdict

class Dataset:
  '''
  type_browser_data : [ {'type':'signal', 'browser': <Browser class output dict>}]
  '''
  def __init__(self, experiment, sample_id, type_browser_data, experiment_attributes, analysis_attributes):
    self.experiment            = experiment
    self.sample_id             = sample_id
    self.type_browser_data     = type_browser_data
    self.experiment_attributes = experiment_attributes
    self.analysis_attributes   = analysis_attributes
    


  def get_dataset_block(self):
    '''
    Creating dataset block for the JSON hub
    '''
    dataset = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    dataset[self.experiment]['sample_id']             = self.sample_id
    dataset[self.experiment]['experiment_attributes'] = self.experiment_attributes
    dataset[self.experiment]['analysis_attributes']   = self.analysis_attributes

    for browser_line in self.type_browser_data:
      type    = browser_line['type']
      browser = browser_line['browser']
      dataset[self.experiment]['browser'][type].append(browser)
    return dataset

