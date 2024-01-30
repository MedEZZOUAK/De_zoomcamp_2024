#a script to download the parquet files from the web and store them locally

import io
import os
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

#loop the year using a base url
base_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{}.parquet'

for month in range(1, 13):
    month_str = str(month).zfill(2)  # Pad single digit months with a leading zero
    url = base_url.format(month_str)
    print(url) # Print the URL to track progress
    r = requests.get(url)
    # Write the file to disk
    with open(f'green_tripdata_2022-{month_str}.parquet', 'wb') as f:
        f.write(r.content)
    
