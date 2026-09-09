import json
import boto3
import os

sqs = boto3.client("sqs")

QUEUE_URL = os.environ["QUEUE_URL"]


def lambda_handler(event, context):

    try:
        # API Gateway se aane wala body
        body = json.loads(event.get("body", "{}"))

        name = body.get("name")
        email = body.get("email")
        message = body.get("message")

        # SQS mein message send
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({
                "name": name,
                "email": email,
                "message": message
            })
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "success": True,
                "message": "Data sent to SQS successfully",
                "messageId": response["MessageId"]
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }
