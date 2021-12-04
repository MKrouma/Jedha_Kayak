""" docstring to make pylint happy.
"""

# import
import os
import boto3
from dotenv import load_dotenv

# aws session
load_dotenv()
AWSS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
session = boto3.Session(aws_access_key_id=AWSS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# s3 service
s3 = session.resource("s3")

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

# upload weather and hotels data to s3
# Upload a new file
data_list = [
    "../data/temp/weather_data.csv",
    "../data/temp/hotels_booking.json",
    "../data/temp/hotels_booking.csv"
    
]

# bucket 
bucket_name = 'kayak-mahadou'
kayak_bucket = s3.Bucket(bucket_name)

# objects.key in kayak bucket
allFiles = kayak_bucket.objects.all()
existing_keys = [file.key for file in allFiles]
print(existing_keys)

# add new data in bucket
for data in data_list : 
    key = os.path.split(data)[-1]

    if not key in existing_keys : 
        s3.Bucket('kayak-mahadou').put_object(Key=key, Body=data)
    else :
        print(f"{key} exists in bucket {bucket_name}!")