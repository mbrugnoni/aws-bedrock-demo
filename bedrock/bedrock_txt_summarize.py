import json
import os
import sys
from IPython.display import display_markdown,Markdown,clear_output
import boto3

module_path = ".."
sys.path.append(os.path.abspath(module_path))
# from utils import bedrock, print_ww


# ---- ⚠️ Un-comment and edit the below lines as needed for your AWS setup ⚠️ ----

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"  # E.g. "us-east-1"
os.environ["AWS_PROFILE"] = "bedrock-work"
# os.environ["BEDROCK_ASSUME_ROLE"] = "<YOUR_ROLE_ARN>"  # E.g. "arn:aws:..."


boto3_bedrock = bedrock.get_bedrock_client(
    assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
    region=os.environ.get("AWS_DEFAULT_REGION", None)
)



prompt = """

Human: Please provide a summary of the following text.
<text>
AWS took all of that feedback from customers, and today we are excited to announce Amazon Bedrock, \
a new service that makes FMs from AI21 Labs, Anthropic, Stability AI, and Amazon accessible via an API. \
Bedrock is the easiest way for customers to build and scale generative AI-based applications using FMs, \
democratizing access for all builders. Bedrock will offer the ability to access a range of powerful FMs \
for text and images—including Amazons Titan FMs, which consist of two new LLMs we’re also announcing \
today—through a scalable, reliable, and secure AWS managed service. With Bedrock’s serverless experience, \
customers can easily find the right model for what they’re trying to get done, get started quickly, privately \
customize FMs with their own data, and easily integrate and deploy them into their applications using the AWS \
tools and capabilities they are familiar with, without having to manage any infrastructure (including integrations \
with Amazon SageMaker ML features like Experiments to test different models and Pipelines to manage their FMs at scale).
</text>

Assistant:"""

body = json.dumps({"prompt": prompt,
                 "max_tokens_to_sample":4096,
                 "temperature":0.5,
                 "top_k":250,
                 "top_p":0.5,
                 "stop_sequences":[]
                  })

modelId = 'anthropic.claude-v2' # change this to use a different version from the model provider
accept = 'application/json'
contentType = 'application/json'

# response = boto3_bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
# response_body = json.loads(response.get('body').read())

# print_ww(response_body.get('completion'))

# response = boto3_bedrock.invoke_model_with_response_stream(body=body, modelId=modelId, accept=accept, contentType=contentType)
# stream = response.get('body')
# output = list(stream)
# output

response = boto3_bedrock.invoke_model_with_response_stream(body=body, modelId=modelId, accept=accept, contentType=contentType)
stream = response.get('body')
output = []
i = 1
if stream:
    for event in stream:
        chunk = event.get('chunk')
        if chunk:
            chunk_obj = json.loads(chunk.get('bytes').decode())
            text = chunk_obj['completion']
            clear_output(wait=True)
            output.append(text)
            display_markdown(Markdown(''.join(output)))
            i+=1