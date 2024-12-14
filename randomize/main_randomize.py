#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: caiazzo
@date July 2024
"""

import randomize

###############################################################################
# INPUT DATA
###############################################################################
# input XLS
xls_file = './tests/test_survey.xlsx'
# output file (CSV oder Excel)
output_filename = './tests/test_data.csv'

df_random = randomize(xls_file,data_filename=None,random_length = 200,years=[2022,2023])

if output_filename[-3:]=='csv':
    df_random.to_csv(output_filename)
elif output_filename[-4:]=='xlsx':
    df_random.to_excel(output_filename)
else:
    print(' ** wrong output format: ', output_filename)





# example: concatenate different files
# df_companies = []
# trends = [20,5,10,-10,30,15,15,25,0,10,9,40,11,15]
# for c in companies:
#     df_as = df_data[df_data['institution_name']==c]
#     df_random_1 = form.randomize(data_filename=None,df=df_as,random_length = 10,trend=trends[companies.index(c)])
#     df_random_1['institution_name']=c
#     df_random_1['year'] = [2023,2022,2021,2020,2019,2018,2017,2016,2015,2014]
#     for v in share_columns:
#         df_data[v]=df_data[v].apply(lambda x: min(x,98))
    
#     df_random_1['craft'] = df_random_1[['agriculture','craft']].apply(lambda x: round(min(100,x['craft'],100 - x['agriculture']),2),axis=1)
#     df_random_1['service'] = df_random_1[['agriculture','craft','service']].apply(lambda x: round(min(100,x['service'],100 - x['agriculture']-x['craft']),2),axis=1)
#     df_random_1['other'] = df_random_1[['agriculture','craft','service','other']].apply(lambda x: round(100 - x['agriculture'] - x['craft'] - x['service'],2),axis=1)

#     df_companies.append(df_random_1)
    
    
# df_kpi = pd.concat(df_companies)
# df_kpi.to_csv('data/kpi_microfinance_random_companies.csv')