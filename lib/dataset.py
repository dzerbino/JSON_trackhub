#!/usr/bin/env python3

from collections import defaultdict

class Dataset:
  def __init__(self,**data):
    self.experiment            = data['experiment']
    self.sample_id             = data['sample_id']
    self.browser               = data['browser']
    self.type                  = data['type']
    self.experiment_attributes = data['experiment_attributes']
    self.analysis_attributes   = data['analysis_attributes']
    


  def get_dataset_block(self):
    '''
    Creating dataset block for the JSON hub
    '''
    dataset = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    dataset[self.experiment]['sample_id']             = self.sample_id
    dataset[self.experiment]['experiment_attributes'] = self.experiment_attributes
    dataset[self.experiment]['analysis_attributes']   = self.analysis_attributes
    dataset[self.experiment]['browser'][self.type]    = self.browser
    return dataset
