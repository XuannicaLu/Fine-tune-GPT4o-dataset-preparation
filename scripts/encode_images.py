import base64
from PIL import Image
from io import BytesIO
import os
import json

def encode_image(image_path, quality=100):
    with Image.open(image_path) as image:
        image = image.convert("RGB")  # 转换为 RGB 格式
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=quality)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def encode_images_in_directory(directory):
    encoded_images = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(directory, filename)
            encoded_images[filename] = encode_image(image_path)
    return encoded_images

if __name__ == "__main__":
    # 将图片文件夹路径修改为你的实际路径
    image_directory = "../images"
    encoded_images = encode_images_in_directory(image_directory)
    
    # 将编码后的图像数据保存为 JSON 文件，方便后续使用
    with open("../data/encoded_images.json", "w") as f:
        json.dump(encoded_images, f)
