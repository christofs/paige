
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint as scf
import os
import sys
from os.path import join

wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(os.path.dirname(wdir), "Data-France-web-post-CS.csv")
#datafile = join(wdir, "Data-France-web-post_CS_fig3-3_mod1.csv")


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",")
    data.fillna(0, inplace=True)
    #print(data.head())
    return data


def filter_data(data): 
    filtered = data[["decade", "inset", "halfcentury", "titled insets?"]]
    filtered = filtered.rename({"titled insets?" : "titled"}, axis=1)
    halfcenturies = ["1701-1750", "1751-1800", "1801-1850"]
    for item in halfcenturies: 
        filtered = filtered.drop(filtered[filtered["halfcentury"] == item].index)
    filtered = filtered.drop(filtered[filtered["inset"] != "i1"].index)
    filtered = filtered.drop(["halfcentury", "inset"], axis=1)

    # Check and return
    #print(filtered.head())
    print("filtered", filtered.shape)
    return filtered


def prepare_data(data):
    binary = pd.get_dummies(data["titled"])
    prepared = pd.concat((binary, data), axis=1)
    prepared = prepared.drop(["titled"], axis=1)
    prepared = prepared.rename(columns={"y": "titled", "n" : "untitled"})
    prepared = prepared.groupby(by="decade").sum()
    prepared["total"] = prepared["titled"] + prepared["untitled"]        
    prepared["titled"] = prepared["titled"] / prepared["total"] * 100
    prepared["untitled"] = prepared["untitled"] / prepared["total"] * 100
    prepared = prepared.drop("total", axis=1) # Keep for annotation and confints in re-analysis.
    prepared.reset_index(inplace=True)

    # Check and return
    #print(prepared)
    print("prepared", prepared.shape)
    return prepared


def plot_data(data, filename): 
    fig,ax = plt.subplots(figsize=(16,10))
    plt.bar(data["decade"], data["titled"], width=0.5, label="titled insets", color="black")
    plt.bar(data["decade"], data["untitled"], width=0.5, label="untitled insets", color="grey", bottom=data["titled"])
    plt.title('Replication of Figure 3.3: Titled insets in Type 1 novels', fontsize=16)
    plt.ylabel('Production of Type 1 inset novels', fontsize=14)
    plt.xticks(rotation=0, fontsize=14)
    plt.legend(loc="lower center", ncol=2, fontsize=14)
    plt.savefig(filename, dpi=300)
    print("Figure saved.")



def main(datafile):
    data = read_data(datafile)
    filename = join(wdir, "fig_3-3_replication.svg")
    filtered = filter_data(data)
    prepared = prepare_data(filtered)
    plot_data(prepared, filename)

main(datafile)

