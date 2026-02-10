import json
import boto3
import uuid
import os

# Inicjalizacja klientów AWS
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Pobieranie nazw z Terraform (zmienne środowiskowe)
BUCKET_NAME = os.environ.get('BUCKET_NAME')
TABLE_NAME = os.environ.get('TABLE_NAME')


def lambda_handler(event, context):
    try:
        # Parsowanie danych z aplikacji
        body = json.loads(event['body'])

        # Wyciągamy dane i nową flagę hasPhoto
        date = body.get('date')
        track_type = body.get('trackType')
        location = body.get('location')
        # Domyślnie False jeśli brak klucza
        has_photo = body.get('hasPhoto', False)

        report_id = str(uuid.uuid4())
        upload_url = None
        photo_key = None

        # LOGIKA: Generujemy URL tylko jeśli has_photo jest True
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

        # Przygotowanie rekordu do bazy DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        item = {
            'reportId': report_id,
            'date': date,
            'trackType': track_type,
            'location': location
        }

        # Dodajemy informację o zdjęciu tylko jeśli faktycznie istnieje
        if photo_key:
            item['photoUrl'] = f"https://{BUCKET_NAME}.s3.amazonaws.com/{photo_key}"

        # Zapis w bazie
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Report saved successfully',
                'report_id': report_id,
                'upload_url': upload_url 
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Internal Server Error'})
        }
