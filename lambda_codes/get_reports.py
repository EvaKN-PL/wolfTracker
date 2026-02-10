import json
import boto3
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')


def handler(event, context):
    try:
        table = dynamodb.Table(TABLE_NAME)

        # Pobieramy parametry z zapytania URL (np. ?startDate=2026-01-01)
        query_params = event.get('queryStringParameters', {}) or {}
        start_date = query_params.get('startDate')

        if start_date:
            # Pobierz tylko wpisy nowsze niż start_date
            response = table.scan(
                FilterExpression=Attr('date').gt(start_date)
            )
        else:
            # Jeśli brak parametru, domyślnie pobierz np. ostatnie 20
            response = table.scan(Limit=50)

        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items)
        }
    except Exception as e:
        print(str(e))
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
