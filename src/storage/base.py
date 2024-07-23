from contextlib import asynccontextmanager
from aiobotocore.session import get_session 


class S3Client:
    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        bucket_name: str,
        endpoint_url: str
    ):
        self.config = {
            "aws_access_key_id": access_key_id,
            "aws_secret_access_key": secret_access_key,
            "endpoint_url": endpoint_url
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def create_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
        self,
        file,
        object_name: str
    ):
        async with self.create_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file
            )
