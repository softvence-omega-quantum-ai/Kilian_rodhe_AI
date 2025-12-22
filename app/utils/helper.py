import os
from PIL import Image
from io import BytesIO
import mimetypes
import json
# import cloudinary  # COMMENTED OUT - USING S3 NOW
# from cloudinary.uploader import upload  # COMMENTED OUT - USING S3 NOW
import shutil
import requests
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime

# from app.config import CLOUDINARY_API_KEY, CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_SECRET, GENERATED_IMG_PATH  # COMMENTED OUT
from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_S3_BUCKET_NAME, GENERATED_IMG_PATH

# COMMENTED OUT CLOUDINARY CONFIG - USING S3 NOW
# cloudinary.config(
#     cloud_name = CLOUDINARY_CLOUD_NAME,
#     api_key = CLOUDINARY_API_KEY,
#     api_secret = CLOUDINARY_API_SECRET
# )

# S3 Client Configuration
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# COMMENTED OUT CLOUDINARY UPLOAD - USING S3 NOW
# def cloudinary_file_upload(file_path):
#     try:
#         result = upload(
#             file = file_path,
#             resource_type = "auto",
#             folder = "generated_images"
#         )
#         return result['secure_url']
#     except Exception as e:
#         raise ValueError(str(e))

def s3_file_upload(file_path):
    """Upload file to S3 and return public URL"""
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_extension = os.path.splitext(file_path)[1]
        s3_key = f"generated_images/{timestamp}_{unique_id}{file_extension}"
        
        # Upload to S3 without ACL (bucket policy handles public access)
        s3_client.upload_file(
            file_path, 
            AWS_S3_BUCKET_NAME, 
            s3_key,
            ExtraArgs={'ContentType': 'image/png'}
        )
        
        # Return public URL
        s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        return s3_url
        
    except ClientError as e:
        raise ValueError(f"S3 upload failed: {str(e)}")
    except Exception as e:
        raise ValueError(f"Upload error: {str(e)}")


def upload_image(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    return {"mime_type": mime_type, "data": image_data}

def response_data_img(response):
    os.makedirs(GENERATED_IMG_PATH, exist_ok=True)
    temp_file_path = os.path.join(GENERATED_IMG_PATH, "generated_image.png")

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(temp_file_path)
            # image.show()

    return temp_file_path


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