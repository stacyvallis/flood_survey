#!/usr/bin/env python

import pandas as pd

# Load dataset
df = pd.read_csv('results/filt_surveys_format_multi.tsv', sep='\t', index_col=0)

# Prepare output
records = []

for q in df.columns:
    # Get all unique options, excluding blanks and 'All of the previous'
    all_parts = (
        df[q].dropna()
        .str.split(',')
        .explode()
        .str.strip()
        .unique()
    )
    clean_options = [opt for opt in all_parts if opt and "All of" not in opt]

    # Count how many answered (not null)
    total_respondents = len(df)
    answered_count = df[q].notna().sum()
    unanswered_count = total_respondents - answered_count

    # Add row for unanswered
    if unanswered_count > 0:
        percent_unanswered = 100 * unanswered_count / total_respondents
        formatted_unanswered = f"{unanswered_count}/{total_respondents} ({percent_unanswered:.1f}%)"
        records.append((q, "Unanswered", formatted_unanswered))

    # Process responses
    for opt in clean_options:
        selected = 0
        for response in df[q].dropna():
            parts = [p.strip() for p in response.split(',') if p.strip()]
            if any("All of" in p for p in parts):
                parts.extend(clean_options)
            if opt in set(parts):
                selected += 1
        percent = 100 * selected / total_respondents
        formatted = f"{selected}/{total_respondents} ({percent:.1f}%)"
        records.append((q, opt, formatted))

# Convert to DataFrame
result = pd.DataFrame(records, columns=["question", "answer", "proportion"])

# Save
result.to_csv("results/multiproportions.tsv", sep="\t", index=False)
print("Proportions saved")

