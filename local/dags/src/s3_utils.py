import boto3
import os
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv('KEY')
SECRET = os.getenv('SECRET')
REGION_NAME = os.getenv('REGION_NAME')
BUCKET = os.getenv('BUCKET')

resource = boto3.resource('s3', region_name=REGION_NAME, aws_access_key_id=KEY, aws_secret_access_key=SECRET)

bucket_resource = resource.Bucket(BUCKET) 


def upload_to_s3(filename, s3_key):
	"""
	Description: 
	"""
	bucket_resource.upload_file(filename, f"{s3_key}/{filename}")