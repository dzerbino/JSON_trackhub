#!/usr/bin/env python3

import argparse,json
from blueprint_json_hub import Blueprint_json_hub

parser=argparse.ArgumentParser()
parser.add_argument('-i','--index_file',    required=True, help='Blueprint metadata index file')
parser.add_argument('-a','--analysis_file', required=True, help='Analysis information file')
parser.add_argument('-e','--epirr_file',    required=True, help='EpiRR id list')
parser.add_argument('-d','--release_date',  required=True, help='Data release date')
args=parser.parse_args()

bp_json = Blueprint_json_hub( index_file    = args.index_file,
                              analysis_file = args.analysis_file,
                              epirr_file    = args.epirr_file,
                              date          = args.release_date
                            )

bp_json_hub = bp_json.json_hub()
print(json.dumps(bp_json_hub,indent=4))
