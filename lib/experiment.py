#!/usr/bin/env python3

class Experiment:
  def __init__(self,**data):
   self.metadata= data['metadata']
    

  def _required_experiment_attributes(self):
    required_attributes = [ 'EXPERIMENT_TYPE','EXPERIMENT_ONTOLOGY_URI','REFERENCE_REGISTRY_ID',
                            'ASSAY',          'EXPERIMENT_ONTOLOGY_URI' ]
    return required_attributes
 
  def get_experiment_data(self):
    experiment          = self.metadata
    required_attributes = self._required_experiment_attributes()
    experiment_data     = dict((k.lower(),v) for k,v in experiment.items() if k.upper() in required_attributes)
    return experiment_data
