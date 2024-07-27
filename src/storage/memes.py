from storage.base import S3Client


ACCESS_KEY_ID = "YCAJEqAEmpo91jCK8FPXemqq7"
SECRET_ACCESS_KEY = "YCPKxm-pAyUBkGu1m7MFlOED1XHl9DcaT7h4haGv"
BUCKET_NAME = "memes1919"
ENDPOINT_URL = "https://storage.yandexcloud.net"

memes_s3 = S3Client(
        access_key_id=ACCESS_KEY_ID,
        secret_access_key=SECRET_ACCESS_KEY,
        bucket_name=BUCKET_NAME,
        endpoint_url=ENDPOINT_URL
    )
