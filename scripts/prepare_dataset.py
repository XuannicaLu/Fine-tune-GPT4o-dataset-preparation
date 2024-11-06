import json
import pandas as pd

# 示例问题和答案
questions = [
    "What is the state of the cell in this image?",
    "Is this cell in the mitosis phase?",
]
answers = ["Interphase", "Yes"]

def prepare_dataset(encoded_images, questions, answers):
    data = []
    for image_name, encoded_image in encoded_images.items():
        for question, answer in zip(questions, answers):
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
    # 从 Step 1 生成的 JSON 文件读取编码图像数据
    with open("../data/encoded_images.json", "r") as f:
        encoded_images = json.load(f)

    # 生成数据集
    dataset = prepare_dataset(encoded_images, questions, answers)
    
    # 保存为 JSONL 文件
    with open("../data/dataset.jsonl", "w") as f:
        for entry in dataset:
            json.dump(entry, f)
            f.write("\n")
