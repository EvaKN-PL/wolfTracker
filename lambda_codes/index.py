import json
import boto3
import uuid
import os

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


BUCKET_NAME = os.environ.get('PHOTO_BUCKET')
TABLE_NAME = os.environ.get('TABLE_NAME')


def handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    try:
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})

        date = body.get('date')
        track_type = body.get('trackType', 'unknown')
        location = body.get('location', '0,0')
        has_photo = body.get('hasPhoto', False)
        notes = body.get('notes', '')

        report_id = str(uuid.uuid4())
        upload_url = None
        photo_key = None

        # Logika S3
        if has_photo and BUCKET_NAME:
            photo_key = f"photos/{report_id}.jpg"
            upload_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': BUCKET_NAME,
                    'Key': photo_key,
                    'ContentType': 'image/jpeg'
                },
                ExpiresIn=3600
            )

        # Zapis do DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        item = {
            'report_id': report_id,
            'date': date,
            'trackType': track_type,
            'location': location,
            'notes': notes
        }

        if photo_key:
            item['photoUrl'] = f"https://{BUCKET_NAME}.s3.amazonaws.com/{photo_key}"

        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'message': 'Report saved',
                'report_id': report_id,
                'upload_url': upload_url
            })
        }

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
