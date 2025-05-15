import requests
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

# Your Hugging Face API token
api_token = "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"
headers = {"Authorization": f"Bearer {api_token}"}
api_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

def generate_image(prompt):
    """Generates an image based on a given prompt using Hugging Face API."""
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        image_data = response.content
        img = Image.open(BytesIO(image_data))
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    raise Exception(f"Failed to generate image. Status Code: {response.status_code}")