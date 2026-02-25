from fastapi import APIRouter, HTTPException, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional
import os
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ServerError
import asyncio

from app.config import TEMP_FOLDER_NAME
from app.services.t_shirt.shirt import TShirt
from app.utils.helper import (
    response_data_img_async,
    delete_file_async,
    s3_file_upload_async,
    delete_file,
    download_image_from_url_async,
)
# from app.utils.helper import cloudinary_file_upload  # COMMENTED OUT - USING S3 NOW
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

@router.post("/generate_merchandise")
async def generate_merchandise(
    prompt: Optional[str] = Form(None, description="Detailed description of the design and style"),
    style: Optional[str]= Form(None, description= "Comic /Cartoon /Minimalist"),
    lighting: Optional[str]= Form(None, description= "Bright day light / Soft light / Golden hour"),
    weatherenv: Optional[str]= Form(None, description="Sunny / Rain/ Fog"),
    cameraperspective: Optional[str]= Form(None, description= "Close up/ Medium shot / Wide shot"),
    colorscheme: Optional[str]= Form(None, description= "Black White / Monochrome/ Pastel"),
    subjecttype: Optional[str]=Form(None,description= "Person / Animal/ Landscape"), 
    emotionexpression: Optional[str]=Form(None, description= "Happy / Sad / Excited"),
    backgroundtype: Optional[str]= Form(None, description=" Transparent / Solid color / Natural"),
    clothingfashion: Optional[str]= Form(None, description= "Casual / Business / Sports Wear"),
    compositiontype: Optional[str]= Form(None, description= "Centered / Symmetrical / Asymmetrical"),
    imagequality: Optional[str]= Form(None, description="HD / Low Resulation / Sharp"),
    modificationtype: Optional[str]= Form(None, description="Background Removal / Style Transfer/ Face Enhancement"),
    product_image_url: Optional[str] = Form(None, description="Optional product/reference image URL"),
    logo_image_url: Optional[str] = Form(None, description="Optional logo image URL"),
    background_task : BackgroundTasks = None
):

    t_shirt = TShirt(
        prompt=prompt or "",
        style=style,
        lighting=lighting,
        weatherenv=weatherenv,
        cameraperspective=cameraperspective,
        colorscheme=colorscheme,
        subjecttype=subjecttype,
        emotionexpression=emotionexpression,
        backgroundtype=backgroundtype,
        clothingfashion=clothingfashion,
        compositiontype=compositiontype,
        imagequality=imagequality,
        modificationtype=modificationtype,
    )

    product_image_path = None
    logo_image_path = None

    try:
        if product_image_url or logo_image_url:
            os.makedirs(TEMP_FOLDER_NAME, exist_ok = True)

        if product_image_url:
            product_image_path = await download_image_from_url_async(
                product_image_url,
                TEMP_FOLDER_NAME,
                "product",
            )

        if logo_image_url:
            logo_image_path = await download_image_from_url_async(
                logo_image_url,
                TEMP_FOLDER_NAME,
                "logo",
            )

        if product_image_path:
            # Design URL should contain only the design asset:
            # - provided logo if user uploaded one
            # - generated design if no logo uploaded
            if logo_image_path:
                print("Using uploaded logo as design asset......")
                generated_design_url = await s3_file_upload_async(logo_image_path)
                design_asset_path = logo_image_path
            else:
                print("Generating Design Asset......")
                response_design_asset = await asyncio.to_thread(
                    t_shirt.generate_shirt_design,
                    None,
                    None
                )
                design_asset_path = await response_data_img_async(response_design_asset)
                generated_design_url = await s3_file_upload_async(design_asset_path)
                print("Design Asset Generated.")

            # Mockup URL should contain designed product output
            print("Generating Designed Product......")
            response_product = await asyncio.to_thread(
                t_shirt.generate_design_on_product,
                product_image_path,
                design_asset_path
            )
            designed_product_path = await response_data_img_async(response_product)
            generated_mockup_url = await s3_file_upload_async(designed_product_path)
            print("Designed Product Generated.")
        else:
            print("Generating Design......")
            response_d = await asyncio.to_thread(
                t_shirt.generate_shirt_design,
                None,
                logo_image_path
            )
            img_path = await response_data_img_async(response_d)
            generated_design_url = await s3_file_upload_async(img_path)
            print("Design Generated")

            print("Generating Mockup......")
            response_mockup = await asyncio.to_thread(t_shirt.generate_mockup, img_path)
            mockup_path = await response_data_img_async(response_mockup)
            generated_mockup_url = await s3_file_upload_async(mockup_path)
            print("Mockup Generated.")

        if product_image_url or logo_image_url:
            if background_task:
                background_task.add_task(delete_file, TEMP_FOLDER_NAME)
            else:
                await delete_file_async(TEMP_FOLDER_NAME)

        return JSONResponse(
            content={
                "generated_design_url": generated_design_url,
                "mockup_url": generated_mockup_url
            })

    except FileNotFoundError:
        raise HTTPException(status_code=400, detail = "File not found.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



