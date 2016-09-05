#!/usr/bin/env python3

import unittest
from experiment import Experiment
from analysis   import Analysis
from browser    import Browser
from sample     import Sample
from dataset    import Dataset

class SimpleDatasetTestCase(unittest.TestCase):
  def setUp(self):
    experiment = 'ERX00001'
    sample_id  = 'ERS00001'
    experiment_attributes = { 'experiment_type':'total-RNA-Seq', 'experiment_ontology_uri':'-', 'reference_registry_id':'IHECRE00001',
                                   'assay':'RNA-Seq' }
    analysis_attributes   = { 'analysis_group':'BLUEPRINT', 'alignment_software':'BWA',  'alignment_software_version':'0.7.7',
                                   'analysis_software':'MACS2',  'analysis_software_version':'2.0.10.20131216' }
    type_browser_data     = [ {'type':'signal','browser':{ 'primary':'true', 'big_data_url':'http://ftp.ebi.ac.uk/../.bw',
                                                           'md5sum':'3a468fba40d81fd7615d8dfa197f72ed'},},
                            ]
    self.dataset = Dataset( experiment=experiment, sample_id=sample_id, experiment_attributes=experiment_attributes,
                           analysis_attributes=analysis_attributes, type_browser_data=type_browser_data )
  def test_dataset(self):
    dataset_dict = self.dataset.get_dataset_block()
    self.assertIn('ERX00001',dataset_dict)
 
class SimpleExperimentTestCase(unittest.TestCase):

  def setUp(self):
     data = {'EXPERIMENT_TYPE':'total-RNA-Seq', 'EXPERIMENT_ONTOLOGY_URI':'-',
             'REFERENCE_REGISTRY_ID':'IHECRE000001', 'ASSAY':'RNA-Seq', 'EXP_META':'E1'}
     self.experiment = Experiment( metadata=data )

  def test_exp_metadata(self):
    exp_data  = self.experiment.get_experiment_data() 
    self.assertEqual('total-RNA-Seq', exp_data['experiment_type'])  


class SimpleAnalysisTestCase(unittest.TestCase):
  
  def setUp(self):
    data={ 'ANALYSIS_GROUP':'BLUEPRINT',   'ALIGNMENT_SOFTWARE':'BWA',  'ALIGNMENT_SOFTWARE_VERSION':'0.7.7', 
                        'ANALYSIS_SOFTWARE':'MACS2','ANALYSIS_SOFTWARE_VERSION':'2.0.10.20131216'}
    self.analysis = Analysis( metadata=data ) 
  
  def test_analysis_metadata(self):
    analysis_data = self.analysis.get_analysis_data()
    self.assertEqual('BWA', analysis_data['alignment_software'])

class SimpleBrowserTestCase(unittest.TestCase):
  def setUp(self):
    self.browser = Browser( primary='true', big_data_url='http://ftp.ebi.ac.uk/../.bw', md5sum='3a468fba40d81fd7615d8dfa197f72ed')
  
  def test_browser_metadata(self):
    browser_data = self.browser.get_browser_data()
    self.assertEqual('3a468fba40d81fd7615d8dfa197f72ed', browser_data['md5sum'])

class SimpleSampleTestCase(unittest.TestCase):
  def setUp(self):
    data = { 'DONOR_ID': 'A1',        'DONOR_AGE':'0 - 5',                  'DONOR_HEALTH_STATUS':'NA', 
             'DONOR_SEX':'Female',
             'DONOR_AGE_UNIT':'year', 'DONOR_LIFE_STAGE':'unknown',         'DONOR_ETHNICITY':'NA',
             'SAMPLE_ONTOLOGY_URI':'http://url',  'MOLECULE':'genomic DNA', 'DISEASE':'None',
             'BIOMATERIAL_TYPE':'Primary Cell',   'CELL_TYPE':'Monocyte' ,  'CELL_LINE':'None'
           }
    self.sample = Sample( metadata=data, biomaterial_type='primary cell' )

  def test_sample_metadata(self):
    sample_data = self.sample.get_samples_data() 
    self.assertEqual('Monocyte', sample_data['cell_type'])
    self.assertEqual('0-5', sample_data['donor_age'])
    self.assertNotIn('cell_line', sample_data)
 
  
if __name__ == '__main__':
    unittest.main()
