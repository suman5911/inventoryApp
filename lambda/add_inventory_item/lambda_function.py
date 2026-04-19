import boto3
import json
import os
import uuid
from decimal import Decimal


def lambda_handler(event, context):
    table_name = os.environ["table_name"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    try:
        body = json.loads(event["body"])
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps("Bad request. Please provide valid JSON data.")
        }

    try:
        item_id = str(uuid.uuid4())

        item = {
            "item_id": item_id,
            "location_id": int(body["location_id"]),
            "item_name": body["item_name"],
            "item_description": body["item_description"],
            "item_qty_on_hand": int(body["item_qty_on_hand"]),
            "item_price": Decimal(str(body["item_price"]))
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Item added successfully.",
                "item_id": item_id
            })
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error adding item: {str(e)}")
        }