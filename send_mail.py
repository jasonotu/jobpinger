import boto3
from botocore.exceptions import ClientError
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    sender_email = config.get('sender_email')

def send_mail(subject, body, recipients):
    ses_client = boto3.client('ses', region_name='us-east-1')
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={'ToAddresses': recipients},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}},
            }
        )
        return {
            'status': 'success',
            'message_id': response['MessageId']
        }
    except ClientError as e:
        return {
            'status': 'error',
            'error_message': str(e)
        }
