import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('weather_summary')

def lambda_handler(event, context):
    # Get query parameter 'datehour'
    datehour = event.get('queryStringParameters', {}).get('datehour')
    
    if not datehour:
        return {
            'statusCode': 400,
            'body': 'Missing datehour parameter'
        }
    
    try:
        response = table.query(
            KeyConditionExpression=Key('datehour').eq(datehour)
        )
        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': str(items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
