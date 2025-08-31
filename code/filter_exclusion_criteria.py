#!/usr/bin/env python
import pandas as pd

# Load surveys
df = pd.read_csv('results/surveys.tsv', sep='\t', index_col=0)

# Original count
total_respondents = df.shape[0]

# Filter those respondents who have not answered the age range question
filtdf = df.dropna(subset=['Q1'])

# Filter those respondents who have not answered the location question or have answered 'Other'
filtdf = filtdf.dropna(subset=['Q2'])
filtdf = filtdf.loc[~filtdf['Q2'].isin(['Other'])]

# Save filtered data
filtdf.to_csv('results/filt_surveys.tsv', sep='\t')

# Count filtered respondents
filtered_count = filtdf.shape[0]
excluded_count = total_respondents - filtered_count

# Print summary
print(f"Total respondents after filtering: {filtered_count} out of {total_respondents} ({(filtered_count / total_respondents) * 100:.1f}%)")
print(f"Excluded respondents: {excluded_count}")
