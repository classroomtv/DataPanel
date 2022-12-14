import boto3
import os
import datetime
from dotenv import load_dotenv
from os import walk


load_dotenv() 
bucket_name = os.environ.get('S3_BUCKET_NAME')
access_key = os.environ.get('S3_ACCESS_KEY')
secret_key = os.environ.get('S3_SECRET_KEY')



def upload_files_to_s3(pathToFiles):
    print("--------------------------------------------------------------------")
    print(f"{datetime.datetime.now()}: Log")
    filenames = next(walk(pathToFiles), (None, None, []))[2]
    session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
    )
    s3_session = session.resource('s3') 
    for filename in filenames:
        if filename[-4:] == ".csv":
            s3_session.meta.client.upload_file(Filename=pathToFiles+filename, Bucket=bucket_name, Key=filename)

    print("Database were correctly uploaded to the S3 bucket")
    print("--------------------------------------------------------------------")

upload_files_to_s3(pathToFiles="/home/ubuntu/DataPanel/pages/Database/")
