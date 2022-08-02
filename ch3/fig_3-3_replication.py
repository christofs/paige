
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint as scf
import os
import sys
from os.path import join

wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(wdir, "Data-France-web-post_CS_fig3-3_mod1.csv")


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep="\t")
        data.fillna(0, inplace=True)
        #print(data.head())
        return data


def group_data(data):
    grouped = data.groupby(by="decade").sum()
    grouped.drop("year", axis=1, inplace=True)
    grouped["titled insets"] = grouped["titled"] / grouped["total"] * 100
    grouped["untitled insets"] = 100 - grouped["titled insets"]
    grouped = grouped.drop("titled", axis=1)
    grouped = grouped.drop("untitled", axis=1)
    grouped = grouped.drop("total", axis=1)
    print(grouped)
    return grouped


def plot_data(data, filename): 
    fig,ax = plt.subplots(figsize=(16,10))
    data.plot(kind='bar', stacked=True, color=["black", "grey"])
    plt.title('Figure 3.3: Titled insets in Type 1 novels (replication)')
    plt.ylabel('Production of Type 1 inset novels')
    plt.xticks(rotation=0)
    plt.legend(loc="lower center", ncol=2)
    plt.savefig(filename, dpi=300)



def main(datafile):
    data = read_data(datafile)
    filename = join(wdir, "fig_3-3_replication.svg")
    grouped = group_data(data)
    plot_data(grouped, filename)

main(datafile)

