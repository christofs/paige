from cmath import nan
import os
import sys
from os.path import join
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint as scf
import pygal


wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(wdir, "Data-France-web-post_CS-fig4-4.csv")

def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",", index_col=None)
        data.fillna(0, inplace=True)
        data.drop(["paige", "half-century", "score", "year", "generic subtitle"], axis=1, inplace=True)
        # Filter out novels with more than 150k words
        indexNames = data[data["words"] > 150].index
        data.drop(indexNames , inplace=True)
        print(data.head())
        return data


def prepare_data1(data):
    prepared = []
    grouped = data.groupby(by=["decade", "simple"])
    for name,group in grouped: 
        if name[0] in ["1600s", "1610s", "1620s"]:
            if name[1] in ["unsubtitled", "histoire", "nouvelle"]:
                decade = name[0]
                subtitle = name[1]
                kwords = list(group["words"])
                entry = {"subtitle" : subtitle, "decade" : decade, "kwords" : kwords} 
                prepared.append(entry)
    #print(prepared)
    print("prepared", type(prepared))
    return prepared


def make_pgplot(prepared, filename): 
    from pygal.style import Style
    custom_style = Style(colors=('#404040', '#9BC850', '#E81190', '#404040', '#9BC850', '#E81190', '#404040', '#9BC850', '#E81190', '#404040', '#9BC850', '#E81190'))
    plot = pygal.Box(style=custom_style)
    for entry in prepared: 
        plot.add(entry["subtitle"], entry["kwords"])
    plot.render_to_file(filename)




def make_snsplot(data, filename):
    fig,ax = plt.subplots(figsize=(10, 6))
    ax = sns.boxplot(data=data, x="decade", y="words", hue="simple", showfliers=False)
    #ax = sns.stripplot(data=data, color=".26")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)







def main(datafile):
    data = read_data(datafile)
    #filename = join(wdir, "fig4-4_boxplot-decades.svg")
    #prepared = prepare_data1(data)
    #make_pgplot(prepared, filename)
    filename = join(wdir, "fig4-4_violinplot-decades.svg")
    make_snsplot(data, filename)
    

main(datafile)

