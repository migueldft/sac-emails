PROJECT_NAME = sac-emails

# Local Tests
build-docker:
	cd container; docker build  -t ${PROJECT_NAME} .

train: build-docker
	cd container/local_test; ./train_local.sh ${PROJECT_NAME}

serve: build-docker
	cd container/local_test; ./serve_local.sh ${PROJECT_NAME}

predict: build-docker
	cd container/local_test; ./predict.sh payload.json

# AWS
build-and-push:
	cd container; ./build_and_push.sh ${PROJECT_NAME}

create-training-job:
	cd aws_scripts; python3 create_training_job.py

create-model:
	cd aws_scripts; python3 create_model.py

create-batch-transform-job:
	cd aws_scripts; python3 create_batch_transform_job.py

deploy-model:
	cd aws_scripts; python3 deploy_model.py