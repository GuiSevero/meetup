import json
import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Documents')
    
    res = []
    
    if('query' in event["params"]["querystring"] and event["params"]["querystring"]["query"]):
        res = table.scan(FilterExpression=Attr('Text').contains(event["params"]["querystring"]["query"].lower()))
    else:
        res = table.scan()
        
    for item in res["Items"]:
        item["Url"] = 'https://s3.amazonaws.com/' + item['Bucket'] + '/' +  item['Key']
        
    return {
        'statusCode': 200,
        'count': res["Count"],
        'res': res["Items"]
    }
