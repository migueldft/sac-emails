from datetime import datetime
import boto3
import sagemaker

PROJECT_NAME = 'sac-emails'

CURRENT_TIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
REGION = boto3.Session().region_name
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']
CONTAINER = f'{ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{PROJECT_NAME}:latest'
AWS_SAGEMAKER_ROLE = f'arn:aws:iam::{ACCOUNT_ID}:role/datascience-sagemaker-s3-redshift'

# Create Estimator
model = sagemaker.estimator.Estimator(
    image_uri=CONTAINER,
    role=AWS_SAGEMAKER_ROLE,
    instance_count=1,
    instance_type='ml.g4dn.xlarge',
    output_path=f's3://sagemaker-{REGION}-{ACCOUNT_ID}/{PROJECT_NAME}/training_jobs/'
)

# Fit Estimator
model.fit(
    inputs={"training": f's3://sagemaker-{REGION}-{ACCOUNT_ID}/{PROJECT_NAME}/input/training_data/'},
    job_name=f'{PROJECT_NAME}-{CURRENT_TIME}'
)