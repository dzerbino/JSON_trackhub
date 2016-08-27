# JSON Trackhub

A repository for creating IHEC format JSON trackhub for Blueprint project 

## Usage

<pre><code>
  python3 JSON_trackhub/script/prepare_blueprint_json_hub.py -i data.index        \
                                                             -a analysis_info.txt \
                                                             -e epirr_ids.index   \
                                                             -d '2016-08-16'
</pre></code>

## Options

<pre><code>
  -h, --help            show this help message and exit
  -i INDEX_FILE,    --index_file INDEX_FILE       : Blueprint metadata index file
  -a ANALYSIS_FILE, --analysis_file ANALYSIS_FILE : Analysis information file
  -e EPIRR_FILE,    --epirr_file EPIRR_FILE       : EpiRR id list
  -d RELEASE_DATE,  --release_date RELEASE_DATE   : Data release date
</pre></code>

