from contextlib import asynccontextmanager
from aiobotocore.session import get_session 

from typing import Dict, List


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
        key: str
    ):
        async with self.create_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file
            )

    async def get_file(self, key: str) -> Dict:
        async with self.create_client() as client:
            response = await client.get_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return response

    async def delete_file(self, key: str):
        async with self.create_client() as client:
            await client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
