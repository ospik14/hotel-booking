import uuid
import aioboto3
from .config import (
    S3_ENDPOINT_URL, 
    S3_ACCESS_KEY, 
    S3_SECRET_KEY, 
    S3_REGION, 
    S3_BUCKET_NAME,
    S3_PUBLIC_URL
)

session = aioboto3.Session()

async def upload_image_to_cloud(file_bytes: bytes, original_filename: str) -> str:
    ext = original_filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4()}.{ext}'

    async with session.client(
        service_name="s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION
    ) as s3_client:
        await s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=unique_filename,
            Body=file_bytes,
            ContentType=f"image/{ext}",
        )

    return f"{S3_PUBLIC_URL}/{unique_filename}"