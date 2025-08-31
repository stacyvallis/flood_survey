#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import os

def load(file_path):
    """Load the input TSV file."""
    if os.path.isfile(file_path):
        return pd.read_csv(file_path, sep='\t', index_col=0)
    else:
        raise FileNotFoundError(f"The file {file_path} does not exist.")

def save(df, output_file, index=True):
    """Save the filtered DataFrame to an output file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, sep='\t', index=index)

def filter(df, **kwargs):
    """Apply filters to the DataFrame based on provided arguments."""
    df.index = df.index.astype(str)
    if kwargs.get('filter_df') is not None:
        if kwargs.get('filter_df_axis') == 1:
            df = df.loc[:, kwargs.get('filter_df').index]
        else:
            df = df.loc[kwargs.get('filter_df').index]
    if kwargs.get('colfilt'):
        df = df.loc[:, df.columns.str.contains(kwargs.get('colfilt'), regex=True)]
    if kwargs.get('rowfilt'):
        df = df.loc[df.index.str.contains(kwargs.get('rowfilt'), regex=True)]
    if kwargs.get('prevail'):
        df = df.loc[:, df.agg(np.count_nonzero, axis=0).gt(df.shape[0]*kwargs.get('prevail'))]
    if kwargs.get('abund'):
        df = df.loc[:, df.mean().gt(kwargs.get('abund'))]
    if kwargs.get('min_unique'):
        df = df.loc[:, df.nunique().gt(kwargs.get('min_unique'))]
    if kwargs.get('nonzero'):
        df = df.loc[df.sum(axis=1) != 0, df.sum(axis=0) != 0]
    if kwargs.get('min_nonzero_rows') is not None:
        df = df[df.astype(bool).sum(axis=1) >= kwargs.get('min_nonzero_rows')]
    if kwargs.get('min_nonzero_cols') is not None:
        df = df.loc[:, df.astype(bool).sum(axis=0) >= kwargs.get('min_nonzero_cols')]
    if kwargs.get('numeric_only'):
        if ~(df.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())).any():
            df = pd.DataFrame()
    if kwargs.get('query'):
        df = df.query(kwargs.get('query'))
    if kwargs.get('dtype'):
        df = df.select_dtypes(kwargs.get('dtype'))
    if df.empty:
        return None
    else:
        return df

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Filter a TSV file based on various criteria.')
    parser.add_argument('input_file', help='Input TSV file')
    parser.add_argument('output_file', help='Output file for the filtered results')
    parser.add_argument('-rf', '--rowfilt', type=str, help='Regex for index filtering')
    parser.add_argument('-cf', '--colfilt', type=str, help='Regex for column filtering')
    parser.add_argument('-q', '--query', type=str, help='Pandas custom query')
    parser.add_argument('-m', '--min_unique', type=int, help='Minimum number of unique values')
    parser.add_argument('-fdf', '--filter_df', help='CSV file for filtering indices')
    parser.add_argument('-fdfx', '--filter_df_axis', type=int, help='Axis to filter the dataframe indices (0 or 1)')
    parser.add_argument('-absgt', type=float, help='Absolute greater than threshold')
    parser.add_argument('-p', '--prevail', type=float, help='Prevalence threshold')
    parser.add_argument('-a', '--abund', type=float, help='Abundance threshold')
    parser.add_argument('-s', '--suffix', type=str, help='Suffix to append to the subject for output')
    parser.add_argument('--numeric_only', action='store_true', help='Select numeric columns only')
    parser.add_argument('--nonzero', action='store_true', help='Remove rows and columns that sum to zero')
    parser.add_argument('--min_nonzero_rows', type=int, help='Minimum number of non-zero values required in a row')
    parser.add_argument('--min_nonzero_cols', type=int, help='Minimum number of non-zero values required in a column')
    parser.add_argument('--print_counts', action='store_true', help='Print the number of rows and columns that have been filtered')
    parser.add_argument('-dt', '--dtype', type=str, help='Select columns with a specific dtype')
    args = parser.parse_args()
    return {k: v for k, v in vars(args).items() if v is not None}

def main():
    """Main function to load, filter, and save the DataFrame."""
    known = parse_args()

    input_file = known.get("input_file")
    output_file = known.get("output_file")

    # Load the original DataFrame
    original_df = load(input_file)

    if known.get("filter_df"):
        known['filter_df'] = load(known.get("filter_df"))

    # Filter the DataFrame using the provided options
    output = filter(original_df.copy(), **known)

    # If print_counts flag is set, print the differences in rows and columns
    if known.get("print_counts"):
        if output is None:
            print("All rows and columns have been filtered out.")
        else:
            original_rows, original_cols = original_df.shape
            filtered_rows, filtered_cols = output.shape
            print(f"Rows filtered: {original_rows - filtered_rows} out of {original_rows}")
            print(f"Columns filtered: {original_cols - filtered_cols} out of {original_cols}")

    # Output the filtered DataFrame
    print(output)

    if output is not None:
        # Save the result to the output file
        save(output, output_file)

if __name__ == "__main__":
    main()

