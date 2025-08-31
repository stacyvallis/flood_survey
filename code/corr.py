#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import pandas as pd
from scipy.stats import spearmanr
from statsmodels.stats.multitest import fdrcorrection
from itertools import permutations

def parse_args():
    parser = argparse.ArgumentParser(description='''
    Corr - Produces a report of the significant correlations between data
    ''')
    parser.add_argument('subject', nargs='+', help='Input file(s)')
    parser.add_argument('-m', '--mult', action='store_true', help='Apply FDR correction')
    parser.add_argument('-o', '--output', type=str, help='Base name for output files (without extension)')
    args = parser.parse_args()
    return {k: v for k, v in vars(args).items() if v is not None}

def load(subject):
    if os.path.isfile(subject):
        return pd.read_csv(subject, sep='\t', index_col=0)
    return pd.read_csv(f'../results/{subject}.tsv', sep='\t', index_col=0)

def save(df, subject, index=True):
    df.to_csv(subject, sep='\t', index=index)

def corrpair(df1, df2, FDR=True, min_unique=0):
    print("[INFO] Filtering columns with low variability...")
    df1 = df1.loc[:, df1.nunique() > min_unique]
    df2 = df2.loc[:, df2.nunique() > min_unique]
    print("[INFO] Joining dataframes on index...")
    df = df1.join(df2, how='inner')
    print(f"[INFO] Performing Spearman correlation on {df.shape[0]} samples...")
    cor, pval = spearmanr(df)
    cordf = pd.DataFrame(cor, index=df.columns, columns=df.columns)
    pvaldf = pd.DataFrame(pval, index=df.columns, columns=df.columns)
    cordf = cordf.loc[df1.columns, df2.columns]
    pvaldf = pvaldf.loc[df1.columns, df2.columns]
    pvaldf.fillna(1, inplace=True)
    if FDR:
        print("[INFO] Applying FDR correction...")
        pvaldf = pd.DataFrame(
            fdrcorrection(pvaldf.values.flatten())[1].reshape(pvaldf.shape),
            index=pvaldf.index,
            columns=pvaldf.columns)
    return cordf, pvaldf

def corr(df):
    combs = list(permutations(df.columns.unique(), 2))
    print(f"[INFO] Computing pairwise correlations for {len(combs)} pairs...")
    outdf = pd.DataFrame(index=pd.MultiIndex.from_tuples(combs), columns=['cor','pval'])
    for comb in combs:
        tdf = pd.concat([df[comb[0]], df[comb[1]]], axis=1).dropna()
        cor, pval = spearmanr(tdf[comb[0]], tdf[comb[1]])
        outdf.loc[comb, 'cor'] = cor
        outdf.loc[comb, 'pval'] = pval
    print("[INFO] Applying FDR correction...")
    outdf['qval'] = fdrcorrection(outdf.pval)[1]
    outdf.index.set_names(['source', 'target'], inplace=True)
    return outdf

if __name__ == '__main__':
    known = parse_args()
    subject = known.get("subject")
    mult = known.get("mult") if known.get('mult') else False
    output_base = known.get("output")

    if len(subject) == 1:
        print(f"[INFO] Loading data from: {subject[0]}")
        df = load(subject[0])
        print("[INFO] Performing intra-dataset correlation analysis...")
        output = corr(df)
        print("[INFO] Correlation matrix:")
        print(output.head())
        if not output_base:
            output_base = subject[0] + 'corr'
        print(f"[INFO] Saving results to: {output_base}")
        save(output, output_base)

    elif len(subject) == 2:
        print(f"[INFO] Loading data from: {subject[0]}")
        df1 = load(subject[0])
        print(f"[INFO] Loading data from: {subject[1]}")
        df2 = load(subject[1])
        print("[INFO] Performing inter-dataset correlation analysis...")
        cor, pval = corrpair(df1, df2, FDR=mult)
        print("[INFO] Correlation matrix:")
        print(cor.head())
        if not output_base:
            output_base = subject[0] + subject[1]
        cor_out = output_base + 'corr'
        pval_out = output_base + 'corrpval'
        print(f"[INFO] Saving correlation coefficients to: {cor_out}")
        save(cor, cor_out)
        print(f"[INFO] Saving p-values (FDR corrected: {mult}) to: {pval_out}")
        save(pval, pval_out)

    else:
        print("[ERROR] Invalid number of arguments. Provide one or two input files.")

