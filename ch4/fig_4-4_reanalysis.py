from cmath import nan
import os
import sys
from os.path import join
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(os.path.dirname(wdir), "Data-France-web-post_CS2.csv")


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",", index_col=None)
        data.fillna(0, inplace=True)
        return data


def prepare_data(data, target):
    # Filter out novels with more than 1000k words (1 outlier) == optional!!
    if target == "score":
        data.drop(data[data["words"] > 1000].index, inplace=True)
    # Filter out novels based on their genre subtitle
    del_rows = ["other", "conte", "memoires", "anecdote", "chronique", "roman"]
    for item in del_rows: 
        data.drop(data[data["subtitle1"] == item].index, inplace=True)
    # Filter data based on time of publication, depending on level of analysis
    if target == "score": 
        del_rows = ["1741-1760", "1761-1780", "1781-1800", "1801-1820", "1821-1840"]
        for item in del_rows: 
            data.drop(data[data["score"] == item].index, inplace=True)
    elif target == "halfcentury": 
        data.drop(data[data["halfcentury"] == "1801-1850"].index, inplace=True)
    print(data.head())
    return data


def make_snsplot(prepared, filename, target):
    fig,ax = plt.subplots(figsize=(10, 6))
    ax = sns.boxplot(data=prepared, x=target, y="words", hue="subtitle1", palette="light:grey", showfliers=False)
    ax = sns.stripplot(data=prepared, x=target, y="words", hue="subtitle1", jitter=0.15, size=2.5, palette="dark:black", dodge=True)
    ax.set_title('Figure 4.4: Lengths of novels by subtitle (reanalysis)')
    ax.set_ylabel('Number of words (in thousands)')
    ax.set_xlabel('Time interval')
    plt.ylim(0,360) 
    plt.tight_layout()
    ax.legend(scatterpoints=0)
    if target == "score": 
        ax.text(-0.4, 345, "(NB.: One outlier with 1000k words was removed. Due to the low number of datapoints,\nthis strongly lowers the median of the boxplot for 'histoire' in the period 1641-1660.)", style='italic', fontsize=6)
    sns.move_legend(ax, "upper right")
    plt.savefig(filename, dpi=300)


def main(datafile):
    targets = ["score", "halfcentury"]
    for target in targets: 
        filename = join(wdir, "fig_4-4_box+scatter-"+target+".svg")
        data = read_data(datafile)
        prepared = prepare_data(data, target)
        make_snsplot(prepared, filename, target)
    

main(datafile)

