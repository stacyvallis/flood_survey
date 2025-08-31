#!/usr/bin/env python
import pandas as pd
from collections import defaultdict

# Load questions
questions = pd.read_excel("conf/questions.xlsx", index_col=0)

# Load surveys
survey1 = pd.read_excel("data/Public Perceptions of Flood Risk for Residental Neighbourhoods in West Auckland, New Zealand_March 8, 2025_19.57.xlsx", header=0).iloc[1:]
survey2 = pd.read_excel("data/Public Perceptions of Flood Risk for Residental Neighbourhoods in West Auckland, New Zealand_March 9, 2025_15.58.xlsx", header=0).iloc[1:]
survey3 = pd.read_excel("data/Public Perceptions of Flood Risk for Residential Neighbourhoods in West Auckland, New Zealand_March 9, 2025_15.56.xlsx", header=0).iloc[1:]

# Name surveys
survey1["Site"] = "Mount Eden"
survey2["Site"] = "New Lynn"
survey3["Site"] = "New Lynn"

# Merge
df = pd.concat([survey1,survey2,survey3])

# Filter to remove the unusable data
df = df.loc[:, questions.dropna().index]

# Filter whitespaces
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Format risk column
question = 'Q3'
df[question] = df[question].str.split(' ', expand=True).iloc[:, 0].astype(float)

# Format distance column
question = 'Q7'
df[question] = df[question].str.split(' ', expand=True).iloc[:, 0].astype(float)

# Format trust column
question='Q12'
df[question] = df[question].str.split(' ', expand=True).iloc[:, 0].astype(float)

# Format neigherbourhood column
question='Q13'
df[question] = df[question].str.split(' ', expand=True).iloc[:, 0].astype(float)

# Update age categories
mapping = {'19-34':'18-34', '54-74':'55-74'}
df['Q1'] = df['Q1'].replace(mapping)

# Save
df.to_csv("results/surveys.tsv", sep="\t")

