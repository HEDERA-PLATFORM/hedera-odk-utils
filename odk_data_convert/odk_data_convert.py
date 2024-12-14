#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 17:14:02 2021

@author: caiazzo
"""
import sys
import pandas as pd

#print(f"Arguments count: {len(sys.argv)}")
#for i, arg in enumerate(sys.argv):
#    print(f"Argument {i:>6}: {arg}")
 
if len(sys.argv)<3:
    print('** ERROR: I need at least two arguments (input and output files **')

else: 
    file_in = sys.argv[1]
    file_out = sys.argv[2]

    if len(sys.argv)>3:
        sheet = sys.argv[3]
    else:
        sheet = None




#file_in = '/Users/caiazzo/HEDERA/CODES/table-search-app/info/mfis_world.xlsx'
#file_out = "/Users/caiazzo/HEDERA/CODES/table-search-app/info/africa.json"

    # find file and ending
    
    ending_in = file_in[file_in.rfind('.')+1:]
    ending_out = file_out[file_out.rfind('.')+1:]
    
    
    print(" ** converting from ", ending_in, " into ", ending_out, ' **')
    
    if ending_in == 'xlsx' or ending_in == 'xls':
        if sheet==None:
            df = pd.read_excel(file_in)
        else:
            df = pd.read_excel(file_in,sheet_name = sheet)
        df.columns = [c[c.rfind("-")+1:] for c in df.columns]
        
        if ending_out == 'csv':
            df.to_csv(file_out,index=False)
            
        elif ending_out == 'json':\
            df.to_json(file_out,orient='records')
            
        else:
            print(' ** ERROR: I do not know yet how to convert to ', ending_out)        
    
    
    elif ending_in == 'csv':
        df = pd.read_csv(file_in)
        df.columns = [c[c.rfind("-")+1:] for c in df.columns]
        
        if ending_out == 'xlsx' or ending_out == 'xls':
            df.to_excel(file_out)
            
        else:
            print(' ** ERROR: I do not know yet how to convert to ', ending_out)         
    
    
    else:
        print(' ** ERROR: I do not know yet how to convert from ', ending_in)  
    
