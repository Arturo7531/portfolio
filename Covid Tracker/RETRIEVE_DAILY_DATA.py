# Author: Arturo Ford
"""
This file is some sample code used in a project during the pandemic.
Myself and a team of data scientists decided to build a covid tracker for our country, Panama.
My task involved building the data infrastructure required to set up a proper ETL 
and have the information saved on a cloud vendor's SQL database. 
"""

#IMPORT NECESSARY PACKAGES
import json
from pandas import DataFrame as pd
from sqlalchemy import create_engine as sql
import os
from os import listdir, chdir
from os.path import isfile, join, dirname

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#THIS IS THE MAIN FUNCTION THAT UPLOADS ALL DATA TO MYSQL DATABASE
def data_upload(filecode, connection):
    df = []
    
    with open('webscrape/corregimientos/{date}-datacovid19.json'
              .format(date = filecode), 
              'r', encoding="utf8") as f:
        try:
            data = json.load(f) #LOAD FILE AS JSON
        except:
            print("Error: JSON filecode {code} unreadable."
                  .format(code=filecode))
            success = 0
            return success
            
    parsed = data.values()
    
    for line in parsed:
        for info in line:
            df.append(info["attributes"])
            
    df = pd(df) #TURN DATA INTO A PANDAS DATAFRAME
    
    df["FECHA_CAPTURA"] = filecode[0:4]+'-'+filecode[4:6]+'-'+filecode[6:8]
    
    #SELECT ONLY NECESSARY COLUMNS
    df = df[['OBJECTID', 'PROVINCIA', 'DISTRITO', 'CORREGIMIENTO', 'CANTIDAD',
             'HOSPITALIZADO', 'AISLAMIENTO_DOMICILIARIO', 'FALLECIDO', 'UCI', 
             'RECUPERADO', 'FECHA_CAPTURA']].sort_values("OBJECTID")
            
    #print(df) #To validate data
    #print(df.dtypes) #To validate data
    #return df

    """
    filecode = '20200426'
    df = data_upload(filecode)
    print(df)
    """    
    
    #CONNECT TO MYSQL AND EXPORT DATA
    try:
        df.to_sql('data_minsa_raw', con = connection, if_exists = 'append', 
                    chunksize = 1000, index=False)
        df.to_csv('PARSED_DATA/{code}.csv'.format(code=filecode), index=False, 
                  encoding='utf-8-sig')
        success = 1
    
    except Exception as e:
        print("Error: SQL Insert failure processing filecode {code}:\n"
              .format(code=filecode))
        print(e)
        print("\n")
        success = 0
    
    return success


#CHECKS FOR ALREADY-PARSED DATA AND FINDS UNPARSED DATA TO LOAD
print("Initiating daily file upload...")
parsedfiles = [f for f in listdir('PARSED_DATA/') 
if isfile(join('PARSED_DATA/', f))]

parsed = []
for file in parsedfiles:
    file = file[0:8]
    parsed.append(file)
    

rawfiles = [f for f in listdir('webscrape/corregimientos/') 
if isfile(join('webscrape/corregimientos/', f))]

raw = []
for file in rawfiles:
    file = file[0:8]
    raw.append(file)

to_parse = [x for x in raw if x not in parsed]

#ITERATE THROUGH MISSING FILES AND RUN MAIN FUNCTION TO UPLOAD
successes = 0
total = 0
new_processed = []

if to_parse == []:
    print('Data up to date.')
else:
    print("Connecting to server...")
    connection = sql("mysql+pymysql://{user}:{pw}@{host}/{db}"
                 .format(user='REMOVED',
                         pw='REMOVED',
                         host='REMOVED',
                         db='REMOVED'))
    for filecode in to_parse:
        success = data_upload(filecode, connection) #RUNNING MAIN FUNCTION HERE
        if success == 1:
            new_processed.append(filecode) 
        else:
            pass
        successes += success
        total += 1

failures = total - successes

#REPORT BACK TO USER
if failures == 0 and to_parse != []:
    print("Successfully processed {x} files\n".format(x=successes))
    print("New files processed:")
    for i in new_processed:
        print(i)
elif to_parse == []:
    pass
else:
    print("Successfully processed {x} files. There were {y} errors.\n"
          .format(x=successes, y=failures))
    if successes > 0:
        print("New files processed:")
        for i in new_processed:
            print(i)
    else:
        pass
