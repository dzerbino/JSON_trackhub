#!/usr/bin/env python3

import re
import sys
from collections import defaultdict

class Sample:
  def __init__(self,metadata, biomaterial_type):
    self.metadata         = metadata
    self.biomaterial_type = biomaterial_type
  
  def _get_required_attributes(self):
    '''
    Create list of required samples attributes
    '''

    type = None

    if self.biomaterial_type == "Primary Cell":
      type = 'PRIMARY_CELL'
    elif self.biomaterial_type == "Primary Tissue":
      type = 'PRIMARY_TISSUE'
    elif self.biomaterial_type == "Cell Line":
      type = 'CELL_LINE'
    elif self.biomaterial_type == "Primary Cell Culture":
      type = 'PRIMARY_CELL_CULTURE'
    else:
      print('Unknown Biomaterial type: %s' % self.biomaterial_type)
      sys.exit(2)

    donor=[ 'DONOR_ID',       'DONOR_AGE',        'DONOR_HEALTH_STATUS', 'DONOR_SEX',
            'DONOR_AGE_UNIT', 'DONOR_LIFE_STAGE', 'DONOR_ETHNICITY',
          ]
    meta= ['SAMPLE_ONTOLOGY_URI',  'MOLECULE',        'DISEASE', 
           'DISEASE_ONTOLOGY_URI', 'BIOMATERIAL_TYPE'
          ]

    required={ 'CELL_LINE' :           ['BIOMATERIAL_TYPE', 'LINE',       'LINEAGE','DIFFERENTIATION_STAGE','MEDIUM','SEX'],
               'PRIMARY_CELL':         ['BIOMATERIAL_TYPE', 'CELL_TYPE' ],
               'PRIMARY_TISSUE':       ['BIOMATERIAL_TYPE', 'TISSUE_TYPE','TISSUE_DEPOT'],
               'PRIMARY_CELL_CULTURE': ['BIOMATERIAL_TYPE', 'CELL_TYPE',  'CULTURE_CONDITIONS']
             }

    list = meta + required[type]
    if type != 'CELL_LINE':
      list += donor
    return list

  def get_samples_data(self):
    '''
    create sample block for JSON hub
    '''
    sample_metadata      = self.metadata
    sample_metadata['sex'] = sample_metadata['DONOR_SEX']
    required_attributes  = self._get_required_attributes()   
    sample               = dict((k.lower(),v) for k,v in sample_metadata.items() if k.upper() in required_attributes)

    # No space allowed in the donor_age value
    if 'donor_age' in sample:
      sample['donor_age']=re.sub(r'\s+','',sample['donor_age'])
      # DONOR_LIFE_STAGE - (Controlled Vocabulary) "fetal", "newborn", "child", "adult", "unknown", "embryonic", "postnatal"
      if 'tissue_type' in sample and re.search('cord', sample['tissue_type'], flags=re.IGNORECASE):
        sample['donor_life_stage'] = "postnatal"
      elif re.search('(\d+)\s?-\s?(\d+)',sample['donor_age']):
        low, high = map(int, re.findall('\d+', sample['donor_age']))
        if low < 19 and high < 19:
          sample['donor_life_stage'] = 'child'
        elif low > 18 and high > 18:
          sample['donor_life_stage'] = 'adult'
        else:
          sample['donor_life_stage'] = 'unknown'
      elif re.search('\+$',sample['donor_age']):
        sample['donor_life_stage'] = 'adult'
      else:
        sample['donor_life_stage'] = 'unknown'
      if 'donor_age_unit' not in sample:
        sample['donor_age_unit'] = "year"
 
    if 'sex' in sample and sample['sex'] != 'Male' and sample['sex'] != 'Female':
      sample['sex'] = "Unknown"
    for attribute in required_attributes:
      if attribute.lower() not in sample or sample[attribute.lower()] is None:
        sys.stderr.write("Could not find %s in %s\n" % ( attribute, repr(sample)))

    return sample

