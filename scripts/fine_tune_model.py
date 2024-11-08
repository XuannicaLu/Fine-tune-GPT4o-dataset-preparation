from openai import OpenAI
import json
import os

client = OpenAI()

def upload_file(filepath):
    with open(filepath, "rb") as file:
        return client.files.create(file=file, purpose="fine-tune").id

def fine_tune_model(train_file_id, val_file_id):
    job = client.fine_tuning.jobs.create(
        training_file=train_file_id,
        validation_file=val_file_id,
        model="gpt-4o-2024-08-06"
    )
    print("Fine-tuning job started:", job.id)

if __name__ == "__main__":
    train_file_id = upload_file("data/train.jsonl")
    val_file_id = upload_file("data/val.jsonl")
    
    fine_tune_model(train_file_id, val_file_id)
