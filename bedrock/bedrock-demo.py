import os
import json
import boto3

session = boto3.Session(
    profile_name="bedrock-work"
) #sets the profile name to use for AWS credentials

bedrock = session.client(
  service_name='bedrock-runtime', 
  region_name="us-east-1"
)

#S3 conect
s3 = session.client('s3')

#S3 object we are referring to
s3_object = s3.get_object(Bucket='demobucket-mjb-1', Key='demofile.txt')

#open S3 file content
file_content = s3_object['Body'].read()

#Convert content to string
text = file_content.decode('utf-8')

# prompt = """
# Give me a title for the following text:
# Amazon Bedrock is a managed container runtime that allows you to run serverless containers on AWS. It is designed to simplify the deployment and management of containerized applications, making it easier to build and run containerized workloads at scale.
# To get started with Amazon Bedrock, you will need to create an AWS account and install the AWS CLI (Command Line Interface) on your local machine. Once you have the AWS CLI installed, you can use the following steps to create and deploy a containerized application using Amazon Bedrock:
# 1. Create an Amazon EC2 instance: The first step is to create an Amazon EC2 instance that will serve as the host for your containerized application. You can use the AWS CLI to create an EC2 instance with the desired specifications, such as the instance type, region, and security group.
# 2. Install Docker: Once the EC2 instance is created, you will need to install Docker on the instance. Docker is a popular containerization platform that allows you to build, run, and manage containers. You can follow the instructions on the Docker website to install Docker on your EC2 instance.
# 3. Build your container image: Next, you will need to build a container image for your application. You can use a Dockerfile to define the steps required to build your container image, including the base image, dependencies, and application code. Once the Dockerfile is created, you can use the docker build command to build the container image.
# 4. Push the container image to Amazon ECR: Amazon Elastic Container Registry (ECR) is a fully managed container registry that makes it easy to store and share container images. You can use the AWS CLI to create an ECR repository and then push your container image to the repository.
# 5. Create an Amazon Bedrock stack: Amazon Bedrock uses stacks to organize and manage your containerized applications. You can use the AWS CLI to create a new Bedrock stack and specify the EC2 instance, container image, and other required settings.
# 6. Deploy the containerized application: Once the Bedrock stack is created, you can use the AWS CLI to deploy the containerized application to the Bedrock stack. This will start the containerized application on the EC2 instance and make it available to users.
# By following these steps, you can create and deploy a containerized application using Amazon Bedrock. Amazon Bedrock provides a fully managed container runtime that simplifies the deployment and management of containerized applications, making it easier to run containerized workloads at scale on AWS.
# """

# Open local text file
# pfile = open('test-file.txt','r')

# Read local text file
# prompt = pfile.read()

# Set prompt to 
prompt = text

body = json.dumps({
    "prompt": prompt,
    "max_tokens": 1000,
    "temperature": 0.75,
    "p": 0.01,
    "k": 0,
})

modelId = 'cohere.command-text-v14'
accept = 'application/json'
contentType = 'application/json'

response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

response_body = json.loads(response.get('body').read())

print(response_body['generations'][0]['text'])