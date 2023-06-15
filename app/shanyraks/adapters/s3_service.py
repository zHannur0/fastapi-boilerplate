from typing import BinaryIO

import boto3


class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def upload_file(self, file: BinaryIO, shanyrak_id: str, filename: str):
        bucket = "zhannurkhan04-bucket"
        filekey = f"shanyraks/{shanyrak_id}/{filename}"

        self.s3.upload_fileobj(file, bucket, filekey)

        bucket_location = boto3.client("s3").get_bucket_location(
            Bucket=bucket
        )
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location["LocationConstraint"], bucket, filekey
        )

        return object_url

    def delete_file(self, shanyrak_id: str, filename: str):
        bucket = "zhannurkhan04-bucket"
        print(filename.split('/')[-1])
        filekey = f"shanyraks/{shanyrak_id}/{filename.split('/')[-1]}"

        self.s3.delete_object(Bucket=bucket, Key=filekey)