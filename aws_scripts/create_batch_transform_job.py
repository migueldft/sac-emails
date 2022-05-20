import boto3
from datetime import datetime

PROJECT_NAME = 'sac-emails'

CURRENT_TIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
REGION = boto3.Session().region_name
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']
CONTAINER = f'{ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{PROJECT_NAME}:latest'
AWS_SAGEMAKER_ROLE = f'arn:aws:iam::{ACCOUNT_ID}:role/datascience-sagemaker-s3-redshift'

client = boto3.client("sagemaker", region_name="us-east-1")

LAST_MODEL = client.list_models(
    NameContains=PROJECT_NAME,
    SortBy='CreationTime',
    SortOrder='Descending'
)['Models'][0]['ModelName']

create_batch = client.create_transform_job(
    TransformJobName=f'{PROJECT_NAME}-{CURRENT_TIME}',
    ModelName=LAST_MODEL,
    # MaxConcurrentTransforms=0,
    MaxPayloadInMB=20,
    BatchStrategy='MultiRecord',
    TransformInput={
        'DataSource': {
            'S3DataSource': {
                'S3DataType': 'S3Prefix',
                'S3Uri': f's3://sagemaker-{REGION}-{ACCOUNT_ID}/{PROJECT_NAME}/input/payload.json'
            }
        },
        'ContentType': 'application/json'
        # 'SplitType': 'Line'
    },
    TransformOutput={
        'S3OutputPath': f's3://sagemaker-{REGION}-{ACCOUNT_ID}/{PROJECT_NAME}/output/'
    },
    TransformResources={
        'InstanceType': 'ml.m5.xlarge',
        'InstanceCount': 1
    }
)