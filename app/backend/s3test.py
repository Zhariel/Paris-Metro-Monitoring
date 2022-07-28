import boto3
import json

s3_public = "AKIATBU6KR6FT7NILQNK"
s3_private = "+MGfbGy/amBgWYraTNTI3H+LVYjp7CBQA5pmbiCv"

client = boto3.client(service_name='sagemaker-runtime',
                      region_name='us-west-1',
                      # endpoint_url='https://sagemaker-eu-west-1-209711697803.s3.eu-west-1.amazonaws.com/sagemaker/endpoints/disruptions-endpoint/invocations',
                      endpoint_url='https://runtime.sagemaker.eu-west-1.amazonaws.com/endpoints/disruptions-endpoint/invocations',
                      aws_access_key_id=s3_public,
                      aws_secret_access_key=s3_private)

# ['is_disrupted', 'year', 'month', 'day', 'hour', 'minute', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
data = {'inputs': {'year': 2022, 'month': 7, 'day': 25, 'hour': 19, 'minute': 45, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 1}}

response = client.invoke_endpoint(
    EndpointName='disruptions-endpoint',
    Body=bytes(json.dumps(data), 'utf-8')
)

print(response["Body"].read())

# import requests
#
# url = 'https://runtime.sagemaker.eu-west-1.amazonaws.com/endpoints/disruptions-endpoint/invocations'
#
# x = requests.post(url, json = data)
#
# print(x.text)
