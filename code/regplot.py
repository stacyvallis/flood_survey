#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import seaborn as sns

def parse_arguments():
    parser = argparse.ArgumentParser(description='Produces a regplot from a given dataset')
    parser.add_argument('--input', required=True, help='Input TSV file path')
    parser.add_argument('--output', required=True, help='Output filename without extension')
    parser.add_argument('-x', help='Column name for x-axis')
    parser.add_argument('-y', help='Column name for y-axis')
    parser.add_argument('--hue', help='Column name for hue grouping')
    parser.add_argument('--hue_order', help='Comma-separated order of hue categories')
    parser.add_argument('--logy', action='store_true', help='Set y-axis to log scale')
    parser.add_argument('--show', action='store_true', help='Display the plot window')
    parser.add_argument('--figsize', default='2,2', help='Figure size as width,height (default: 2,2)')
    return parser.parse_args()

def load_data(input_path):
    return pd.read_csv(input_path, sep='\t', index_col=0)

def plot_reg(df, x=None, y=None, hue=None, hue_order=None, ax=None, figsize=(2, 2)):
    df = df.reset_index()

    if x is None:
        x = df.columns[0]
    if y is None:
        y = df.columns[1]

    if hue and hue_order:
        hue_order_list = [s.strip() for s in hue_order.split(',')]
        df[hue] = pd.Categorical(df[hue], categories=hue_order_list, ordered=True)
    else:
        hue_order_list = None

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    sns.regplot(data=df, x=x, y=y, scatter=False, line_kws={"color": "red"}, ax=ax)

    if hue:
        sns.scatterplot(
            data=df,
            x=x,
            y=y,
            hue=hue,
            hue_order=hue_order_list,
            s=2,
            legend=False,
            ax=ax
        )
    else:
        sns.scatterplot(
            data=df,
            x=x,
            y=y,
            s=2,
            color='black',
            ax=ax
        )

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_linewidth(0.4)
    ax.spines['bottom'].set_linewidth(0.4)
    ax.tick_params(axis='both', which='major', width=0.4, size=4)
    ax.tick_params(axis='both', which='minor', width=0.4, size=2)

    return ax

def save_plot(output_path, show=False):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path = output_path.with_suffix('.svg')
    plt.savefig(svg_path)
    if show:
        plt.show()
    plt.clf()

def main():
    args = parse_arguments()

    figsize = tuple(map(float, args.figsize.split(',')))
    df = load_data(args.input)

    plot_reg(df, x=args.x, y=args.y, hue=args.hue, hue_order=args.hue_order, figsize=figsize)

    if args.logy:
        plt.yscale('log')

    plt.tight_layout()
    save_plot(args.output, show=args.show)

if __name__ == '__main__':
    main()

