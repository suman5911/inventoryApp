import boto3
import json
import os


def lambda_handler(event, context):
    dynamo_client = boto3.client("dynamodb")
    table_name = os.environ["table_name"]

    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter")
        }

    location_id = event["pathParameters"]["id"]

    try:
        response = dynamo_client.query(
            TableName=table_name,
            IndexName="GSI_location_id-item_id",
            KeyConditionExpression="location_id = :location_id",
            ExpressionAttributeValues={
                ":location_id": {"N": location_id}
            }
        )

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