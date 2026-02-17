# app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv
import cloudinary
from google import genai



# Load env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GENAI_CLIENT = genai.Client(api_key=GEMINI_API_KEY)


# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

# local directory for generated images
BASE_DIR = os.getcwd()

## Constant
LOG_DIR = "logs"
TEMP_FOLDER_NAME = "temp"
MODEL_NAME = "gemini-2.5-flash-image"
TEMPERATURE = 1.0
GENERATED_IMG_PATH = Path("data")

# Product Design Generation Prompt (legacy)
# CLOTHING_DESIGN_PROMPT = """
# You are a premium merchandise designer creating stunning yet realistic designs for apparel and mugs.
#
# RULES:
# - Do NOT add any brand names, logos, or text unless the user explicitly provides them.
# - Keep everything realistic, clean, and print-ready.
# - If an image is uploaded, treat it as the main logo/mark; preserve it without alterations.
#
# IF IMAGE UPLOADED:
# - Center the design around the uploaded logo/mark.
# - Complement (do not alter) the logo with subtle supporting elements based on: {prompt}
# - Ensure great contrast and clarity on both t-shirts and mugs.
#
# IF NO IMAGE:
# - Create a complete design only from the user description: {prompt}
# - Avoid arbitrary text or branding unless provided.
#
# OUTPUT STYLE:
# - High-impact, professional, realistic look.
# - Clean/transparent background, print-ready.
# - Works on both t-shirts (fabric) and mugs (curved surface).
# - Balanced composition; crisp lines; no clutter.
#
# FINAL OUTPUT:
# - A single, print-ready design suitable for both t-shirts and mugs.
# """

# Product Design Generation Prompt (with structured inputs)
CLOTHING_DESIGN_PROMPT = """
You are a premium merchandise designer creating stunning, realistic designs for apparel and mugs.

USER INPUTS:
- Core prompt: {prompt}
- Style: {style}
- Lighting: {lighting}
- Weather/Environment: {weatherenv}
- Camera perspective: {cameraperspective}
- Color scheme: {colorscheme}
- Subject type: {subjecttype}
- Emotion/Expression: {emotionexpression}
- Background type: {backgroundtype}
- Clothing/Fashion: {clothingfashion}
- Composition: {compositiontype}
- Image quality: {imagequality}
- Modification type: {modificationtype}

RULES:
- Do NOT add any brand names, logos, or text unless the user explicitly provides them.
- Keep everything realistic, clean, and print-ready.
- If a logo image is uploaded, preserve it without alterations.
- If a product/reference image is uploaded, use it as visual context.

IF IMAGE(S) UPLOADED:
- If logo image exists, center the design around the uploaded logo/mark.
- If product/reference image exists, align style/composition to that reference where helpful.
- Complement uploaded inputs with subtle supporting elements based on the user inputs.
- Ensure great contrast and clarity on both t-shirts and mugs.

IF NO IMAGE:
- Create a complete design only from the user inputs.
- Avoid arbitrary text or branding unless provided.

OUTPUT STYLE:
- High-impact, professional, realistic look.
- Clean/transparent background, print-ready.
- Works on both t-shirts (fabric) and mugs (curved surface).
- Balanced composition; crisp lines; no clutter.

FINAL OUTPUT:
- A single, print-ready design suitable for both t-shirts and mugs.
"""


