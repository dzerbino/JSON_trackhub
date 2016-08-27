#!/usr/bin/env python3

import os,sys
import re

class Json_hub:
  def __init__(self, **data):
    self.email            = data['email']
    self.date             = data['date']
    self.taxon_id         = data['taxon_id']
    self.assembly         = data['assembly']
    self.description      = data['description']
    self.publishing_group = data['publishing_group']

  def hub_data(self):
    hub_dict = { 'taxon_id'         : self.taxon_id,
                 'description'      : self.description,
                 'assembly'         : self.assembly, 
                 'publishing_group' : self.publishing_group,
                 'date'             : self.date,
                 'email'            : self.email
               }

    return hub_dict

  def get_json_data(self):
    '''
    add project specific method
    '''
    dataset_dict={}
    sample_dict={}
    return dataset_dict,sample_dict
 

  def json_hub(self):
    '''
    IHEC JSON structure
    '''
    hub_dict = self.hub_data()
    (dataset_dict, samples_dict) = self.get_json_data()

    json_obj={ 'hub_description' : hub_dict, 
               'datasets'        : dataset_dict, 
               'samples'         : samples_dict
             }
    return json_obj
    
