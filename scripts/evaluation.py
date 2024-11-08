from collections import Counter
from matplotlib import pyplot as plt

results_ft = []
with open("ft-results.jsonl", "r") as f:
    for line in f:
        results_ft.append(json.loads(line))

ratings_ft = [result['rating'] for result in results_w_scores if result['type'] == 'Open']

rating_counts_ft = Counter(ratings_ft)

bar_width = 0.35
index = range(len(rating_order))

fig, ax = plt.subplots()
bar1 = ax.bar(index, [rating_counts_ft.get(rating, 0) for rating in rating_order], bar_width, label='FT GPT-4o')

ax.set_xlabel('Ratings')
ax.set_ylabel('Count')
ax.set_title('Ratings Distribution')
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(rating_order)
ax.legend()

plt.show()
