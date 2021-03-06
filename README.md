# aws_localsample

 ## まず初めに
* AWS SAM　CLI & Dockerを[インストール](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install-windows.html) 
* [LocalStack](https://github.com/localstack/localstack)を以下のようにインストール　
```bash
pip install localstack
```
* このリポジトリをローカル環境にコピー
```bash
git clone https://github.com/shinkawk/aws_localsample.git
```
* コピーしたリポジトリの中でLocalStackのImageを作成＆起動
```bash
docker-compose up -d
```

## Local S3 サンプル


上記のDocker-compose up -dが正常に起動したことを確認すること
* AWS S3のローカルバケットを作成
```bash
aws --endpoint-url=http://localhost:4572 s3 mb s3://demo-bucket
```
* 作成したバケットに読み込み権限を付与
```bash
aws --endpoint-url=http://localhost:4572 s3api put-bucket-acl --bucket demo-bucket --acl public-read
```
* [作成したバケットを確認](http://localhost:8055/)

* local_s3.pyを起動（cat.jpgがアップロード＆ダウンロードされます）
```bash
python local_s3.py
```

## Local DynamoDB

* AWS DynamoDBのローカルテーブルを作成
```
aws dynamodb create-table
    --table-name Music
    --attribute-definitions
        AttributeName=Artist,AttributeType=S
        AttributeName=SongTitle,AttributeType=S
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
    --endpoint-url http://localhost:4569
```
* 作成したDynamoDBを確認
```
aws dynamodb list-tables --endpoint-url http://localhost:4569
```
* local_dynamo.pyを起動
```bash
python local_dynamo.py
```

## Local Lambda

コードは以下で作成可能（レポジトリではすでに作成済み）
```bash
sam init --runtime python3.7
```

* local lambdaを起動
```bash
cd local_lambda\
sam local start-api
```

* [リスポンスを確認](http://127.0.0.1:3000/hello)

* local lambdaに手動でeventをフィードする方法
```bash
sam local invoke "HelloWorldFunction" -e events/event.json
```
* local lambda用のevent jsonの作成方法
```bash
sam local generate-event apigateway aws-proxy --body "" --path "hello" --method GET > api-event.json
```
`↑で作成されるファイルはEncodeがUTF16になるので必ずUTF8にしてから実行すること`