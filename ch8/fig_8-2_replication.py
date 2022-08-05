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
    #decades = ["1700s","1710s","1720s","1730s","1740s","1750s","1760s","1770s","1780s","1790s","1800s","1810s","1820s"]
    prepared = data.groupby(by="decade").median()

    # Check and return
    print(prepared)
    print(prepared.shape)
    return prepared


def plot_data(data, filename): 
    fig,ax = plt.subplots(figsize=(16,10))
    line = sns.lineplot(data=data, palette="dark:grey", linewidth=3, legend=False)
    plt.title('Figure 8.2: Median length of nobody novels (replication)', fontsize=18)
    plt.ylabel('Number of words (in thousands)', fontsize=16)
    plt.xticks(rotation=0, fontsize=14)
    plt.yticks(rotation=0, fontsize=14)
    plt.ylim(0, 80)
    #plt.locator_params(nbins=10)
    plt.savefig(filename, dpi=300)


    print("Figure saved.")



def main(datafile):
    data = read_data(datafile)
    filename = join(wdir, "fig_8-2_replication.svg")
    filtered = filter_data(data)
    prepared = prepare_data(filtered)
    plot_data(prepared, filename)

main(datafile)

