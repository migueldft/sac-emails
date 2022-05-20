import boto3
from datetime import datetime

PROJECT_NAME = 'sac-emails'

CURRENT_TIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
REGION = boto3.Session().region_name
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']
CONTAINER = f'{ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{PROJECT_NAME}:latest'
AWS_SAGEMAKER_ROLE = f'arn:aws:iam::{ACCOUNT_ID}:role/datascience-sagemaker-s3-redshift'

client = boto3.client("sagemaker")

LAST_TRAINING_JOB = client.list_training_jobs(
    NameContains=PROJECT_NAME,
    SortBy='CreationTime',
    SortOrder='Descending'
)['TrainingJobSummaries'][0]['TrainingJobName']

response = client.create_model(
    ModelName=f'{PROJECT_NAME}-{CURRENT_TIME}',
    PrimaryContainer={
        'Image': CONTAINER,
        'Mode': 'SingleModel',
        'ModelDataUrl': f's3://sagemaker-{REGION}-{ACCOUNT_ID}/{PROJECT_NAME}/training_jobs/{LAST_TRAINING_JOB}/output/model.tar.gz'
    },
    ExecutionRoleArn=AWS_SAGEMAKER_ROLE
)