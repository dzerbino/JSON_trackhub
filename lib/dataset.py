#!/usr/bin/env python3

import re,sys
from collections import defaultdict

class Dataset:
  '''
  type_browser_data : [ {'type':'signal', 'browser': <Browser class output dict>}]
  '''
  def __init__(self, sample_id, browser_dict, experiment_attributes, analysis_attributes):
    self.sample_id             = sample_id
    self.browser               = browser_dict
    self.experiment_attributes = experiment_attributes
    self.analysis_attributes   = analysis_attributes
    


  def get_dataset_block(self):
    '''
    Creating dataset block for the JSON hub
    '''
    dataset_block = dict()
    dataset_block['sample_id']             = self.sample_id
    dataset_block['experiment_attributes'] = self.experiment_attributes
    dataset_block['analysis_attributes']   = self.analysis_attributes
    dataset_block['browser']               = self.browser
    return dataset_block

