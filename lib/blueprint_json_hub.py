#!/usr/bin/env python3

import os,sys,re
from collections import defaultdict
from json_hub    import Json_hub
from experiment  import Experiment
from analysis    import Analysis
from browser     import Browser
from sample      import Sample
from dataset     import Dataset

class Blueprint_json_hub(Json_hub):
  def __init__(self,**data):
 
    '''
    set Blueprint specific default values
    '''
    data.setdefault('taxon_id',         '9606')
    data.setdefault('assembly',         'hg38')
    data.setdefault('publishing_group', 'Blueprint')
    data.setdefault('exp_key_name',     'EXPERIMENT_ID')
    data.setdefault('file_key_name',    'FILE')
    data.setdefault('sample_key_name',  'SAMPLE_ID')
    data.setdefault('epirr_key_name',   'EPIRR_ID')
    data.setdefault('analysis_key_name','FILE_TYPE')
    data.setdefault('file_type_key',    'FILE_TYPE')
    data.setdefault('email',            'blueprint-info@ebi.ac.uk')
    data.setdefault('url_prefix',       'http://ftp.ebi.ac.uk/pub/databases/')
    data.setdefault('description',      'Blueprint JSON Data hub generated for the IHEC Data Portal.')

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
    epirr_data    = self._read_file_info(self.epirr_file, self.exp_key_name)
    analysis_data = self._read_file_info(self.analysis_file, self.analysis_key_name)

    samples_dict = defaultdict(dict)
    #dataset_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
  
    for exp,entries in index_data.items():
      sample_data = self._sample_metadata(entries[0]) 
      sample_id   = entries[0][self.sample_key_name]
      '''
      add IHEC JSON specific sample information block
      '''
      samples_dict[sample_id] = sample_data  

      type_browser_list = []
      analysis_meta     = None
      exp_meta          = self._experiment_metadata(entries[0])
      exp_meta['reference_registry_id'] = epirr_data[exp][0][self.epirr_key_name]

      for experiment in entries:
        file_type = experiment[self.file_type_key]
        file_name = os.path.basename(experiment[self.file_key_name])
        exp_id    = experiment[self.exp_key_name]
  
        if re.search(r'\.(bb|bw)$',file_name): 
          '''
          skip file if its not bigwig or bigbed
          '''           
          analysis_meta       = self._analysis_metadata(analysis_data[file_type][0])
          (browser_dict,type) = self._file_dict(experiment)
         
          type_browser_list.append( { 'type':type, 'browser':browser_dict } )

      dataset = Dataset(experiment=exp_id, sample_id=sample_id, experiment_attributes=exp_meta,
                        analysis_attributes=analysis_meta, type_browser_data=type_browser_list)
      dataset_dict = dataset.get_dataset_block()

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
   
    browser = Browser( big_data_url=file_url, md5sum=experiment['FILE_MD5'],primary=True)
    browser_dict = browser.get_browser_data()
    return browser_dict,type


  def _analysis_metadata(self, analysis_data):
    '''
    Set analysis attribute for the JSON block
    '''
    analysis = Analysis( metadata=analysis_data )
    analysis_dict = analysis.get_analysis_data()
    return analysis_dict

  def _experiment_metadata(self, experiment_data):
    '''
    Set experiment attribute for JSON block
    '''
    experiment_data['assay'] = experiment_data['LIBRARY_STRATEGY']
    experiment = Experiment( metadata=experiment_data )
    exp_dict   = experiment.get_experiment_data() 
    return exp_dict

  def _sample_metadata(self, sample):
    '''
    Set samples metadata block for json hub
    '''
    sample = Sample( metadata=sample, biomaterial_type=sample['BIOMATERIAL_TYPE'] )
    sample_dict = sample.get_samples_data()
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

