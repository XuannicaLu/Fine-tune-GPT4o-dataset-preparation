import base64
from PIL import Image
from io import BytesIO
import os
import json

def encode_image(image_path, quality=100):
    with Image.open(image_path) as image:
        image = image.convert("RGB")  
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=quality)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def encode_images_in_directory(directory):
    encoded_images = {}
    for root, _, files in os.walk(directory):  
        for filename in files:
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, filename)
                print(f"Encoding image: {image_path}")  
                relative_path = os.path.relpath(image_path, directory)
                encoded_images[relative_path] = encode_image(image_path)
    return encoded_images

if __name__ == "__main__":

    image_directory = "images"
    encoded_images = encode_images_in_directory(image_directory)
    
    with open("encoded_images.json", "w") as f:
        json.dump(encoded_images, f)
