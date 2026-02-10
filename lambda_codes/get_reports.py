import json
import boto3
import os
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')


def handler(event, context):
    try:
        table = dynamodb.Table(TABLE_NAME)

        query_params = event.get('queryStringParameters', {}) or {}
        start_date = query_params.get('startDate')

        if start_date:
            response = table.scan(
                FilterExpression=Attr('date').gt(start_date)
            )
        else:
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
