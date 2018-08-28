# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 16:04:27 2018

@author: yiyuezhuo
"""

import argparse
import decoder

parser = argparse.ArgumentParser(description='SRPG studio asset extractor')
parser.add_argument('asset_path', help='The path of asset')
parser.add_argument('-o','--output', help='Output directory',default='output')
parser.add_argument('-r','--raw', 
                    help='Raw output(Default pattern output runtime file informative but wrong to custom data format)', 
                    action='store_const', const=True, default=False)
parser.add_argument('-s','--silent', help="Print nothing when processing",
                    action='store_const', const=True, default=False)

args = parser.parse_args()

decoder.setup(args.asset_path)
extract = decoder.raw_extract if args.raw else decoder.extract
extract(args.output, verbose = not args.silent)
