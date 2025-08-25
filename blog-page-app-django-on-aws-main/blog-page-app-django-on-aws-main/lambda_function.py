# lambda_function.py - sanitized
import json
import boto3
import os
from botocore.exceptions import ClientError

# When running in Lambda with an assigned IAM role, boto3 will use the role automatically.
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME', 'your-table-name')

def lambda_handler(event, context):
    """
    Example Lambda: write S3 event data to DynamoDB.
    This function assumes the Lambda execution role has permissions for S3:GetObject and DynamoDB:PutItem.
    """
    try:
        records = event.get('Records', [])
        table = dynamodb.Table(DDB_TABLE_NAME)

        for r in records:
            s3_info = r.get('s3', {})
            bucket = s3_info.get('bucket', {}).get('name')
            key = s3_info.get('object', {}).get('key')

            # Example metadata item
            item = {
                's3_key': key,
                'bucket': bucket,
                # Add other attributes if needed, e.g., timestamp
                'processed_at': context.aws_request_id if context else 'local'
            }

            table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'processed', 'records': len(records)})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
