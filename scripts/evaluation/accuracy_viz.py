import json
import matplotlib.pyplot as plt
from collections import Counter

# Load evaluation results
with open("evaluation_summary.json", "r") as f:
    data = json.load(f)
    ft_accuracy = data["ft_accuracy"]
    base_accuracy = data["base_accuracy"]
    ft_counts = data["ft_counts"]
    base_counts = data["base_counts"]

# Plot accuracy by cell cycle phase
phases = list(ft_accuracy.keys())
ft_values = [ft_accuracy[phase] for phase in phases]
base_values = [base_accuracy[phase] for phase in phases]

plt.figure(figsize=(10, 6))
bar_width = 0.35
indices = range(len(phases))

plt.bar(indices, ft_values, bar_width, label="Fine-Tuned Model")
plt.bar([i + bar_width for i in indices], base_values, bar_width, label="Base Model")

plt.xlabel("Cell Cycle Phase")
plt.ylabel("Accuracy (%)")
plt.title("Accuracy by Cell Cycle Phase")
plt.xticks([i + bar_width / 2 for i in indices], phases, rotation=45)
plt.legend()
plt.show()

# Plot similarity rating distribution
similarity_labels = ["Very Similar", "Mostly Similar", "Somewhat Similar", "Incorrect"]
ft_similarity_counts = Counter({label: ft_counts["total"][label] for label in similarity_labels})
base_similarity_counts = Counter({label: base_counts["total"][label] for label in similarity_labels})

ft_values = [ft_similarity_counts[label] for label in similarity_labels]
base_values = [base_similarity_counts[label] for label in similarity_labels]

plt.figure(figsize=(10, 6))
indices = range(len(similarity_labels))
plt.bar(indices, ft_values, bar_width, label="Fine-Tuned Model")
plt.bar([i + bar_width for i in indices], base_values, bar_width, label="Base Model")

plt.xlabel("Similarity Rating")
plt.ylabel("Count")
plt.title("Similarity Rating Distribution")
plt.xticks([i + bar_width / 2 for i in indices], similarity_labels)
plt.legend()
plt.show()
