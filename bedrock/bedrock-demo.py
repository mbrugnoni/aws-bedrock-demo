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
# <Insert text here>
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
