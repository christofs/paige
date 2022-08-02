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
    #print(data.head())
    #print(data.shape)
    return data


def select_data(data):
    # Select only the required columns
    #print(data.columns)
    sel = data[["decade", "subtitle2", "mode", "nouvelle", "count"]]
    # Filter out novels based to keep only real-world novels
    sel = sel.drop(sel[sel["mode"] != "rw"].index)
    # Filter out novels based on their decade of publication
    sel.drop(sel[sel["decade"] == "1600s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1610s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1620s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1630s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1750s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1760s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1770s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1780s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1790s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1800s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1810s"].index, inplace=True)
    sel.drop(sel[sel["decade"] == "1820s"].index, inplace=True)
    # Check and return
    #print(sel.head())
    #print(sel.shape)
    return sel

def prepare_data(sel):
    # Create the contrast between any kind of real-world novel and the separate kinds of nouvelles
    sel["47"] = sel["mode"]
    sel = sel[["decade", "47", "subtitle2", "nouvelle", "count"]]
    sel.loc[sel["nouvelle"] == 0, "47"] = "other"
    sel.loc[sel["subtitle2"] == "nouvelle_other", "47"] = "other"
    sel.loc[sel["subtitle2"] == "other", "47"] = "other"
    sel.loc[sel["subtitle2"] == "nouvelle_plain", "47"] = "nouvelle_plain"
    sel.loc[sel["subtitle2"] == "nouvelle_historique", "47"] = "nouvelle_historique"
    sel.loc[sel["subtitle2"] == "nouvelle_galante", "47"] = "nouvelle_galante"
    # Reshape the data
    prep = sel[["decade", "47", "count"]]
    prep = prep.pivot_table(index="decade", columns="47", values="count", aggfunc='sum', fill_value=0)
    # Turn counts into percentages
    print(prep)
    prep = (prep[prep.columns].div(np.sum(prep, axis=1), axis=0).multiply(100))   
    prep = prep.drop("other", axis=1)
    # Check and return
    print(prep.head(12))
    print(prep.shape)
    ##print(set(list(prep["subtitle1"])))
    return prep



def make_snsplot(prepared, filename):
    fig,ax = plt.subplots(figsize=(12, 6))
    ax = sns.lineplot(data=prepared, palette="dark:grey", legend = False)
    ax.set(ylabel="Production of real-world novels")
    plt.text(0.10, 20, "nouvelle (plain) ↘ ")
    plt.text(4.00, 23, "nouvelle galante ↘ ")
    plt.text(7.80, 7, "↙ nouvelle historique")
    plt.ylim(0,35)
    #plt.tight_layout()
    plt.savefig(filename, dpi=300)


def main(datafile):
    filename = join(wdir, "fig_4-7_lineplot-decades.svg")
    data = read_data(datafile)
    selected = select_data(data)
    prepared = prepare_data(selected)
    make_snsplot(prepared, filename)
    

main(datafile)

