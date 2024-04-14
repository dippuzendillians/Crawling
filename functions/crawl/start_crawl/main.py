import json
import os

import boto3


def lambda_handler(event, context):

    body = json.loads(event["body"])

    FIVE_MINUTES = 300
    timeout = body.get("timeout", FIVE_MINUTES)
    timeout = min(int(timeout), FIVE_MINUTES)

    url = body.get("url")
    job_id = body.get("job_id")

    payload = {"url": url, "timeout": int(timeout), "job_id": job_id}

    lambda_client = boto3.client("lambda")

    TARGET_FUNCTION_ARN = os.environ.get("TARGET_FUNCTION_ARN")

    lambda_client.invoke(
        FunctionName=TARGET_FUNCTION_ARN,
        InvocationType="Event",
        Payload=json.dumps(payload),
    )

    return {"statusCode": 200, "body": json.dumps({"message": "Crawl started!"})}
