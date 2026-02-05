import json
import boto3
import uuid
import os


def handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table_name = os.environ.get('TABLE_NAME')
        table = dynamodb.Table(table_name)

        if 'body' not in event:
            raw_data = event 
        else:
            raw_data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']

        report_id = str(uuid.uuid4())
        
        item = {
            'report_id': report_id,
            'date': raw_data.get('date', '2026-01-01'),
            'location': raw_data.get('location', '0,0'),
            'track_type': raw_data.get('trackType', 'nieznany'),
            'saw_wolf': raw_data.get('sawWolf', False),
            'notes': raw_data.get('notes', '')
        }
        
        table.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Zapisane!', 'id': report_id})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'received_event': str(event)})
        }