import os
from pathlib import Path
from google import genai
from google.genai import types

class ImageGenerator:
    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise RuntimeError("GOOGLE_API_KEY not found.")
        self.client = genai.Client(api_key=self.api_key)

    def generate_bytes(self, prompt: str) -> bytes:
        resp = self.client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold="BLOCK_ONLY_HIGH",
                    )
                ],
            ),
        )
        
        # Robust response handling
        parts = getattr(resp, "parts", None)
        if not parts and getattr(resp, "candidates", None):
            try:
                parts = resp.candidates[0].content.parts
            except Exception:
                parts = None
        
        if not parts:
            raise RuntimeError("No image returned from Gemini.")

        for part in parts:
            inline = getattr(part, "inline_data", None)
            if inline and getattr(inline, "data", None):
                return inline.data
        
        raise RuntimeError("No valid image data found.")

    def save_image(self, prompt: str, path: Path):
        data = self.generate_bytes(prompt)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
