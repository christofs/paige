import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import os
import sys
from os.path import join

wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(os.path.dirname(wdir), "Data-France-web-post-CS.csv")


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",")
    data.fillna(0, inplace=True)
    # Check and return
    #print(data.head())
    print(data.shape)
    return data


def filter_data(data): 
    filtered  = data[["year", "words"]]
    # Check and return
    #print(filtered.head())
    print(filtered.shape)
    return filtered


def prepare_data(data):
    prepared = data.drop(data[data["words"] > 1000].index)
    # Check and return
    # print(prepared.head())
    print(prepared.shape)
    return prepared


def plot_data(data, filename): 
    fig,ax = plt.subplots(figsize=(16,10))
    sns.scatterplot(data=data, x="year", y="words", color="black", legend=False, markers="x", s=16, alpha=0.6)
    ax.text(0, 345, "(NB.: Four novels with <1000k words were removed.)", style='italic', fontsize=6)
    loc = plticker.MultipleLocator(base=10)
    axes = sns.lineplot(data=data.loc["year":])
    axes.xaxis.set_major_locator(loc)
    plt.xticks(rotation=90)
    plt.title("Overview of the dataset used")
    plt.ylabel("Length of the novels (in thousands of words)")
    plt.savefig(filename, dpi=300)



def main(datafile):
    data = read_data(datafile)
    filename = join(wdir, "dataset1.svg")
    filtered = filter_data(data)
    prepared = prepare_data(filtered)
    plot_data(prepared, filename)

main(datafile)

