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

    item_id = event["pathParameters"]["id"]

    try:
        scan_response = dynamo_client.scan(
            TableName=table_name,
            FilterExpression="item_id = :item_id",
            ExpressionAttributeValues={
                ":item_id": {"S": item_id}
            }
        )

        items = scan_response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps("Item not found")
            }

        location_id = items[0]["location_id"]["N"]

        dynamo_client.delete_item(
            TableName=table_name,
            Key={
                "item_id": {"S": item_id},
                "location_id": {"N": location_id}
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps(f"Item with ID {item_id} deleted successfully.")
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error deleting item: {str(e)}")
        }