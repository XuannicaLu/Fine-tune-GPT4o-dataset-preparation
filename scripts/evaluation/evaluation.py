import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from tqdm import tqdm
from openai import OpenAI

client = OpenAI()

# Load test data from JSONL
test_data = []
with open("cell_cycle_test.jsonl", "r") as f:
    for line in f:
        test_data.append(json.loads(line))

def process_example(example, model):
    response = client.chat.completions.create(
        model=model,
        messages=example["messages"],
        store=True
    )
    predicted_answer = response.choices[0].message.content.strip()

    # Extract example ID
    example_id = int(re.search(r'\[(\d+)\]', example["messages"][-1]["content"][0]["text"]).group(1))
    actual_answer = example["actual_answer"]

    return {
        "example_id": example_id,
        "predicted_answer": predicted_answer,
        "actual_answer": actual_answer
    }

def run_inference(model_name, output_file):
    results = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_example, example, model_name): example for example in test_data}
        for future in tqdm(as_completed(futures), total=len(futures)):
            results.append(future.result())

    with open(output_file, "w") as f:
        for result in results:
            json.dump(result, f)
            f.write("\n")

if __name__ == "__main__":
    # Fine-tuned model inference
    run_inference("ft:gpt-4o-2024-08-06:", "ft_results.jsonl")

    # Base model inference
    run_inference("gpt-4o", "base_results.jsonl")
