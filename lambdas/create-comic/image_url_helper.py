import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "comicker-comic-panels"


class ImageUrlHelper:
    def __init__(self):
        # using IAM role for session creds
        self.s3_client = boto3.client("s3")

    def create_put_object_presigned_url(self, object_key: str) -> str:
        """Generate a presigned URL to invoke an S3.Client method

        Not all the client methods provided in the AWS Python SDK are supported.

        :param object_key: Name of the object to store in the bucket
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 client method
        response = self.s3_client.generate_presigned_url(ClientMethod="put_object",
                                                    Params={"Bucket": BUCKET_NAME, "Key": object_key},
                                                    ExpiresIn=180)

        # The response contains the presigned URL
        return response


# if __name__ == "__main__":
#     url = ImageUrlHelper().create_put_object_presigned_url("testKey.jpg")
#     print(url)
