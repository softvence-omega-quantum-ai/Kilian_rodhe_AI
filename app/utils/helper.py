# import os
# import asyncio
# from PIL import Image
# from io import BytesIO
# import mimetypes
# import json
# # import cloudinary  # COMMENTED OUT - USING S3 NOW
# # from cloudinary.uploader import upload  # COMMENTED OUT - USING S3 NOW
# import shutil
# import requests
# import boto3
# from botocore.exceptions import ClientError
# import uuid
# from datetime import datetime
# from urllib.parse import urlparse

# # from app.config import CLOUDINARY_API_KEY, CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_SECRET, GENERATED_IMG_PATH  # COMMENTED OUT
# from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_S3_BUCKET_NAME, GENERATED_IMG_PATH

# # COMMENTED OUT CLOUDINARY CONFIG - USING S3 NOW
# # cloudinary.config(
# #     cloud_name = CLOUDINARY_CLOUD_NAME,
# #     api_key = CLOUDINARY_API_KEY,
# #     api_secret = CLOUDINARY_API_SECRET
# # )

# # S3 Client Configuration
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#     region_name=AWS_REGION
# )

# ALLOWED_IMAGE_MIME_TYPES = {
#     "image/jpeg",
#     "image/jpg",
#     "image/png",
#     "image/bmp",
#     "image/webp",
#     "image/gif",
#     "image/tiff",
#     "image/heic",
#     "image/heif",
# }

# # COMMENTED OUT CLOUDINARY UPLOAD - USING S3 NOW
# # def cloudinary_file_upload(file_path):
# #     try:
# #         result = upload(
# #             file = file_path,
# #             resource_type = "auto",
# #             folder = "generated_images"
# #         )
# #         return result['secure_url']
# #     except Exception as e:
# #         raise ValueError(str(e))

# def s3_file_upload(file_path):
#     """Upload file to S3 and return public URL"""
#     try:
#         # Generate unique filename
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         unique_id = str(uuid.uuid4())[:8]
#         file_extension = os.path.splitext(file_path)[1]
#         s3_key = f"generated_images/{timestamp}_{unique_id}{file_extension}"
        
#         # Upload to S3 without ACL (bucket policy handles public access)
#         s3_client.upload_file(
#             file_path, 
#             AWS_S3_BUCKET_NAME, 
#             s3_key,
#             ExtraArgs={'ContentType': 'image/png'}
#         )
        
#         # Return public URL
#         s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
#         return s3_url
        
#     except ClientError as e:
#         raise ValueError(f"S3 upload failed: {str(e)}")
#     except Exception as e:
#         raise ValueError(f"Upload error: {str(e)}")


# async def s3_file_upload_async(file_path):
#     return await asyncio.to_thread(s3_file_upload, file_path)


# def upload_image(image_path):
#     mime_type, _ = mimetypes.guess_type(image_path)
#     if mime_type is None:
#         mime_type = "application/octet-stream"

#     with open(image_path, "rb") as image_file:
#         image_data = image_file.read()

#     return {"mime_type": mime_type, "data": image_data}


# def download_image_from_url(image_url, destination_dir, prefix):
#     parsed_url = urlparse(image_url)
#     if parsed_url.scheme not in {"http", "https"}:
#         raise ValueError("Invalid image URL. Only http/https URLs are supported.")

#     with requests.get(image_url, stream=True, timeout=20) as response:
#         response.raise_for_status()
#         content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
#         if content_type not in ALLOWED_IMAGE_MIME_TYPES:
#             raise ValueError(
#                 "Only JPEG, PNG, BMP, WEBP, GIF, TIFF, and HEIC image URLs are acceptable."
#             )

#         extension_map = {
#             "image/jpeg": ".jpg",
#             "image/jpg": ".jpg",
#             "image/png": ".png",
#             "image/bmp": ".bmp",
#             "image/webp": ".webp",
#             "image/gif": ".gif",
#             "image/tiff": ".tiff",
#             "image/heic": ".heic",
#             "image/heif": ".heif",
#         }
#         extension = extension_map.get(content_type, ".img")
#         file_name = f"{prefix}_{uuid.uuid4().hex[:8]}{extension}"
#         file_path = os.path.join(destination_dir, file_name)

#         response.raw.decode_content = True
#         with open(file_path, "wb") as temp_file:
#             shutil.copyfileobj(response.raw, temp_file)

#     return file_path


# async def download_image_from_url_async(image_url, destination_dir, prefix):
#     return await asyncio.to_thread(download_image_from_url, image_url, destination_dir, prefix)

# def response_data_img(response):
#     os.makedirs(GENERATED_IMG_PATH, exist_ok=True)
#     temp_file_path = os.path.join(GENERATED_IMG_PATH, "generated_image.png")

#     for part in response.candidates[0].content.parts:
#         if part.inline_data is not None:
#             image = Image.open(BytesIO(part.inline_data.data))
#             image.save(temp_file_path)
#             # image.show()

#     return temp_file_path


# async def response_data_img_async(response):
#     return await asyncio.to_thread(response_data_img, response)


# def load_json(json_data, JsonOpject):
#     try:
#         data_dict = json.loads(json_data)
#         obj = JsonOpject(**data_dict)

#         return obj
#     except Exception as e:
#         raise ValueError(str(e))

# def delete_file(file_path):
#     if os.path.exists(file_path):
#         shutil.rmtree(file_path)


# async def delete_file_async(file_path):
#     return await asyncio.to_thread(delete_file, file_path)



# def request_product(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         product = response.json()
#         return product
#     else:
#         raise ValueError(f"Failed to fetch product. Status code: {response.status_code}")


