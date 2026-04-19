import boto3
import json
import os


def lambda_handler(event, context):
    dynamo_client = boto3.client("dynamodb")
    table_name = os.environ["table_name"]

    try:
        response = dynamo_client.scan(TableName=table_name)
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps(items, default=str)
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }