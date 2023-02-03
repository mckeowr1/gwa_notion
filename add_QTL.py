import csv
import argparse


from typing import Dict, Any

from lib.notion import NotionDBInterface
from lib.preproc import format_entry


csv_file = open("test_qtl.tsv", 'r+')
csv_reader = csv.DictReader(csv_file, delimiter='\t')

ws="cb4c9ed3a9034eb09b0a3091a67d510a"
pin="secret_Q5cktwWfIrqQK6udE6LK5A6Nb0B5QwSvmgVSlJuuooz"
notion = NotionDBInterface(ws, pin)

for i, row in enumerate(csv_reader):

    formatted_entry = {
        'ID':      {'type': 'title',        'value': row['marker']},
        'Phenotype':     {'type': 'multi_select', 'value': [row['trait']]},
        'log10p':      {'type': 'text',        'value': row['log10p']},
        'startPOS':      {'type': 'text',        'value': row['startPOS']},
        'peakPOS':      {'type': 'text',        'value': row['peakPOS']},
        'endPOS':      {'type': 'text',        'value': row['endPOS']},
        'peak_id':      {'type': 'text',        'value': row['peak_id']},
        'narrow_h2':      {'type': 'text',        'value': row['narrow_h2']},
    }
    
    notion.create_page(formatted_entry)