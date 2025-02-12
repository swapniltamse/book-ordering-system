import boto3
import json
import os

def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise e

    secret_string = get_secret_value_response.get('SecretString')
    if secret_string:
        return json.loads(secret_string)
    else:
        raise ValueError("SecretString is empty!")

# You can either hard-code the secret name and region here or set them via environment variables.
SECRET_NAME = os.environ.get("BOOK_ORDER_SECRET_NAME", "BookOrderSystemConfig")
DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")  

secrets = get_secret(SECRET_NAME, DEFAULT_REGION)

# Retrieve configuration values from the secret
AWS_REGION = secrets.get("AWS_REGION")
SQS_QUEUE_URL = secrets.get("SQS_QUEUE_URL")
SNS_TOPIC_ARN = secrets.get("SNS_TOPIC_ARN")

if not (AWS_REGION and SQS_QUEUE_URL and SNS_TOPIC_ARN):
    raise ValueError("One or more configuration values are missing in the secret.")
