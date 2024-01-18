#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd 
from sqlalchemy import create_engine
from time import time
import argparse
import os 
import pyarrow.parquet as pq



def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    database=params.database
    table=params.table
    url=params.url
    gzip_name='output.csv.gz'
    csv_name='output.csv'
    
    #download the csv file
    os.system(f'wget {url} -O {gzip_name}')
    #unzip the file
    os.system(f'gunzip {gzip_name}')
    #read the csv file from the disk
    df=pd.read_csv(csv_name)
    #create the engine and load the data
    engine= create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    df_itter = pd.read_csv(csv_name,iterator=True,chunksize=100000)

    df=next(df_itter)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)


    df.head(n=0).to_sql(name=table,con=engine,if_exists='replace')
    df.to_sql(name=table,con=engine,if_exists='append')

    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    while True:
        try:
            start = time()
            df = next(df_itter)
            df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)
            df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
            df.to_sql(name=table,con=engine,if_exists='append')
            logging.info("Chunk loaded in {} seconds".format(time() - start))
        except StopIteration:
            logging.info("Iteration is stopped.")
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingestion script')
    #user, password, host, port, database 
    #url for the csv file

    parser.add_argument('--user',help='database user name')
    parser.add_argument('--password',help='database password')
    parser.add_argument('--host',help='database host')
    parser.add_argument('--port',help='database port')
    parser.add_argument('--database',help='database name')
    parser.add_argument('--table',help='table name')
    parser.add_argument('--url',help='url for the csv file')

    args = parser.parse_args()
    main(args)











