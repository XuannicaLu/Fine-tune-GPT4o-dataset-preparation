import json

def prepare_dataset(encoded_images):
    data = []
    for relative_path, encoded_image in encoded_images.items():
        # Determine cell state and phase based on the path
        if "interphase" in relative_path.lower():
            answer = "The cell is in interphase."
        elif "mitosis" in relative_path.lower():
            if "prophase" in relative_path.lower():
                answer = "The cell is in prophase."
            elif "metaphase" in relative_path.lower():
                answer = "The cell is in metaphase."
            elif "anaphase" in relative_path.lower():
                answer = "The cell is in anaphase."
            elif "telophase" in relative_path.lower():
                answer = "The cell is in telophase."
            else:
                answer = "The cell is in mitosis."
        else:
            answer = "Unknown cell state."

        # Define the question and create the message structure
        question = "What is the state of the cell in this image?"
        entry = {
            "messages": [
                {
                    "role": "system",
                    "content": "Use the image to answer the question."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                    ]
                },
                {
                    "role": "assistant",
                    "content": [{"type": "text", "text": answer}]
                }
            ]
        }
        data.append(entry)
    return data

if __name__ == "__main__":
    # Load encoded images from the JSON file created in encode_images.py
    with open("encoded_images.json", "r") as f:
        encoded_images = json.load(f)

    # Generate dataset
    dataset = prepare_dataset(encoded_images)
    
    # Save as a JSONL file
    with open("dataset.jsonl", "w") as f:
        for entry in dataset:
            json.dump(entry, f)
            f.write("\n")
