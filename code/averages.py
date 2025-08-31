#!/usr/bin/env python

import pandas as pd

# Load data
df = pd.read_csv('results/filt_surveys_format_numeric.tsv', sep='\t', index_col=0)

# Calculate averages
average = df.agg(['mean','std']).T
print(average)

# Save the averages to a file
average.to_csv('results/averages.tsv', sep='\t')
