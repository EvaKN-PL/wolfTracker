import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')


def handler(event, context):
    try:
        # Parsowanie body - szukamy tylko report_id
        body = json.loads(event.get('body', '{}'))
        report_id = body.get('report_id')

        if not report_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing report_id'})
            }

        table = dynamodb.Table(TABLE_NAME)

        # Operacja usunięcia
        table.delete_item(
            Key={'report_id': report_id}
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Report deleted successfully'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
