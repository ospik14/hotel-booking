import uuid

async def upload_image_to_cloud(file_bytes: bytes, original_filename: str) -> str:
    ext = original_filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4()}.{ext}'