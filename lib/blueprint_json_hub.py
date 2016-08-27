#!/usr/bin/env python3

import os,sys,re
from collections import defaultdict
from json_hub import Json_hub

class Blueprint_json_hub(Json_hub):
  def __init__(self,**data):
 
    '''
    set default values for Blueprint
    '''
    data.setdefault('email', 'blueprint-info@ebi.ac.uk')
    data.setdefault('taxon_id', 9606)
    data.setdefault('assembly', 'hg38')
    data.setdefault('description', 'Blueprint JSON Data hub generated for the IHEC Data Portal.')
    data.setdefault('publishing_group', 'Blueprint')
    data.setdefault('exp_key_name', 'EXPERIMENT_ID')
    data.setdefault('file_key_name', 'FILE')
    data.setdefault('sample_key_name', 'SAMPLE_ID')
    data.setdefault('epirr_key_name', 'EPIRR_ID')
    data.setdefault('analysis_key_name', 'FILE_TYPE')
    data.setdefault('file_type_key', 'FILE_TYPE')
    data.setdefault('url_prefix', 'http://ftp.ebi.ac.uk/pub/databases/')

    super(self.__class__, self).__init__(**data)
    self.index_file        = data['index_file']
    self.analysis_file     = data['analysis_file']
    self.epirr_file        = data['epirr_file']
    self.exp_key_name      = data['exp_key_name']      
    self.file_key_name     = data['file_key_name']     
    self.sample_key_name   = data['sample_key_name']   
    self.epirr_key_name    = data['epirr_key_name']    
    self.analysis_key_name = data['analysis_key_name'] 
    self.file_type_key     = data['file_type_key']     
    self.url_prefix        = data['url_prefix']       

  def get_json_data(self):
    '''
    Blueprint specific method
    '''

    index_data    = self._read_file_info(self.index_file, self.exp_key_name)
    epirr_data    = self._read_file_info(self.epirr_file, self.epirr_key_name)
    analysis_data = self._read_file_info(self.analysis_file, self.analysis_key_name)

    samples_dict = defaultdict(dict)
    dataset_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for exp,entries in index_data.items():
      sample_data = self._sample_metadata(entries[0]) 
      sample_id   = entries[0][self.sample_key_name]
      '''
      add IHEC JSON specific sample information block
      '''
      samples_dict[sample_id] = sample_data  
 
      for experiment in entries:
        file_type = experiment[self.file_type_key]
        file_name = os.path.basename(experiment[self.file_key_name])
        exp_id    = experiment[self.exp_key_name]

        if re.match(r'\.(bb|bw)$',file_name): 
          '''
          skip file if its not bigwig or bigbed
          '''           
          exp_meta                 = self._experiment_metadata(experiment)
          analysis_meta            = self._analysis_metadata(analysis_data[file_type][0])
          (browser_dict,type)      = self._file_dict(experiment)
          exp_meta[epirr_key_name] = epirr_data[exp][0][epirr_key_name]

          '''
          add IHEC JSON specific dataset information block
          '''        
          dataset_dict[exp_id]['analysis_attributes']   = analysis_meta
          dataset_dict[exp_id]['experiment_attributes'] = exp_meta
          dataset_dict[exp_id]['sample_id']             = sample_id     
          dataset_dict[exp_id]['browser'][type].append(browser_dict) 

    return (dataset_dict, samples_dict)
  
  def _file_dict(self,experiment):
    file_name=os.path.basename(experiment['FILE'])
    lib_strategy=experiment['LIBRARY_STRATEGY']
    url_prefix=self.url_prefix

    if file_name.endswith('bw'):
      if re.match(r'plusStrand', file_name, re.IGNORECASE):
        type='signal_forward'
      elif re.match(r'minusStrand', file_name, re.IGNORECASE):
        type='signal_reverse'
      else:
        type='signal_unstranded'
    elif file_name.endswith('bb'):
        type='peak_calls'
    else:
        type='other'

    file_url = url_prefix + experiment['FILE']
    browser_dict = defaultdict(dict)
    browser_dict['big_data_url']=file_url
    browser_dict['md5sum']=experiment['FILE_MD5']
    browser_dict['primary']=True
    return browser_dict,type

  def _required_attributes(self,type):
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
    if type not in ['CELL_LINE',]:
      list=required[type]
      list.extend(donor)
    else:
      list=required[type]
    list.extend(meta)
    return list

  def _analysis_metadata(self, analysis):
    required=[ 'ANALYSIS_GROUP',   'ALIGNMENT_SOFTWARE',  'ALIGNMENT_SOFTWARE_VERSION',
               'ANALYSIS_SOFTWARE','ANALYSIS_SOFTWARE_VERSION' ] 
    analysis_dict=dict((k.lower(),v) for k,v in analysis.items() if k in required)
    return analysis_dict

  def _experiment_metadata(self, experiment):
    required = [ 'EXPERIMENT_TYPE','EXPERIMENT_ONTOLOGY_URI','REFERENCE_REGISTRY_ID' ]
    exp_dict = dict((k.lower(),v) for k,v in experiment.items() if k in required)
    exp_dict['experiment_ontology_uri']='-'
    exp_dict['assay']=experiment['LIBRARY_STRATEGY']
    return exp_dict

  def _sample_metadata(self, sample):
    '''
    Set samples metadata block for json hub
    '''
    bio_type=sample['BIOMATERIAL_TYPE']
    if re.match(r'\bprimary\scell\b', bio_type, re.IGNORECASE):
      type = 'PRIMARY_CELL'
    elif re.match(r'\bprimary\stissue\b', bio_type, re.IGNORECASE):
      type = 'PRIMARY_TISSUE'
    elif re.match(r'cell\sline', bio_type, re.IGNORECASE):
      type = 'CELL_LINE'
    elif re.match(r'\bprimary\scell\sculture\b', bio_type, re.IGNORECASE):
      type = 'PRIMARY_CELL_CULTURE'
    else:
      print('Unknown type: %s' % bio_type)
      sys.exit(2)

    required    = self._required_attributes(type)
    sample_dict = dict((k.lower(),v) for k,v in sample.items() if k in required)

    # JSON hub validator doesn't allow space in the donor_age
    if 'donor_age' in sample_dict:
      sample_dict['donor_age']=re.sub(r'\s+','',sample_dict['donor_age'])

    # donor_life_stage & donor_age_unit missing for Blueprint samples
    sample_dict['donor_life_stage'] = 'unknown'
    sample_dict['donor_age_unit']   = 'year'
    return sample_dict

  
  def _read_file_info(self,file,key_name):
    '''
     Read an index file and a field_name
     Returns a dictionary
    '''
    infile=os.path.abspath(file)
    key_name=key_name.upper()

    if os.path.exists(infile) == False:
      print('%s not found' % infile)
      sys.exit(2)
 
    with open(infile, 'r') as f:
      header=[]
      data_list=defaultdict(list)

      for i in f:
        row=i.rstrip('\n').split("\t")
        if(header):
          filtered_dict = dict(zip(header,row))
          exp_id        = filtered_dict[key_name]
          data_list[exp_id].append(filtered_dict)
        else:
          header=list(map(str.upper, row))
          if key_name not in header:
            print('key %s not found in file %s' % (key_name, index))
            sys.exit(2)
    return data_list

