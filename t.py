import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id='0050e63d27947900000000006',
    aws_secret_access_key='K005WJN78p8Y98f4nB7LLFSNUqr7moY',
    endpoint_url='https://s3.us-east-005.backblazeb2.com'
)

try:
    response = s3.list_buckets()
    print("Buckets:", response['Buckets'])
except Exception as e:
    print("Error:", e)
