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

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# local directory for generated images
BASE_DIR = os.getcwd()

## cloudinary api key
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

## Constant
LOG_DIR = "logs"
TEMP_FOLDER_NAME = "temp"
MODEL_NAME = "gemini-2.5-flash-image-preview"
TEMPERATURE = 1.0
GENERATED_IMG_PATH = Path("data")

# Prompt
IMAGE_ANALYSIS_PROMPT = """
    If an image is uploaded:
    - First, analyze the uploaded image and generate a highly detailed, structured, and comprehensive description.
    - The description must be organized into the following categories and optimized for use as a prompt for a high-quality image generator:

    **Overall Composition:** Describe the main subject, its arrangement within the frame, and the general layout. Mention elements like symmetry, asymmetry, depth, and perspective.

    **Dominant Colors:** List the most prominent colors in the image and their general tone (e.g., vibrant, muted, pastel, dark).

    **Shapes:** Identify the primary shapes present in the image, both in the main subject and the background (e.g., geometric, organic, curvilinear, angular).

    **Texture and Material:** Describe any visible textures or implied materials (e.g., smooth, rough, metallic, fabric, wood, glossy).

    **Lighting:** Characterize the lighting conditions (e.g., bright, dim, soft, harsh, natural, artificial, time of day, direction of light, presence of shadows or highlights).

    **Style:** Define the artistic or photographic style of the image (e.g., realistic, abstract, impressionistic, minimalist, retro, futuristic, photorealistic, painterly, cartoon, vector art).

    **Details:** Provide specific observations about intricate elements, patterns, specific objects, or unique features that contribute to the image's character.

    **Mood/Atmosphere:** Describe the overall feeling or emotion evoked by the image (e.g., calm, energetic, mysterious, joyful, somber, professional, whimsical).

    **Keywords:** Generate a list of relevant keywords that succinctly describe the image's content, style, and potential themes, suitable for image search or tagging.

    ---
    After the analysis:
    - Use the uploaded image as the **primary creative reference** for the final design, ensuring its style, subject traits, and inspiration are carried into the generated birthday artwork.

    If NO image is uploaded:
    - Skip the analysis step.
    - Instead, generate the artwork entirely based on the user provided prompt.

    ⚠️ STRICT REQUIREMENTS FOR FINAL OUTPUT:
    - Do NOT generate a t-shirt, mockup, or product photo.
    - The output must be a **standalone design/artwork only**, ready for printing.
    - Artwork must have a **transparent background**.
    - The design should be centered, isolated, and optimized for **fabric printing**.
    - **Never invent random placeholder names (e.g., Nick, John, Mary).**
    
    User Prompt:
    {prompt}

    Birthday-Specific Requirements (if applicable based on prompt):
    - The artwork must clearly feel like it belongs to a **birthday celebration** if mentioned.
    - Include festive elements: confetti, balloons, streamers, cake, or theme-consistent accents.
    - Composition must be colorful, bold, and joyful.
    - Design should be crisp, flat, vector-like, with no background clutter, ensuring it prints cleanly on fabric.
    """


SHIRT_MOCKUP_PROMPT = SHIRT_MOCKUP_PROMPT = """
    Create a realistic, professional product mockup showcasing how the uploaded artwork will appear when printed on the selected apparel.

    Requirements:
    - Use the **uploaded image** as the design to be printed on the apparel (do not recreate, modify, or reposition the artwork).
    - Follow the user's description for the apparel type and style: {prompt}

    Mockup Specifications:
    - The uploaded artwork must appear **naturally printed** on the fabric of the specified apparel type (not floating or pasted).
    - Do **not** include any human models, mannequins, hangers, or background props — show only the apparel item itself.
    - Display the apparel laid flat or presented as a standalone 3D product view.
    - Include realistic fabric texture, folds, lighting, and shadows to emphasize natural print placement.
    - Ensure the design scales properly to the apparel size, gender, and type without distortion.
    - Use a **plain white background** (no gradients or scenery) to keep full focus on the apparel.
    - Present the mockup in a clean, professional, store-ready product photo style.

    ⚠️ Only generate the mockup of the specified apparel with the uploaded image printed on it — do not include duplicate designs, extra variations, or unrelated products.
    """

