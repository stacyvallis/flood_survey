#!/usr/bin/env python

import pandas as pd

# Load the Excel file and skip the first 17 rows
df = pd.read_excel('conf/questions.xlsx')
df = df.iloc[17:]

# Save the DataFrame to a TSV file
df.to_csv('results/questions.tsv', index=False, sep='\t')
