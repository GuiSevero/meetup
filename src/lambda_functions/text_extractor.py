import json
import boto3

def lambda_handler(event, context):
    
    client = boto3.client('textract')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Documents')

    record=event['Records'][0]
    bucket=record['s3']['bucket']['name']
    document=record['s3']['object']['key']
  
    # Analyze document with Textract
    response = client.analyze_document(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}},
        FeatureTypes=['FORMS'])

    key_map, value_map, block_map = get_kv_map(response['Blocks'])

    # Get Key Value relationship
    kvs = get_kv_relationship(key_map, value_map, block_map)
    
    # Extract text
    text = extract_text(response["Blocks"])
   
   # Save all data into DynamoDb
    table.put_item(Item={"Key": document
        , "Bucket": bucket
        , "S3Record": record
        , "Data": json.dumps(response)
        , "Text": text
        , "Form": json.dumps(kvs)})
        
    item = table.get_item(Key={"Key": document})
    
    return {
        'statusCode': 200,
        'body': response
    }
    
    
def get_kv_map(blocks):

    # get key and value maps
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block

    return key_map, value_map, block_map


def get_kv_relationship(key_map, value_map, block_map):
    kvs = {}
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key] = val
    return kvs


def find_value_block(key_block, value_map):
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '    

                                
    return text


def print_kvs(kvs):
    for key, value in kvs.items():
        print(key, ":", value)


def extract_text(blocks):
    text = ''
    for item in blocks:
        if item["BlockType"] == "LINE":
            text += ' ' + item["Text"].lower()            

    return text