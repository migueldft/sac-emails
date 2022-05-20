#%%
import boto3
import time
from datetime import datetime

PROJECT_NAME = 'sac-emails'

CURRENT_TIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
REGION = boto3.Session().region_name
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']
CONTAINER = f'{ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{PROJECT_NAME}:latest'
AWS_SAGEMAKER_ROLE = f'arn:aws:iam::{ACCOUNT_ID}:role/datascience-sagemaker-s3-redshift'

client = boto3.client("sagemaker")

# Delete EndpointConfig if exists
try:
    client.delete_endpoint_config(EndpointConfigName=f'{PROJECT_NAME}-endpoint')
    time.sleep(5)
except:
    pass

# Delete Endpoint if exists
try:
    client.delete_endpoint(EndpointName=f'{PROJECT_NAME}-endpoint')
    time.sleep(5)
except:
    pass

LAST_MODEL = client.list_models(
    NameContains=PROJECT_NAME,
    SortBy='CreationTime',
    SortOrder='Descending'
)['Models'][0]['ModelName']

client.create_endpoint_config(
    EndpointConfigName=f'{PROJECT_NAME}-endpoint',
    ProductionVariants=[
        {
            'VariantName': 'AllTraffic',
            'ModelName': LAST_MODEL,
            'InitialInstanceCount': 1,
            'InstanceType': 'ml.t2.large',
            'InitialVariantWeight': 1
        }
    ],
)

client.create_endpoint(
    EndpointName=f'{PROJECT_NAME}-endpoint',
    EndpointConfigName=f'{PROJECT_NAME}-endpoint'
)