#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
import os
from scipy.stats import kruskal
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='''
    Kruskal-Wallis test for categorical columns with respect to numeric columns.
    ''')
    parser.add_argument('subject', type=str, help='Table containing numeric variables')
    parser.add_argument('df2', type=str, help='Table containing categorical labels')
    parser.add_argument('-o', '--output', type=str, help='Base name for output file (without extension)')
    args = parser.parse_args()
    return {k: v for k, v in vars(args).items() if v is not None}

def load(subject):
    if os.path.isfile(subject):
        return pd.read_csv(subject, sep='\t', index_col=0)
    return pd.read_csv(f'../results/{subject}.tsv', sep='\t', index_col=0)

def save(df, subject, index=True):
    df.to_csv(subject, sep='\t', index=index)

def kruskal_wallis_test(df, df2):
    results = []
    for cat_col in df2.columns:
        if df2[cat_col].nunique() < 2:
            continue  # Skip columns with only one category

        for num_col in df.columns:
            valid_idx = df2[cat_col].notna() & df[num_col].notna()
            filtered_df = df[valid_idx]
            filtered_df2 = df2[valid_idx]

            groups = [filtered_df[num_col][filtered_df2[cat_col] == category] for category in filtered_df2[cat_col].unique()]

            if len(groups) > 1 and all(len(g) > 0 for g in groups):
                unique_values = [g.nunique() for g in groups]
                if all(u == 1 for u in unique_values):
                    continue  # Skip if all values in all groups are identical

                stat, p = kruskal(*groups)
                results.append({'source': cat_col, 'target': num_col, 'statistic': stat, 'p_value': p})

    return pd.DataFrame(results)

if __name__ == "__main__":
    known = parse_args()
    subject = known["subject"]
    df2_path = known["df2"]
    output_base = known.get("output")

    print(f"[INFO] Loading numeric dataset: {subject}")
    df = load(subject)
    print(f"[INFO] Loading categorical dataset: {df2_path}")
    df2 = load(df2_path)

    print("[INFO] Performing Kruskal-Wallis tests...")
    output = kruskal_wallis_test(df, df2)
    print("[INFO] Test results (showing top 5):")
    print(output.head())

    if not output_base:
        output_base = subject + '_kruskal'

    print(f"[INFO] Saving results to: {output_base}")
    save(output, output_base)

