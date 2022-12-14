from cmath import nan
import os
import sys
from os.path import join
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(os.path.dirname(wdir), "Data-France-web-post-CS.csv")


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",", index_col=None)
        data.fillna(0, inplace=True)
        return data


def prepare_data(data, target):
    data = data[["score", "halfcentury", "subtitle1", "words"]]
    # Filter out novels with more than 1000k words (1 outlier) == optional!!
    if target == "score":
        print("items removed:", len(data[data["words"] > 1000].index))
        data = data.drop(data[data["words"] > 1000].index)
    # Filter out novels based on their genre subtitle
    del_rows = ["other", "conte", "memoires", "anecdote", "chronique", "roman"]
    for item in del_rows: 
        data = data.drop(data[data["subtitle1"] == item].index)
    # Filter data based on time of publication, depending on level of analysis
    if target == "score": 
        del_rows = ["1741-1760", "1761-1780", "1781-1800", "1801-1820", "1821-1840"]
        for item in del_rows: 
            data = data.drop(data[data["score"] == item].index)
    elif target == "halfcentury": 
        data = data.drop(data[data["halfcentury"] == "1801-1850"].index)
    #print(data.head())
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
        ax.text(-0.4, 345, "(NB.: Four novels with >1000k words were removed. Due to the low number of datapoints,\nthis strongly lowers the median of the boxplot for 'histoire' in the period 1641-1660.)", style='italic', fontsize=6)
    sns.move_legend(ax, "upper right")
    plt.savefig(filename, dpi=300)


def test_significance(prepared, target): 
    if target == "score": 
        from scipy.stats import kstest as kst
        unsub1620s = list(prepared[(prepared["score"] == "1621-1640") & (prepared["subtitle1"] == "unsubtitled")]["words"])
        unsub1640s = list(prepared[(prepared["score"] == "1641-1660") & (prepared["subtitle1"] == "unsubtitled")]["words"])
        histnouv1660s = list(prepared[(prepared["score"] == "1661-1680") & ((prepared["subtitle1"] == "histoire") | (prepared["subtitle1"]== "nouvelle"))]["words"])
        unsub1660s = list(prepared[(prepared["score"] == "1661-1680") & (prepared["subtitle1"] == "unsubtitled")]["words"])
        print(histnouv1660s)
        test1 = kst(unsub1620s, unsub1640s)
        print("Comparison: unsub1620s vs. unsubtitled 1640s:", test1)
        test2 = kst(histnouv1660s, unsub1660s)
        print("Comparison: histnouv1660s vs. unsubtitled 1660s:", test2)


def main(datafile):
    targets = ["score", "halfcentury"]
    for target in targets: 
        filename = join(wdir, "fig_4-4_box+scatter-"+target+".svg")
        data = read_data(datafile)
        prepared = prepare_data(data, target)
        test_significance(prepared, target)
        make_snsplot(prepared, filename, target)
    

main(datafile)

