#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 11:20:20 2023

@author: caiazzo
"""

import pandas as pd
import random
import numpy as np

def set_year(n,years):
    year = []
    for  k in range(0,n):
        for i in range(0,len(years)):
            if k < (i+1)*n/len(years):
                year.append(years[i])
                break
    return year


def randomize(xls_file,
              df=[], # provide an initial dataframe to extend
              data_filename=None, # provide an input data set to randomly extend (considered only if df = [])
              random_length=50, #lengthof the random dataframe
              trend=0, # give an additional trend (%) to include in the data
              percentage_columns = [], # for these columns, a value between 0 and 100 is produced
              years = [] #add a year column
              ):
    
    xls_survey = pd.read_excel(xls_file,sheet_name = 'survey')
    xls_choices = pd.read_excel(xls_file,sheet_name = 'choices')
    
    if len(df)==0:
        df = pd.read_csv(data_filename) if data_filename!=None else pd.DataFrame()

    # create a random database
    df_random = pd.DataFrame()
    df_random_columns = df.columns if len(df)>0 else xls_survey['name'].values
        
    for c in df_random_columns:
        question = xls_survey[ xls_survey['name']==c]
        
        if len(question)==0:
            print(" - Column " + c + " does not have a corresponding question!")
        else:
            print(" - Processing column ", c, " ... ")
            q_type = question['type'].values[0].split(' ')
            
            # select one: pick a random choice
            if q_type[0] == 'select_one':
                list_name = q_type[1]
                list_choices = xls_choices[ xls_choices['list_name']==list_name]
                choice_values = [str(c) for c in list_choices['name'].values]
                df_random[c] = random.choices(choice_values, k=random_length)
            
            # select omultiple: pick n random choices (n between 1 and 3)
            elif q_type[0] == 'select_multiple':
                list_name = q_type[1]
                list_choices = xls_choices[ xls_choices['list_name']==list_name]
                choice_values = [str(c) for c in list(list_choices['name'].values)]
                answers = []
                for k in range(0,random_length):
                    # genderate a random number of choices - maximum 3
                    n = random.randint(1, min(3,len(choice_values)-1))
                    answers.append(' '.join(random.sample(choice_values,n)))
                df_random[c] = answers
            
            # numerical questions: give mean and std from a previous d, otherwise use 2
            elif q_type[0] == 'integer' or q_type[0] == 'decimal' or q_type[0] == 'calculate':
                mean = df[c].values[0] if (len(df)>0 and df[c].values[0]>0) else 2
                std = mean/30 if mean>10 else 0.5
                rd_values = np.random.normal(mean, std, random_length)
                
                if trend != 0:
                    for i in range(0,len(rd_values)):
                        rd_values[i] += mean * trend/100 * i/len(rd_values)
                    
                df_random[c] = rd_values #np.random.normal(mean, std, random_length)    
                    
                if q_type[0] != 'decimal':
                    df_random[c] = df_random[c].apply(lambda x: int(x))
                else:
                    if (len(df)>0 and df[c].values[0]<=1):
                        df_random[c] = df_random[c].apply(lambda x: round(max(0.1,x-int(x))),2)
                    else:
                        df_random[c] = df_random[c].apply(lambda x: round(x,1))
               
            elif q_type[0] == 'range':
                # it only works for integer parameters
                parameters = question['parameters'].values[0]
                start_p = parameters.split(';')[0].split("=")[1]
                end_p = parameters.split(';')[1].split("=")[1]
                step_p = parameters.split(';')[2].split("=")[1]
                #print(int(start_p),int(end_p),int(step_p))
                range_values = np.linspace(float(start_p),float(end_p),int((float(end_p)-float(start_p))/float(step_p)+1))
                range_values = [str(int(x)) for x in range_values]
                df_random[c] = random.choices(range_values, k=random_length)
                
            # handle also text questions with appearance numbers            
            elif q_type[0]=='text':
                if question['appearance'].values[0] == 'numbers':
                    mean = 100000
                    std = 20
                    df_random[c] = np.random.normal(mean, std, random_length)
                else:
                    # for any other text question
                    df_random[c] = "this is an example"
            else:
                print(" -- missing type: ", q_type)
    
    # add an ID column to each respondent 
    df_random['id'] = [k+1 for k in range(0,random_length)]
    if len(years)>0:
        df_random['year'] = set_year(random_length,years)
    
    return df_random


