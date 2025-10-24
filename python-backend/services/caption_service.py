from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests
from io import BytesIO
from typing import List, Dict

processor = None
model = None

def load_blip_model():
    global processor, model
    if processor is None or model is None:
        print("Loading BLIP model...")
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        print("BLIP model loaded successfully!")

def caption_single_image(image_url: str) -> str:
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert('RGB')

        inputs = processor(image, return_tensors="pt")

        outputs = model.generate(**inputs, max_length=50, num_beams=5)

        caption = processor.decode(outputs[0], skip_special_tokens=True)

        return caption

    except Exception as e:
        print(f"Error captioning image {image_url}: {str(e)}")
        return "Unable to generate caption"

def generate_captions(images: List[Dict[str, str]]) -> List[Dict[str, str]]:
    load_blip_model()

    results = []

    for idx, image in enumerate(images):
        print(f"Processing image {idx + 1}/{len(images)}: {image['fileName']}")

        caption = caption_single_image(image['directLink'])

        results.append({
            'fileName': image['fileName'],
            'driveLink': image['driveLink'],
            'caption': caption
        })

    return results
