#!/usr/bin/env python3

import os,sys,re
from collections import defaultdict
from json_hub    import Json_hub
from experiment  import Experiment
from analysis    import Analysis
from browser     import Browser
from sample      import Sample
from dataset     import Dataset

def get_file_type(file_name):
  if file_name.endswith('bw'):
    if re.search(r'plusStrand', file_name, re.IGNORECASE):
      type='signal_forward'
    elif re.search(r'minusStrand', file_name, re.IGNORECASE):
      type='signal_reverse'
    else:
      type='signal_unstranded'
  elif file_name.endswith('bb'):
    type='peak_calls'
  else:
    type='other'
  return type

class Blueprint_json_hub(Json_hub):
  def __init__(self,**data):
 
    '''
    set Blueprint specific default values
    '''
    data.setdefault('taxon_id',         9606)
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
    dataset_dict = dict() 

    exp_ontology_dict={
     'ChIP-Seq':'http://www.ebi.ac.uk/efo/EFO_0002692',
     'Bisulfite-Seq':'http://www.ebi.ac.uk/efo/EFO_0002761',
     'DNase-Hypersensitivity':'http://www.ebi.ac.uk/efo/EFO_0002693',
     'mRNA-Seq':'http://www.ebi.ac.uk/efo/EFO_0002770'
    }
  
    for exp,entries in index_data.items():
      # Remove files that are not bigwig or bigbed
      filtered_entries = list(filter(lambda entry: self.file_key_name in entry and re.search(r'\.(bb|bw)$',entry[self.file_key_name]) is not None, entries))
      if len(filtered_entries) == 0:
        continue

      first_entry = filtered_entries[0]

      sample_id   = first_entry[self.sample_key_name]
      sample_data = self._sample_metadata(first_entry) 
      samples_dict[sample_id] = sample_data  

      exp_meta          = self._experiment_metadata(first_entry)
      if exp not in epirr_data:
        continue
      exp_meta['reference_registry_id'] = epirr_data[exp][0][self.epirr_key_name]
      file_type         = first_entry[self.file_type_key]
      analysis_meta     = self._analysis_metadata(analysis_data[file_type][0])

      # Blueprint experiment metadata doesn't have experiment_ontology_uri
      assert exp_meta['assay'] in exp_ontology_dict, print("Failed to find EFO for %s" % exp_meta['assay'])
      exp_meta['experiment_ontology_uri']=exp_ontology_dict[exp_meta['assay']]

      browser_dict = defaultdict(list)
      for entry in filtered_entries:
        (track_type, browser_info) = self._file_dict(entry, exp_meta['assay'])
        browser_dict[track_type].append(browser_info)

      dataset_dict[exp] = Dataset(sample_id=sample_id, 
                                  experiment_attributes=exp_meta,
                                  analysis_attributes=analysis_meta, 
                                  browser_dict=browser_dict).get_dataset_block()

    return (dataset_dict, samples_dict)
  
  def _file_dict(self,entry, assay):
    file_name=os.path.basename(entry['FILE'])
    lib_strategy=entry['LIBRARY_STRATEGY']
    url_prefix=self.url_prefix

    type = get_file_type(file_name)
    if assay == 'ChIP-Seq' or assay == 'DNase-Hypersensitivity':
      primary = True
    elif assay == 'Bisulfite-Seq':
      primary = ((re.search(r'bs_call', file_name) is not None) and (re.search(r'hypo_meth', file_name) is None))
    elif assay == 'mRNA-Seq':
      primary = (re.search(r'Multi', file_name) is not None)
    else:
      assert False, print("Assay type %s unknown" % assay)

    file_url = url_prefix + entry['FILE']
   
    browser = Browser( big_data_url=file_url, md5sum=entry['FILE_MD5'],primary=primary)
    browser_dict = browser.get_browser_data()
    return type, browser_dict


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
            print('key %s not found in file %s' % (key_name, infile))
            sys.exit(2)
    return data_list


