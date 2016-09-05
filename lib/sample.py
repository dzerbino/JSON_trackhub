#!/usr/bin/env python3

import re
from collections import defaultdict

class Sample:
  def __init__(self,**data):
    self.metadata         = data['metadata']
    self.biomaterial_type = data['biomaterial_type']
  
  def _get_required_attributes(self):
    '''
    Create list of required samples attributes
    '''

    type = None

    if re.match(r'\bprimary\scell\b', self.biomaterial_type, re.IGNORECASE):
      type = 'PRIMARY_CELL'
    elif re.match(r'\bprimary\stissue\b', self.biomaterial_type, re.IGNORECASE):
      type = 'PRIMARY_TISSUE'
    elif re.match(r'cell\sline', self.biomaterial_type, re.IGNORECASE):
      type = 'CELL_LINE'
    elif re.match(r'\bprimary\scell\sculture\b', self.biomaterial_type, re.IGNORECASE):
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
    list=[]
    if type  not in ['CELL_LINE',]:
      list=required[type]
      list.extend(donor)
    else:
      list=required[type]
    list.extend(meta)
    return list

  def get_samples_data(self):
    '''
    create sample block for JSON hub
    '''
    sample_metadata      = self.metadata
    required_attributes  = self._get_required_attributes()   
    sample               = dict((k.lower(),v) for k,v in sample_metadata.items() if k.upper() in required_attributes)

    # No space allowed in the donor_age value
    if 'donor_age' in sample:
      sample['donor_age']=re.sub(r'\s+','',sample['donor_age'])
 
    return sample

