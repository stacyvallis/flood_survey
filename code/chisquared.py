#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Theo Portlock (modified by ChatGPT)
This script calculates the Chi Squared test and Cramér's V for all pairs of categorical columns in a DataFrame.
"""

import argparse
import pandas as pd
import numpy as np
import os
from itertools import permutations
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association
from statsmodels.stats.multitest import fdrcorrection

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate Chi Squared test and Cramér's V for all pairs of categorical columns in a DataFrame.")
    parser.add_argument("file", type=str, help="Path to the input file (CSV or TSV format).")
    parser.add_argument("-o", "--output", type=str, help="Base name for output file (no extension).")
    return {k: v for k, v in vars(parser.parse_args()).items() if v is not None}

def load(subject):
    if os.path.isfile(subject):
        return pd.read_csv(subject, sep='\t', index_col=0)
    return pd.read_csv(f'../results/{subject}.tsv', sep='\t', index_col=0)

def save(df, subject, index=True):
    df.to_csv(subject, sep='\t', index=index)

def chi_squared(df: pd.DataFrame) -> pd.DataFrame:
    column_pairs = list(permutations(df.columns, 2))
    results = {
        'chi2': [],
        'pval': [],
        'dof': [],
        'cramers_v': []
    }

    for source, target in column_pairs:
        contingency_table = pd.crosstab(df[target], df[source])
        chi2_stat, pvalue, dof, expected = chi2_contingency(contingency_table)
        v = association(contingency_table, method="cramer")
        results['chi2'].append(chi2_stat)
        results['pval'].append(pvalue)
        results['dof'].append(dof)
        results['cramers_v'].append(v)

    index = pd.MultiIndex.from_tuples(column_pairs, names=['source', 'target'])
    result_df = pd.DataFrame(results, index=index)
    result_df['qval'] = fdrcorrection(result_df.pval)[1]
    return result_df

if __name__ == '__main__':
    args = parse_args()
    file_path = args['file']
    output_base = args.get('output')

    print(f"[INFO] Loading input data: {file_path}")
    df = load(file_path)

    print("[INFO] Running Chi Squared and Cramér's V analysis...")
    result = chi_squared(df)
    print("[INFO] Analysis complete. Top 5 results:")
    print(result.head())

    if not output_base:
        base = os.path.splitext(os.path.basename(file_path))[0]
        output_base = base + '_chisq'

    print(f"[INFO] Saving results to: {output_base}")
    save(result, output_base)

