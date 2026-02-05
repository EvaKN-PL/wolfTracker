import json
import boto3
import uuid
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])


def handler(event, context):
    try:
        data = json.loads(event['body'])
        report_id = str(uuid.uuid4())
        
        item = {
            'report_id': report_id,
            'date': data.get('date'),
            'location': data.get('location'),
            'track_type': data.get('trackType'),
            'saw_wolf': data.get('sawWolf'),
            'notes': data.get('notes')
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
            'body': json.dumps({'error': str(e)})
        }