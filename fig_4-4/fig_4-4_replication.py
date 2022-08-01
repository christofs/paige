from cmath import nan
import os
import sys
from os.path import join
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint as scf


wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(os.path.dirname(wdir), "Data-France-web-post_CS2.csv")
#wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
#datafile = join(wdir, "Data-France-web-post_CS-fig4-4.csv")
aggregations = ["paige44"]


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",")
        data.fillna(0, inplace=True)
        data = data[["paige44", "subtitle1", "words"]]
        print(data.head())
        return data


def group_data(data, agg):
    grouped = data.groupby(by=["subtitle1", agg]).median()
    #grouped.drop("year", axis=1, inplace=True)
    #print(grouped)
    return grouped


def plot_data(grouped, filename): 
    untitled = grouped.query("subtitle1 == 'unsubtitled'").loc["unsubtitled",:]
    untitled.drop("1751-1780", axis=0, inplace=True)
    untitled.drop("1781-1800", axis=0, inplace=True)
    untitled.drop("1801-1820", axis=0, inplace=True)
    untitled.drop("1821-1840", axis=0, inplace=True)
    #print(untitled)
    labels = list(untitled.index)
    #print(labels)
    fig,ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(labels))
    y = untitled["words"]
    plt.ylim(0,120)
    ax.set_xticks(x, labels)
    #for i in range(len(labels)):
    #    ax.text(x[i]+0.0, y[i]+1.0, str(int(y[i])), size=8)
    ax.plot(x, y, "k--", label="untitled")

    histoire = grouped.query("subtitle1 == 'histoire'").loc["histoire",:]
    histoire.drop("1751-1780", axis=0, inplace=True)
    histoire.drop("1781-1800", axis=0, inplace=True)
    histoire.drop("1801-1820", axis=0, inplace=True)
    histoire.drop("1821-1840", axis=0, inplace=True)
    y = histoire["words"]
    #for i in range(len(labels)):
    #    ax.text(x[i]+0.0, y[i]+0.0, str(int(y[i])), size=8)
    ax.plot(x, y, color="grey", linestyle="-", label="histoire")

    nouvelle = grouped.query("subtitle1 == 'nouvelle'").loc["nouvelle",:]
    nouvelle.drop("1751-1780", axis=0, inplace=True)
    nouvelle.drop("1781-1800", axis=0, inplace=True)
    nouvelle.drop("1801-1820", axis=0, inplace=True)
    nouvelle.drop("1821-1840", axis=0, inplace=True)
    missing = pd.DataFrame([["1601-1620", np.nan], ["1621-1640", np.nan]], columns=["paige44", "words"]).set_index("paige44")
    #nouvelle.drop("1641-1660", axis=0, inplace=True)
    #missing = pd.DataFrame([["1601-1620", np.nan], ["1621-1640", np.nan], ["1641-1660", np.nan]], columns=["paige", "words"]).set_index("paige")
    nouvelle = pd.concat([missing, nouvelle])
    print(nouvelle)
    labels = list(nouvelle.index)
    x = np.arange(len(labels))
    y = nouvelle["words"]  
    #for i in range(len(labels)):
    #    if y[i] > 1: 
    #        ax.text(x[i]+0.0, y[i]-2.0, str(int(y[i])), size=8)

    ax.plot(x, y, "k-", label="nouvelle")
    ax.yaxis.grid(False)
    plt.text(2.15, 96, "← unsubtitled",)
    plt.text(2.0, 50, "histoire ↗",)
    plt.text(4.0, 20, "↖ nouvelle",)
    ax.set_title('Figure 4.4: Median lengths of novels by subtitle (replication)')
    ax.set_ylabel('Number of words (in thousands)')
    #plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)


def main(datafile, aggregations):
    data = read_data(datafile)
    for agg in aggregations: 
        grouped = group_data(data, agg)
        filename = join(wdir, "fig_4-4_replication-lineplot-"+agg+".svg")
        plot_data(grouped, filename)

main(datafile, aggregations)

