"""
Todo: 

https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/Tools.CLI.html
1. aws dynamodb create-table `
    --table-name Music `
    --attribute-definitions `
        AttributeName=Artist,AttributeType=S `
        AttributeName=SongTitle,AttributeType=S `
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE `
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 `
    --endpoint-url http://localhost:4569
(*PowerShell用に編集してあります)
2. aws dynamodb list-tables --endpoint-url http://localhost:4569 
TABLENAMES      Music
3. boto3をローカルS3設定に向けてやる（後はAWS上でやるのと全部同じ）
"""

import boto3

s3 = boto3.resource('dynamodb', endpoint_url='http://localhost:4569/',  aws_access_key_id="hogehoge",aws_secret_access_key="foobar" , region_name='ap-northeast-1' )
table = s3.Table("Music")

def put_record(artist="Acme Band", songTitle="Happy Day", albumTitle="Songs About Life"):
    table.put_item(
        Item={
            'Artist': artist,
            'SongTitle' : songTitle,
            'AlbumTitle': albumTitle
        }
    )

def get_record(artist="Acme Band", songTitle="Happy Day"):
    response = table.get_item(
    Key={
        'Artist': artist,
        'SongTitle' : songTitle
        }
    )
    print(response['Item'])


def update_record(artist="Acme Band", songTitle="Happy Day", albumTitle="Songs About Me!"):
    table.update_item(    
        Key={
        'Artist': artist,
        'SongTitle' : songTitle
        },
        UpdateExpression='SET AlbumTitle = :val1',
        ExpressionAttributeValues={
            ':val1': albumTitle
        }
    )

if __name__ == '__main__':
    put_record()
    get_record()
    update_record()
    get_record()



