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
    #print(data.shape)
    return data


def filter_data(data): 
    filtered  = data[["decade", "mode", "count"]]
    # Check and return
    #print(filtered.head())
    #print(filtered.shape)
    return filtered


def prepare_data(data):
    prepared = data.groupby(by=["decade", "mode"]).sum().unstack(fill_value=0).stack()
    prepared = prepared.reset_index()
    # Check and return
    print(prepared.tail(12))
    print(prepared.shape)
    return prepared


def plot_data(data, filename): 
    fig,ax = plt.subplots(figsize=(16,10))
    #sns.barplot(data=data, x="decade", y="count", hue="mode", palette="dark:grey")
    rw = np.add(data[data["mode"]=="rw"], data[data["mode"]=="mar"])
    rw = np.add(rw, data[data["mode"]=="al"])
    s1 = sns.barplot(x="decade", y="count", data=rw, color = 'DarkSlateGrey', label="real-world")
    mar = np.add(data[data["mode"]=="mar"], data[data["mode"]=="al"])
    s2 = sns.barplot(x="decade", y="count", data=mar, color = 'black', label="marvelous")
    al = data[data["mode"]=="al"]
    s3 = sns.barplot(x="decade", y="count", data=al, color = 'grey', label="alternate-world")
    loc = plticker.MultipleLocator(base=1)
    axes = sns.lineplot(data=data.loc["decade":])
    axes.xaxis.set_major_locator(loc)
    plt.xticks(rotation=90)
    plt.title("Overview of the dataset used (novels by mode and decade)")
    plt.ylabel("Number of novels")
    plt.legend(loc="upper left")
    plt.savefig(filename, dpi=300)
    print("Figure saved.")



def main(datafile):
    data = read_data(datafile)
    filename = join(wdir, "dataset-years+mode.svg")
    filtered = filter_data(data)
    prepared = prepare_data(filtered)
    plot_data(prepared, filename)

main(datafile)

