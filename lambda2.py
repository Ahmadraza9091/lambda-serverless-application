import json
import boto3
import os
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    for record in event["Records"]:

        try:
            # SQS message body
            data = json.loads(record["body"])

            # DynamoDB item
            item = {
                "id": str(uuid.uuid4()),
                "name": data.get("name"),
                "email": data.get("email"),
                "message": data.get("message"),
                "createdAt": datetime.now(timezone.utc).isoformat()
            }

            # DynamoDB mein save
            table.put_item(Item=item)

            print("Data saved successfully:", item)

        except Exception as e:
            print("Error processing message:", str(e))
            raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Messages processed successfully"
        })
    }
