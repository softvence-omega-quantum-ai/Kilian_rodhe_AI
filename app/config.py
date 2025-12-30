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
MODEL_NAME = "gemini-2.5-flash-image-preview"
TEMPERATURE = 1.0
GENERATED_IMG_PATH = Path("data")

# Clothing Design Generation Prompt
CLOTHING_DESIGN_PROMPT = """
You are an expert clothing designer and digital artist. Create a high-quality, professional clothing design based on the user's requirements.

**If an image is uploaded:**
1. **Analyze the uploaded image thoroughly:**
   - Extract key design elements: colors, patterns, shapes, textures, style
   - Identify artistic style: minimalist, vintage, modern, abstract, realistic, cartoon, etc.
   - Note composition elements: layout, balance, focal points
   - Understand mood and aesthetic: playful, elegant, bold, subtle, etc.

2. **Use analysis as creative foundation:**
   - Incorporate the visual style and aesthetic from the uploaded image
   - Adapt colors, patterns, and design elements to work on clothing
   - Maintain the essence and mood of the original image

**If NO image is uploaded:**
- Create design entirely based on user's text description
- Focus on interpreting their vision into a clothing-appropriate design

**DESIGN REQUIREMENTS:**
✅ **Output Format:**
- Generate a standalone clothing design/artwork ONLY
- NO t-shirt mockups, product photos, or clothing items
- Design should be ready for printing on any garment
- Transparent or clean background (no clutter)

✅ **Design Specifications:**
- Optimized for fabric printing (vector-style preferred)
- Centered and well-balanced composition
- Scalable design that works on different garment sizes
- High contrast and clear details for print quality

✅ **Style Considerations:**
- Match the requested style: {prompt}
- Consider target audience (age, gender, preferences)
- Ensure design works on specified clothing type and color
- Balance creativity with wearability

✅ **Technical Requirements:**
- Clean, crisp lines and shapes
- Appropriate color palette for clothing
- Design elements should not be too complex for printing
- Consider how design will look when worn

**User Requirements:** {prompt}

**Final Output:** A professional, print-ready clothing design that perfectly captures the user's vision and works beautifully on apparel.
"""


