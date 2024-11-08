import json
from collections import Counter, defaultdict

cell_cycle_phases = [
    "Interphase", "G1", "S", "G2",
    "Mitosis", "Prophase", "Metaphase", "Anaphase", "Telophase"
]

def get_cell_cycle_phase(example):
    for phase in cell_cycle_phases:
        if phase.lower() in example["actual_answer"].lower():
            return phase
    return "Unknown"

def calculate_similarity(predicted, actual):
    if predicted == actual:
        return "Very Similar"
    elif predicted.lower() in actual.lower() or actual.lower() in predicted.lower():
        return "Mostly Similar"
    elif len(set(predicted.lower().split()) & set(actual.lower().split())) > 0:
        return "Somewhat Similar"
    return "Incorrect"

def evaluate_results(file_path):
    phase_counts = defaultdict(Counter)
    with open(file_path, "r") as f:
        for line in f:
            result = json.loads(line)
            phase = get_cell_cycle_phase(result)
            similarity = calculate_similarity(result["predicted_answer"], result["actual_answer"])
            phase_counts[phase][similarity] += 1

    return phase_counts

def calculate_accuracy(phase_counts):
    accuracy_by_phase = {}
    for phase, counts in phase_counts.items():
        total = sum(counts.values())
        correct = counts["Very Similar"] + counts["Mostly Similar"]
        accuracy_by_phase[phase] = (correct / total) * 100 if total > 0 else 0
    return accuracy_by_phase

if __name__ == "__main__":
    ft_counts = evaluate_results("ft_results.jsonl")
    base_counts = evaluate_results("base_results.jsonl")

    # Calculate accuracy by phase for both models
    ft_accuracy = calculate_accuracy(ft_counts)
    base_accuracy = calculate_accuracy(base_counts)

    # Save for plotting
    with open("evaluation_summary.json", "w") as f:
        json.dump({"ft_accuracy": ft_accuracy, "base_accuracy": base_accuracy, 
                   "ft_counts": ft_counts, "base_counts": base_counts}, f)