# def filter_data(data, price):
#     filtered_items = [
#         {
#             "id": item["id"],
#             "title": item["title"],
#             "price": item["price"],
#             "avg_rating": item["avg_rating"],
#             "link": item["link"],
#             "image_url": item["image_url"],
#             "affiliated_company": item["affiliated_company"]
#         }
#         for item in data["data"]["items"]
#         if item["price"] <= price
#     ]
#     return filtered_items


import os
import asyncio
from PIL import Image
from io import BytesIO
import mimetypes
import json
import shutil
import requests
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime
from urllib.parse import urlparse

from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_S3_BUCKET_NAME, GENERATED_IMG_PATH

# S3 Client Configuration
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

ALLOWED_IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/bmp",
    "image/webp",
    "image/gif",
    "image/tiff",
    "image/heic",
    "image/heif",
}

EXTENSION_MIME_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".bmp": "image/bmp",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".tiff": "image/tiff",
    ".heic": "image/heic",
    ".heif": "image/heif",
}


def s3_file_upload(file_path):
    """Upload file to S3 and return public URL"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_extension = os.path.splitext(file_path)[1]
        s3_key = f"generated_images/{timestamp}_{unique_id}{file_extension}"

        s3_client.upload_file(
            file_path,
            AWS_S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={'ContentType': 'image/png'}
        )

        s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        return s3_url

    except ClientError as e:
        raise ValueError(f"S3 upload failed: {str(e)}")
    except Exception as e:
        raise ValueError(f"Upload error: {str(e)}")


async def s3_file_upload_async(file_path):
    return await asyncio.to_thread(s3_file_upload, file_path)


def detect_mime_type(image_path: str) -> str:
    """
    Detect MIME type using multiple fallback strategies:
    1. mimetypes.guess_type (may fail on VPS due to incomplete MIME DB)
    2. File extension manual lookup
    3. Magic bytes from file header
    """
    # Strategy 1: mimetypes standard library
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type and mime_type in ALLOWED_IMAGE_MIME_TYPES:
        return mime_type

    # Strategy 2: Manual extension lookup (reliable since download_image_from_url sets correct extension)
    ext = os.path.splitext(image_path)[1].lower()
    if ext in EXTENSION_MIME_MAP:
        return EXTENSION_MIME_MAP[ext]

    # Strategy 3: Magic bytes from file header
    try:
        with open(image_path, "rb") as f:
            header = f.read(12)
        if header[:8] == b'\x89PNG\r\n\x1a\n':
            return "image/png"
        elif header[:3] == b'\xff\xd8\xff':
            return "image/jpeg"
        elif header[:4] == b'RIFF' and header[8:12] == b'WEBP':
            return "image/webp"
        elif header[:6] in (b'GIF87a', b'GIF89a'):
            return "image/gif"
        elif header[:2] in (b'II', b'MM'):
            return "image/tiff"
    except Exception:
        pass

    # Final fallback: generated images are always PNG
    return "image/png"


def upload_image(image_path: str) -> dict:
    mime_type = detect_mime_type(image_path)

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    return {"mime_type": mime_type, "data": image_data}


def download_image_from_url(image_url, destination_dir, prefix):
    parsed_url = urlparse(image_url)
    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("Invalid image URL. Only http/https URLs are supported.")

    with requests.get(image_url, stream=True, timeout=20) as response:
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
        if content_type not in ALLOWED_IMAGE_MIME_TYPES:
            raise ValueError(
                "Only JPEG, PNG, BMP, WEBP, GIF, TIFF, and HEIC image URLs are acceptable."
            )

        extension_map = {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
            "image/bmp": ".bmp",
            "image/webp": ".webp",
            "image/gif": ".gif",
            "image/tiff": ".tiff",
            "image/heic": ".heic",
            "image/heif": ".heif",
        }
        extension = extension_map.get(content_type, ".img")
        file_name = f"{prefix}_{uuid.uuid4().hex[:8]}{extension}"
        file_path = os.path.join(destination_dir, file_name)

        response.raw.decode_content = True
        with open(file_path, "wb") as temp_file:
            shutil.copyfileobj(response.raw, temp_file)

    return file_path


async def download_image_from_url_async(image_url, destination_dir, prefix):
    return await asyncio.to_thread(download_image_from_url, image_url, destination_dir, prefix)


def response_data_img(response):
    os.makedirs(GENERATED_IMG_PATH, exist_ok=True)
    temp_file_path = os.path.join(GENERATED_IMG_PATH, "generated_image.png")

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(temp_file_path)

    return temp_file_path


async def response_data_img_async(response):
    return await asyncio.to_thread(response_data_img, response)


def load_json(json_data, JsonOpject):
    try:
        data_dict = json.loads(json_data)
        obj = JsonOpject(**data_dict)
        return obj
    except Exception as e:
        raise ValueError(str(e))


def delete_file(file_path):
    if os.path.exists(file_path):
        shutil.rmtree(file_path)


async def delete_file_async(file_path):
    return await asyncio.to_thread(delete_file, file_path)


def request_product(url):
    response = requests.get(url)
    if response.status_code == 200:
        product = response.json()
        return product
    else:
        raise ValueError(f"Failed to fetch product. Status code: {response.status_code}")


def filter_data(data, price):
    filtered_items = [
        {
            "id": item["id"],
            "title": item["title"],
            "price": item["price"],
            "avg_rating": item["avg_rating"],
            "link": item["link"],
            "image_url": item["image_url"],
            "affiliated_company": item["affiliated_company"]
        }
        for item in data["data"]["items"]
        if item["price"] <= price
    ]
    return filtered_items