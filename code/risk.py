import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load and prepare data
df = pd.read_csv('results/edges.tsv', sep='\t')
questions = pd.read_csv('results/questions.tsv', sep='\t', index_col=0)

question = 'Q3'
df = df.query('source == "Q3" or target == "Q3"')
df = df.replace('Q3', np.nan)
ndf = df.rename(columns={'source': 'target', 'target': 'source'})
df = df.fillna(ndf).set_index(['source', 'target'])
df = df.drop_duplicates().droplevel(0)
df['power'] = df.qval.apply(np.log).mul(-1)
df = df.join(questions.short_question).set_index('short_question')

# Reset index for plotting
df = df.reset_index().rename(columns={'short_question': 'Variable'})

# Sort by power
df = df.sort_values('power', ascending=False)

# Plot using seaborn
plt.figure(figsize=(4, 6))

barplot = sns.barplot(
    data=df,
    y='Variable',
    x='power',
    hue='test',
    palette={'spearman': 'steelblue', 'kruskal': 'forestgreen'}
)

# Add vertical line at -log(0.05)
threshold = -np.log(0.05)
plt.axvline(x=threshold, color='gray', linestyle='--', linewidth=0.4)
plt.text(threshold + 0.05, -1, 'q = 0.05', color='gray', ha='left', va='center', fontsize=6)

# Titles and labels
plt.title('Variables associated with perceived flood risk (Spearman & Kruskal-Wallis)')
plt.xlabel('-log(q-value)')
plt.ylabel('')
plt.legend(title='Test Type', loc='lower right')

plt.tight_layout()
plt.savefig('results/combined_explainers_barplots.svg')
plt.show()

