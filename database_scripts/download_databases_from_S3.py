import datetime
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
bucket_name = os.environ.get('S3_BUCKET_NAME')
access_key = os.environ.get('S3_ACCESS_KEY')
secret_key = os.environ.get('S3_SECRET_KEY')


def download_files_from_s3(pathToSaveFiles):
    print("--------------------------------------------------------------------")
    print(f"{datetime.datetime.now()}: Log")
    session = boto3.Session(aws_access_key_id=access_key,aws_secret_access_key=secret_key)
    s3_session = session.resource('s3')
    contents = s3_session.meta.client.list_objects(Bucket = bucket_name)["Contents"]
    for content in contents:
        content_name = content["Key"]
        if content_name[-4:] == ".csv":
            s3_session.meta.client.download_file(bucket_name,content_name, pathToSaveFiles + content_name)

    print("Databases were correctly downloaded from S3 bucket")
    print("--------------------------------------------------------------------")

download_files_from_s3(pathToSaveFiles = "/home/ubuntu/DataPanel/pages/Database/")
