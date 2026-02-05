import json
import boto3
import os
import uuid
from botocore.config import Config


s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    try:
        table_name = os.environ.get('TABLE_NAME')
        bucket_name = os.environ.get('PHOTO_BUCKET')
        table = dynamodb.Table(table_name)

        body = event.get('body', '{}')
        data = json.loads(body) if isinstance(body, str) else body

        report_id = str(uuid.uuid4())
        # Create unique name for s3 file
        file_name = f"photos/{report_id}.jpg"

        # Generate a Presigned URL to PUT the file
        upload_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': file_name,
                'ContentType': 'image/jpeg'
            },
            ExpiresIn=300
        )

        # We save the data in DynamoDB (along with the path to the image)
        item = {
            'report_id': report_id,
            'date': data.get('date', 'no-date'),
            'track_type': data.get('trackType', 'unknown'),
            'location': data.get('location', '0,0'),
            'photo_key': file_name,  # Ścieżka w S3
            'photo_url': f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        }

        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "status": "sukces",
                "report_id": report_id,
                "upload_url": upload_url  
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
