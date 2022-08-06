import pandas as pd
import numpy as np
import os
import sys
from os.path import join
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as plticker

wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(os.path.dirname(wdir), "Data-France-web-post-CS.csv")


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",")
    data.fillna(0, inplace=True)

    # Check and return
    #print(data.head())
    print(data.shape)
    #print(data.columns)
    return data


def filter_data(data): 
    filtered = data[["decade", "characters-rw", "words"]]
    filtered = filtered[filtered["characters-rw"] == "nobodies"] 
    del_decades = ["1600s", "1610s", "1620s", "1630s", "1640s", "1650s", "1660s", "1670s", "1680s", "1690s"]
    for item in del_decades: 
        filtered.drop(filtered[filtered["decade"] == item].index, inplace=True)
    
    # Check and return
    #print(filtered.head())
    print(filtered.shape)
    return filtered


def prepare_data(data):
    # Reference information
    prepared = data.drop(["characters-rw"], axis=1)

    # Check and return
    #print(prepared)
    print(prepared.shape)
    return prepared


def plot_data(data, results, filename): 
    fig,ax = plt.subplots(figsize=(16,10))
    sns.boxplot(data=data, x="decade", y="words", color="LightGrey", showfliers=False)
    sns.stripplot(data=data, x="decade", y="words", jitter=0.15, size=3, palette="dark:black", dodge=True)
    plt.title('Figure 8.2: Length of nobody novels (reanalysis)', fontsize=18)
    plt.ylabel('Number of words (in thousands)', fontsize=16)
    plt.xticks(rotation=0, fontsize=14)
    plt.yticks(rotation=0, fontsize=14)
    plt.ylim(0, 220)
    ax.text(-0.4, 210, "(NB.: The result of a test for a statistically significant difference between\nthe length distributions for the 1770s vs. the 1820s indicates a p-value of 0.012.)", style='italic', fontsize=10)
    plt.savefig(filename, dpi=300)
    print("Figure saved.")


def test_significance(prepared): 
    from scipy.stats import kstest as kst
    w1700s = list(prepared[prepared["decade"] == "1700s"]["words"])
    w1770s = list(prepared[prepared["decade"] == "1770s"]["words"])
    w1780s = list(prepared[prepared["decade"] == "1780s"]["words"])
    w1820s = list(prepared[prepared["decade"] == "1820s"]["words"])
    kst_1700s_1820s = kst(w1700s, w1820s)
    kst_1770s_1780s = kst(w1770s, w1780s)
    results = {"1700s-vs-1820s" : kst_1700s_1820s, "1770s-vs-1780s" : kst_1770s_1780s}
    print(results)
    return results


def main(datafile):
    data = read_data(datafile)
    filename = join(wdir, "fig_8-2_box+scatter.svg")
    filtered = filter_data(data)
    prepared = prepare_data(filtered)
    results = test_significance(prepared)
    plot_data(prepared, results, filename)

main(datafile)

