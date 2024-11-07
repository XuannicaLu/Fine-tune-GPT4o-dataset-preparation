import json

def prepare_dataset(encoded_images):
    data = []
    for relative_path, encoded_image in encoded_images.items():
        # Determine cell state and phase based on the path
        if "Interphase" in relative_path.lower():
            if "G1" in relative_path.lower():
                answer = "The cell is in G1 phase of interphase."
            elif "S" in relative_path.lower():
                answer = "The cell is in S phase of interphase."
            elif "G2" in relative_path.lower():
                answer = "The cell is in G2 phase of interphase."
            else:
                answer = "The cell is in interphase."
        elif "Mitosis" in relative_path.lower():
            if "Prophase" in relative_path.lower():
                answer = "The cell is in prophase of mitosis."
            elif "Metaphase" in relative_path.lower():
                answer = "The cell is in metaphase of mitosis."
            elif "Anaphase" in relative_path.lower():
                answer = "The cell is in anaphase of mitosis."
            elif "Telophase" in relative_path.lower():
                answer = "The cell is in telophase of mitosis."
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
    with open("data/dataset.jsonl", "w") as f:
        for entry in dataset:
            json.dump(entry, f)
            f.write("\n")