import os
import json

image_directory = 'path/to/your/image_directory'

annotations = {}

for filename in os.listdir(image_directory):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        base_name = os.path.splitext(filename)[0]
        parts = base_name.split('_')

        if 'Interphase' in parts:
            if 'G1' in parts:
                label = "The cell is in G1 phase of interphase."
            elif 'S' in parts:
                label = "The cell is in S phase of interphase."
            elif 'G2' in parts:
                label = "The cell is in G2 phase of interphase."
            else:
                label = "The cell is in interphase."
        elif 'Mitosis' in parts:
            if 'Prophase' in parts:
                label = "The cell is in prophase of mitosis."
            elif 'Metaphase' in parts:
                label = "The cell is in metaphase of mitosis."
            elif 'Anaphase' in parts:
                label = "The cell is in anaphase of mitosis."
            elif 'Telophase' in parts:
                label = "The cell is in telophase of mitosis."
            else:
                label = "The cell is in mitosis."
        else:
            label = "Unknown cell state."

        annotations[filename] = label

with open('annotations.json', 'w') as f:
    json.dump(annotations, f, indent=4)

print("annotations.json has been created successfully.")
