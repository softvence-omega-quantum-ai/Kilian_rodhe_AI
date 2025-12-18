from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, Union
import shutil
import os
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ServerError
import asyncio

from app.config import TEMP_FOLDER_NAME
from app.services.t_shirt.shirt import TShirt
from app.utils.helper import response_data_img, delete_file
from app.utils.helper import cloudinary_file_upload
from app.utils.logger import get_logger


logger = get_logger(__name__)


router = APIRouter()

@retry(
    wait = wait_exponential(multiplier=1, min=4, max=10),
    stop = stop_after_attempt(3),
    retry = retry_if_exception_type(ServerError),
    before_sleep=lambda retry_state: logger.info(
        f"Retrying due to 500 error, attempt {retry_state.attempt_number}"
    )
)

@router.post("/t_shirt_generate")
async def t_shirt_generate(
    prompt: str = Form(..., description="Detailed description of the t-shirt design and style"),
    img_file: Optional[Union[UploadFile,str]] = File(None, description="Optional image file to include in the t-shirt design"),
    background_task : BackgroundTasks = None
):

    t_shirt = TShirt(
        prompt=prompt
    )

    allowed_file_types = ["image/jpeg", "image/png", "image/bmp"]

    ## With image
    if img_file:
        if img_file.content_type not in allowed_file_types:
            raise HTTPException(status_code=404, detail = "Only Image file are acceptable.")

        os.makedirs(TEMP_FOLDER_NAME, exist_ok = True)
        temp_file_path = os.path.join(TEMP_FOLDER_NAME, img_file.filename)

        try:
            with open(temp_file_path, 'wb') as temp_file:
                shutil.copyfileobj(img_file.file, temp_file)

            print("Generating Image......")
            response_d = t_shirt.generate_shirt_design(temp_file_path)
            img_path = response_data_img(response_d)
            generated_design_url = cloudinary_file_upload(img_path)
            print("Image Generated")



            print("Generating Mockup......")
            response_m = t_shirt.generate_shirt_mockup(img_path)
            generated_mockup_url = cloudinary_file_upload(response_data_img(response_m))
            print("Mockup Generated.")



            background_task.add_task(delete_file, TEMP_FOLDER_NAME)

            return JSONResponse(
                content={"generated_design_url": generated_design_url, "generated_mockup_url" : generated_mockup_url})

        except FileNotFoundError:
            raise HTTPException(status_code=400, detail = "File not found.")
    else:
        try:

            print("Generating Image......")
            response_d = t_shirt.generate_shirt_design(None)
            img_path = response_data_img(response_d)
            generated_design_url = cloudinary_file_upload(img_path)
            print("Image Generated")



            print("Generating Mockup......")
            response_m = t_shirt.generate_shirt_mockup(img_path)
            generated_mockup_url = cloudinary_file_upload(response_data_img(response_m))
            print("Mockup Generated.")

            return JSONResponse(
                content={"generated_design_url": generated_design_url, "generated_mockup_url" : generated_mockup_url})

        except FileNotFoundError:
            raise HTTPException(status_code=400, detail = "File not found.")



