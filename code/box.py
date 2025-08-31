#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import seaborn as sns

def parse_arguments():
    parser = argparse.ArgumentParser(description='Produces a Boxplot from a given dataset')
    parser.add_argument('--input', required=True, help='Path to input dataset file (.tsv)')
    parser.add_argument('--output', required=True, help='Output filename without extension (SVG will be enforced)')
    parser.add_argument('-x', required=True, help='Column name for x-axis')
    parser.add_argument('-y', required=True, help='Column name for y-axis')
    parser.add_argument('--order', help='Comma-separated order of categories on the x-axis')
    parser.add_argument('--hue', help='Column name for hue grouping')
    parser.add_argument('--logy', action='store_true', help='Set y-axis to log scale')
    parser.add_argument('--show', action='store_true', help='Display the plot window')
    parser.add_argument('--figsize', default='2,2', help='Figure size as width,height')
    parser.add_argument('--meta', nargs='+', help='Path(s) to metadata file(s) to inner-join with input data before plotting')
    return parser.parse_args()

def load_data(filepath):
    return pd.read_csv(filepath, sep='\t', index_col=0)

def merge_meta(df, meta_paths):
    for mpath in meta_paths:
        mdf = pd.read_csv(mpath, sep=None, engine='python', index_col=0)
        df = df.join(mdf, how='inner')
    return df

def plot_box(df, x, y, hue, figsize, order):
    df = df.reset_index()

    if order:
        order_list = [s.strip() for s in order.split(',')]
        df[x] = pd.Categorical(df[x], categories=order_list, ordered=True)
    else:
        order_list = None

    fig, ax = plt.subplots(figsize=figsize)

    sns.boxplot(
        data=df,
        x=x,
        y=y,
        hue=hue,
        ax=ax,
        order=order_list,
        showfliers=False,
        showcaps=False,
        linewidth=0.4,
        boxprops={'edgecolor': 'black'},
        whiskerprops={'color': 'black'},
        medianprops={'color': 'black'},
        capprops={'color': 'black'}
    )

    sns.stripplot(
        data=df,
        x=x,
        y=y,
        hue=hue if not hue else None,  # avoid double legend
        ax=ax,
        order=order_list,
        size=1,
        color='black',
        dodge=bool(hue)
    )

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    return ax

def save_plots(output_filename, show):
    out_path = Path(output_filename).with_suffix('.svg')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)
    if show:
        plt.show()
    plt.clf()

def main():
    args = parse_arguments()

    df = load_data(args.input)
    if args.meta:
        df = merge_meta(df, args.meta)

    figsize = tuple(map(float, args.figsize.split(',')))
    ax = plot_box(df, args.x, args.y, args.hue, figsize, args.order)

    if args.logy:
        ax.set_yscale('log')

    plt.tight_layout()
    save_plots(args.output, args.show)

if __name__ == '__main__':
    main()

