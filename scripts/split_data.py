import json
import random

def split_dataset(input_file, train_file, val_file, max_samples=30000, train_ratio=0.8, val_ratio=0.2):
    with open(input_file, "r") as f:
        data = [json.loads(line) for line in f]

    # Shuffle and limit data to max_samples
    random.shuffle(data)
    data = data[:max_samples]

    total = len(data)
    train_size = int(total * train_ratio)

    train_data = data[:train_size]
    val_data = data[train_size:]

    with open(train_file, "w") as f:
        for entry in train_data:
            json.dump(entry, f)
            f.write("\n")

    with open(val_file, "w") as f:
        for entry in val_data:
            json.dump(entry, f)
            f.write("\n")

if __name__ == "__main__":
    input_file = "data/dataset.jsonl"
    train_file = "data/train.jsonl"
    val_file = "data/val.jsonl"

    split_dataset(input_file, train_file, val_file)
