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
    #print(data.shape)
    #print(data.columns)
    return data


def filter_data(data): 
    filtered = data[["decade", "mode", "count", "truth-rw", "characters-rw", "person"]]
    filtered = filtered[filtered["characters-rw"] == "nobodies"] 
    del_decades = ["1600s", "1610s", "1620s", "1630s", "1640s", "1650s", "1660s", "1670s", "1680s", "1690s"]
    for item in del_decades: 
        filtered.drop(filtered[filtered["decade"] == item].index, inplace=True)
    # Check and return
    #print(filtered.head())
    #print(filtered.shape)
    return filtered


def prepare_data(data):
    # Reference information
    decades = ["1700s","1710s","1720s","1730s","1740s","1750s","1760s","1770s","1780s","1790s","1800s","1810s","1820s"]
    totals = data.groupby(by="decade").count().drop(["mode", "truth-rw", "characters-rw", "person"], axis=1)

    # Define data for the first kind of novel
    novel1 = data[(data["truth-rw"] == "fict") | (data["truth-rw"] == "ind") & (data["person"] != "3")] 
    novel1 = novel1.drop(["mode", "truth-rw", "characters-rw", "person"], axis=1)
    novel1 = novel1.groupby(by="decade").count().T
    novel1 = novel1.reindex(columns=decades, fill_value=0).T   
    novel1 = np.divide(novel1, totals)*100
    novel1 = novel1.round(1).rename({"count": "type 1"}, axis=1)

    # Define data for the second kind of novel
    novel2 = data[(data["person"] == "3") & (data["truth-rw"] != "fict") & (data["truth-rw"] != "ind")] # filter for nobody novel unnecessary; only nobody novels are included here. 
    novel2 = novel2.drop(["mode", "truth-rw", "characters-rw", "person"], axis=1)
    novel2 = novel2.groupby(by="decade").count().T
    novel2 = novel2.reindex(columns=decades, fill_value=0).T   
    novel2 = np.divide(novel2, totals)*100
    novel2 = novel2.round(1).rename({"count": "type 2"}, axis=1)


    # Define data for the third kind of novel: 
    novel3 = data[(data["truth-rw"] == "fict") | (data["truth-rw"] == "ind") & (data["person"] == "3")] 
    novel3 = novel3.drop(["mode", "truth-rw", "characters-rw", "person"], axis=1)
    novel3 = novel3.groupby(by="decade").count().T
    novel3 = novel3.reindex(columns=decades, fill_value=0).T   
    novel3 = np.divide(novel3, totals)*100
    novel3 = novel3.round(1).rename({"count": "type 3"}, axis=1)


    # Merge the data
    data = pd.concat([totals, novel1, novel2, novel3], axis=1).rename({"count": "totals"}, axis=1)

    # Check and return
    #print(novel1)
    #print(novel1.shape)
    #print(novel2)
    #print(novel2.shape)
    print(data)
    print(data.shape)
    prepared = data
    #prepared = [novel1, novel2, totals]
    return prepared

def calculate_correlation(data): 
    matrix = np.corrcoef(data["type 1"], data["type 2"])
    print(matrix)
    corr = np.round(matrix[0][1], 2)
    print(corr)
    return corr


def plot_data(data, corr, filename): 
    fig,ax = plt.subplots(figsize=(16,10))
    line1 = sns.lineplot(data=data["type 1"], color="black", linewidth=3)
    line2 = sns.lineplot(data=data["type 2"], color="grey", linewidth=3)
    line3 = sns.lineplot(data=data["type 3"], color="LightGrey", linewidth=3)
    #data[0].plot(kind='line', color="black")
    plt.ylim(0, 100)
    plt.title('Figure 8.1: Truth posture and narrative person (replication)', fontsize=18)
    plt.ylabel('Production of nobody novels (percentages)', fontsize=16)
    plt.xlabel("", fontsize=16)
    plt.locator_params(nbins=10)
    plt.legend(loc="lower center", ncol=2)
    plt.text(5.2, 55, "invented and indeterminate novels\n(only non-third person) ↘", fontsize=12)
    plt.text(6.5, 20, "↙ third-person novels (only not\ninvented or indeterminate)", fontsize=12)
    plt.text(6.5, 70, "third-person novels that are\nalso invented or indeterminate ↘", fontsize=12)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    totalstext = "Number of all nobody novels per decade:\n " + "                 ".join([str(item) for item in data["totals"]])
    plt.text(-0.1, 2, str(totalstext), fontsize=10)
    plt.text(-0.1, 95, "(NB.: Pearson's r = " + str(corr) + ".)", fontsize=10)
    plt.savefig(filename, dpi=300)


    print("Figure saved.")



def main(datafile):
    data = read_data(datafile)
    filename = join(wdir, "fig_8-1_reanalysis2.svg")
    filtered = filter_data(data)
    prepared = prepare_data(filtered)
    corr = calculate_correlation(prepared)
    plot_data(prepared, corr, filename)

main(datafile)

