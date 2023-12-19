import boto3
import io
import json


def get_json_object(bucket, key):
    s3 = boto3.resource("s3")
    s3_obj = s3.Object(bucket, key)
    data = io.BytesIO()
    s3_obj.download_fileobj(data)

    return json.loads(data.getvalue().decode('utf-8'))


def put_json_object(obj, bucket, key):
    s3 = boto3.resource("s3")
    s3_obj = s3.Object(bucket, key)

    s3_obj.put(
        Body=(bytes(json.dumps(obj).encode('utf-8')))
    )

