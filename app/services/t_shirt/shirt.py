from google import genai
from google.genai.types import GenerateContentConfig, Modality
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.api_core.exceptions import ServiceUnavailable

from app.utils.logger import get_logger
from app.utils.helper import upload_image
from app.config import CLOTHING_DESIGN_PROMPT, GEMINI_API_KEY, MODEL_NAME, TEMPERATURE

logger = get_logger(__name__)



class TShirt:

    def __init__(
        self,
        prompt: str,
        style: Optional[str] = None,
        lighting: Optional[str] = None,
        weatherenv: Optional[str] = None,
        cameraperspective: Optional[str] = None,
        colorscheme: Optional[str] = None,
        subjecttype: Optional[str] = None,
        emotionexpression: Optional[str] = None,
        backgroundtype: Optional[str] = None,
        clothingfashion: Optional[str] = None,
        compositiontype: Optional[str] = None,
        imagequality: Optional[str] = None,
        modificationtype: Optional[str] = None,
    ):
        self.prompt = prompt
        self.style = style
        self.lighting = lighting
        self.weatherenv = weatherenv
        self.cameraperspective = cameraperspective
        self.colorscheme = colorscheme
        self.subjecttype = subjecttype
        self.emotionexpression = emotionexpression
        self.backgroundtype = backgroundtype
        self.clothingfashion = clothingfashion
        self.compositiontype = compositiontype
        self.imagequality = imagequality
        self.modificationtype = modificationtype

    def _mockup_target(self) -> str:
        """Choose mockup target based on prompt hints."""
        text = (self.prompt or "").lower()
        mug_keywords = ["mug", "cup", "ceramic"]
        for kw in mug_keywords:
            if kw in text:
                return "mug"
        return "tshirt"


    ## model
    @staticmethod
    def model_client():
        try:
            logger.info("Initializing model client...")

            client = genai.Client(api_key=GEMINI_API_KEY)

            config = GenerateContentConfig(
                response_modalities=[Modality.TEXT, Modality.IMAGE],
                temperature=TEMPERATURE
            )

            return client, config
        except Exception as e:
            logger.error(f"Error in model client: {e}")
            raise e

    @retry(
        stop = stop_after_attempt(3),
        wait = wait_exponential(multiplier = 1, min = 4, max = 10),
        retry = retry_if_exception_type(ServiceUnavailable)
    )
    def _make_api_call(self, client, model, contents, config):
        return client.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )

    ## T-Shirt Design
    def generate_shirt_design(
        self,
        product_img_path: Optional[str] = None,
        logo_img_path: Optional[str] = None
    ):
        try:
            prompt_vars = {
                "prompt": self.prompt,
                "style": self.style or "Unspecified",
                "lighting": self.lighting or "Unspecified",
                "weatherenv": self.weatherenv or "Unspecified",
                "cameraperspective": self.cameraperspective or "Unspecified",
                "colorscheme": self.colorscheme or "Unspecified",
                "subjecttype": self.subjecttype or "Unspecified",
                "emotionexpression": self.emotionexpression or "Unspecified",
                "backgroundtype": self.backgroundtype or "Unspecified",
                "clothingfashion": self.clothingfashion or "Unspecified",
                "compositiontype": self.compositiontype or "Unspecified",
                "imagequality": self.imagequality or "Unspecified",
                "modificationtype": self.modificationtype or "Unspecified",
            }

            parts = []
            role_hints = []

            if product_img_path:
                logger.info("Uploading product/reference image...")
                parts.append({"inline_data": upload_image(product_img_path)})
                role_hints.append("- Use the first uploaded image as a product/reference image.")

            if logo_img_path:
                logger.info("Uploading logo image...")
                parts.append({"inline_data": upload_image(logo_img_path)})
                role_hints.append("- Use the second uploaded image as the logo and preserve it accurately.")

            if not parts:
                logger.info("No reference images provided.")

            role_hint_text = ""
            if role_hints:
                role_hint_text = "\n\nIMAGE ROLE GUIDANCE:\n" + "\n".join(role_hints)

            parts.append({"text": CLOTHING_DESIGN_PROMPT.format(**prompt_vars) + role_hint_text})
            t_shirt_content = [{"parts": parts}]

            ## Model
            logger.info("Generating t-shirt design...")
            client, config = self.model_client()

            response = self._make_api_call(client, MODEL_NAME, t_shirt_content, config)
            logger.info("T-shirt design generated successfully.")
            return response
        except Exception as e:
            logger.error(f"Error in shirt design: {e}")
            raise e

    # Generate T-Shirt Mockup
    def generate_shirt_mockup(self, generated_design):
        try:
            # T-shirt mockup prompt
            mockup_prompt = f"""
            Create a STUNNING, professional t-shirt mockup showcasing the uploaded design.
            
            Requirements:
            - Show the design beautifully printed on a premium quality t-shirt
            - T-shirt should be laid flat or 3D product view (choose most flattering angle)
            - Clean white or subtle gradient background
            - Professional product photography style with soft shadows
            - Premium lighting that highlights the design
            - No models, mannequins, or extra props
            - Make it look like a high-end retail product photo
            - Based on user requirements: {self.prompt}
            """
            
            t_shirt_mockup_content = [
                {
                    "parts": [
                        {"inline_data": upload_image(generated_design)},
                        {"text": mockup_prompt}
                    ]
                }
            ]

            ## Model
            logger.info("Generating t-shirt mockup...")
            client, config = self.model_client()

            response = self._make_api_call(
                client, MODEL_NAME, t_shirt_mockup_content, config)
            logger.info("T-shirt mockup generated successfully.")
            return response
        except Exception as e:
            logger.error(f"Error in shirt mockup: {e}")
            raise e

    # Generate Mug Mockup
    def generate_mug_mockup(self, generated_design):
        try:
            # Mug mockup prompt
            mockup_prompt = f"""
            Create a STUNNING, professional mug mockup showcasing the uploaded design.
            
            Requirements:
            - Show the design beautifully printed on a premium ceramic mug
            - Mug should be positioned at a flattering 3/4 angle showing the design clearly
            - Clean white or subtle gradient background
            - Professional product photography style with soft shadows and reflections
            - Premium lighting that makes the mug look expensive and desirable
            - Design should wrap naturally around the curved mug surface
            - Show the mug handle positioned attractively
            - Make it look like a high-end retail product photo
            - The mug should be a classic white ceramic mug
            - Based on user requirements: {self.prompt}
            """
            
            mug_mockup_content = [
                {
                    "parts": [
                        {"inline_data": upload_image(generated_design)},
                        {"text": mockup_prompt}
                    ]
                }
            ]

            ## Model
            logger.info("Generating mug mockup...")
            client, config = self.model_client()

            response = self._make_api_call(
                client, MODEL_NAME, mug_mockup_content, config)
            logger.info("Mug mockup generated successfully.")
            return response
        except Exception as e:
            logger.error(f"Error in mug mockup: {e}")
            raise e

    def generate_mockup(self, generated_design):
        """Generate the appropriate mockup (t-shirt or mug) based on prompt."""
        target = self._mockup_target()
        if target == "mug":
            return self.generate_mug_mockup(generated_design)
        return self.generate_shirt_mockup(generated_design)

