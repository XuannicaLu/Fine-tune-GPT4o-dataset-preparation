import os
import glob
import json
import base64
import random
from io import BytesIO
from PIL import Image
from tqdm import tqdm

# Image encoding function
def encode_image(image_path, quality=100):
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=quality)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Example image paths
# Make sure that the images used for the few-shot examples do not appear in the training, validation, or test sets.
example_image_paths = [
    "example_images/cell_metaphase.jpg",
    "example_images/cell_anaphase.jpg",
    "example_images/cell_interphase.jpg",
]

# Few-Shot 
FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "**Example 1:**\n\n**Question:** What is the state of the cell in this image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encode_image(example_image_paths[0], quality=50)}"
                }
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "The cell is in metaphase of mitosis."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "**Example 2:**\n\n**Question:** What phase is the cell currently in?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encode_image(example_image_paths[1], quality=50)}"
                }
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "The cell is in anaphase of mitosis."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "**Example 3:**\n\n**Question:** Can you identify the cell cycle phase shown in the image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encode_image(example_image_paths[2], quality=50)}"
                }
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "The cell is in interphase."
            }
        ]
    },
]


# System prompt
SYSTEM_PROMPT = """
Use the image to answer the question. Analyze the cell's phase based on the visual cues.
"""

# Dataset preparation function, using external annotation file for labels
def prepare_dataset(image_paths, annotations, few_shot_examples, include_assistant=True):
    json_data = []
    for idx, image_path in enumerate(tqdm(image_paths)):
        # Get the image filename
        image_name = os.path.basename(image_path)
        
        # Get the ground truth label for the image
        answer = annotations.get(image_name, "Unknown cell state.")
        
        # Encode the image
        encoded_image = encode_image(image_path, quality=50)
        
        # Question and message structure
        question = "What is the state of the cell in this image?"
        system_message = {"role": "system", "content": [{"type": "text", "text": SYSTEM_PROMPT}]}
        user_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]
        }
        assistant_message = {"role": "assistant", "content": [{"type": "text", "text": answer}]}

        # Combine system message, Few-Shot examples, and user message
        all_messages = [system_message] + few_shot_examples + [user_message]
        
        # Include assistant's answer if required
        if include_assistant:
            all_messages.append(assistant_message)

        json_data.append({"messages": all_messages})
    return json_data

# Function to save JSONL file
def save_jsonl(data, filename):
    with open(filename, "w") as f:
        for entry in data:
            json.dump(entry, f)
            f.write("\n")

# Main function
if __name__ == "__main__":
    # Load annotations from external file
    with open("annotations.json", "r") as f:
        annotations = json.load(f)

    # Specify the path to your image folder
    image_folder = "path/to/your/image/folder"  # Replace with your actual image folder path

    # Get all image paths from the folder
    # This will get all .jpg and .jpeg files; modify the extension if needed
    all_image_paths = glob.glob(os.path.join(image_folder, "*.jpg")) + \
                      glob.glob(os.path.join(image_folder, "*.jpeg"))

    # Shuffle data
    random.shuffle(all_image_paths)

    # Split dataset: 75% training, 15% validation, 15% test
    total_size = len(all_image_paths)
    train_size = int(0.75 * total_size)
    val_size = int(0.15 * total_size)

    # Create split datasets
    train_images = all_image_paths[:train_size]
    val_images = all_image_paths[train_size:train_size + val_size]
    test_images = all_image_paths[train_size + val_size:]

    # Prepare and save training set with assistant responses
    train_data = prepare_dataset(train_images, annotations, FEW_SHOT_EXAMPLES, include_assistant=True)
    save_jsonl(train_data, "train.jsonl")

    # Prepare and save validation set without assistant responses
    val_data = prepare_dataset(val_images, annotations, FEW_SHOT_EXAMPLES, include_assistant=False)
    save_jsonl(val_data, "validation.jsonl")

    # Prepare and save test set without assistant responses
    test_data = prepare_dataset(test_images, annotations, FEW_SHOT_EXAMPLES, include_assistant=False)
    save_jsonl(test_data, "test.jsonl")

    print("Training, validation, and test sets have been successfully generated!")
