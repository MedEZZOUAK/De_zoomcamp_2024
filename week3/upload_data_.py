#upload all the parquet files to gcs bucket from the local folder

import io
import os
import requests
import pandas as pd
from google.cloud import storage



def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)
    print(f"File {local_file} uploaded to {bucket}/{object_name}.")

BUCKET = "homework3_dezoomcamp"
#cred
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/simo/Desktop/de_zoomcamp/week3/cred.json"

#upload the files to gcs
stand_parh="/home/simo/Desktop/de_zoomcamp/week3/data_green_taxi2022/green_tripdata_2022-{}.parquet"
for month in range(1, 13):
    month_str = str(month).zfill(2)  # Pad single digit months with a leading zero
    local_file=stand_parh.format(month_str)
    object_name = f"green_tripdata_2022-{month_str}.parquet"
    upload_to_gcs(BUCKET, object_name, local_file)
    print(f"Uploaded {local_file} to {BUCKET}/{object_name}.")



