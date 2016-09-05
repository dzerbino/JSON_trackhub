#!/usr/bin/env python3

class Analysis:
  def __init__(self,**data):
    self.metadata = data['metadata']

  def get_analysis_data(self):
    required_attributes = self._requited_analysis_metadata()
    analysis_metadata   = self.metadata
    analysis = dict((k.lower(),v) for k,v in analysis_metadata.items() if k.upper() in required_attributes)
    return analysis
   
  def _requited_analysis_metadata(self):
    required_attributes = [ 'ANALYSIS_GROUP',   'ALIGNMENT_SOFTWARE',  'ALIGNMENT_SOFTWARE_VERSION',
                            'ANALYSIS_SOFTWARE','ANALYSIS_SOFTWARE_VERSION' ]
    return required_attributes
