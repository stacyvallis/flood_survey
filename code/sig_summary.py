#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import pandas as pd
from pathlib import Path

def load(subject):
    if os.path.isfile(subject):
        return pd.read_csv(subject, sep='\t', index_col=0)
    return pd.read_csv(f'../results/{subject}.tsv', sep='\t', index_col=0)

def save(df, subject, index=True):
    output_path = f'../results/{subject}.tsv' 
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep='\t', index=index)

def change_summary(df, change='coef', sig='qval', pval=0.25):
    total_rows = df.shape[0]
    sig_changed_count = df[sig].lt(pval).sum()
    changed = f"sig changed = {sig_changed_count}/{total_rows} ({round(sig_changed_count / total_rows * 100)}%)"
    sig_increased_count = df.loc[(df[sig] < pval) & (df[change] > 0), sig].lt(pval).sum()
    increased = f"sig up = {sig_increased_count}/{total_rows} ({round(sig_increased_count / total_rows * 100)}%)"
    sig_decreased_count = df.loc[(df[sig] < pval) & (df[change] < 0), sig].lt(pval).sum()
    decreased = f"sig down = {sig_decreased_count}/{total_rows} ({round(sig_decreased_count / total_rows * 100)}%)"
    return pd.Series([changed, increased, decreased])

def parse_arguments():
    parser = argparse.ArgumentParser(description='Produces a summary report of analysis')
    parser.add_argument('-i', '--input', required=True, help='Input file path (without extension)')
    parser.add_argument('-o', '--output', required=True, help='Output file path (without extension)')
    parser.add_argument('-p', '--pval', type=float, default=0.25, help='P-value threshold (default: 0.25)')
    parser.add_argument('-c', '--change', type=str, default='coef', help='Column name for change (default: "coef")')
    parser.add_argument('-s', '--sig', type=str, default='qval', help='Column name for significance (default: "qval")')
    return parser.parse_args()

def main():
    args = parse_arguments()

    input_path = args.input
    output_path = args.output
    pval = args.pval
    change = args.change
    sig = args.sig

    df = load(input_path)
    summary = change_summary(df, change=change, pval=pval, sig=sig)

    print(summary.to_string())
    save(summary, output_path)

if __name__ == '__main__':
    main()

