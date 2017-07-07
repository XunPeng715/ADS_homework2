import json
import fnmatch
import logging
import time

json_data = open("config.json")
j_obj = json.load(json_data)

AWSAccess = j_obj['AWSAccess']
AWSSecret = j_obj['AWSSecret']


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logfile = time.strftime("%Y-%m-%d_%H:%M:%S" + ".log")

# create a file handler
handler = logging.FileHandler(logfile)
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

logger.info('Hello!!!!')




# Check the bucket was created or not
import urllib3
import boto3
import botocore

client = boto3.client('s3',
                      aws_access_key_id=AWSAccess, 
                      aws_secret_access_key=AWSSecret)
s3 = boto3.resource('s3',
                   aws_access_key_id=AWSAccess, 
                      aws_secret_access_key=AWSSecret)

BucketName = 'ZillowDataBucket'
bucket = s3.Bucket(BucketName)
client.create_bucket(Bucket=BucketName)


# check the file was in bucket or not
flag = False
filename = 'data.csv'
bucket = s3.Bucket(BucketName)
for obj in bucket.objects.all():
    if fnmatch.fnmatch(obj.key, 'data.csv'):
        logger.info(filename + ' already exists!')
        flag = True
        
print(flag)       
if flag == False:
    logger.info(filename + ' does not exists!')
    logger.info('Uploading file!')
    s3.meta.client.upload_file(filename, BucketName, filename)
elif flag == True:
    print(filename + 'is existing!')