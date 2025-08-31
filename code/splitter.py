#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import pandas as pd

def load(subject):
    if os.path.isfile(subject):
        if subject.endswith(".xlsx"):
            return pd.read_excel(subject, index_col=0)
        else:
            return pd.read_csv(subject, sep='\t', index_col=0)
    elif os.path.isfile(f'../results/{subject}.xlsx'):
        return pd.read_excel(f'../results/{subject}.xlsx', index_col=0)
    else:
        return pd.read_csv(f'../results/{subject}.tsv', sep='\t', index_col=0)

def save(df, subject, index=True):
    output_path = f'results/{subject}.tsv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep='\t', index=index)

def splitter(df, df2, col):
    output = {}
    if df2 is None:
        df2 = df.copy()
    for level in df2[col].dropna().unique():
        merged = df.loc[:, df2.loc[df2[col] == level, col].index]
        output[level] = merged
    return output

def parse_args():
    parser = argparse.ArgumentParser(description='''
Splitter - splits dataframes according to the values in a defined column
''')
    parser.add_argument('subject', help='Name or path to the main TSV or Excel file')
    parser.add_argument('column', help='Column name to split on')
    parser.add_argument('--df2', help='Optional second dataframe to split by', required=False)
    return parser.parse_args()

def main():
    args = parse_args()
    df = load(args.subject)
    df2 = load(args.df2) if args.df2 else None
    col = args.column
    subject = os.path.splitext(os.path.basename(args.subject))[0]
    output = splitter(df, df2, col)

    for level, out_df in output.items():
        safe_level = str(level).replace(" ", "_").replace("/", "_")
        save(out_df, f'{subject}_{col}_{safe_level}')

if __name__ == '__main__':
    main()
