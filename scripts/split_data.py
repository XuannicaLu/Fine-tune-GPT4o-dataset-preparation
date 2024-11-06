import json
import random

def split_dataset(input_file, train_file, val_file, test_file, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    with open(input_file, "r") as f:
        data = [json.loads(line) for line in f]

    # 打乱数据顺序
    random.shuffle(data)

    # 计算每个数据集的大小
    total = len(data)
    train_size = int(total * train_ratio)
    val_size = int(total * val_ratio)

    train_data = data[:train_size]
    val_data = data[train_size:train_size + val_size]
    test_data = data[train_size + val_size:]

    # 保存拆分后的数据
    with open(train_file, "w") as f:
        for entry in train_data:
            json.dump(entry, f)
            f.write("\n")

    with open(val_file, "w") as f:
        for entry in val_data:
            json.dump(entry, f)
            f.write("\n")

    with open(test_file, "w") as f:
        for entry in test_data:
            json.dump(entry, f)
            f.write("\n")

if __name__ == "__main__":
    # 输入输出文件路径
    input_file = "../data/dataset.jsonl"
    train_file = "../data/train.jsonl"
    val_file = "../data/val.jsonl"
    test_file = "../data/test.jsonl"

    split_dataset(input_file, train_file, val_file, test_file)