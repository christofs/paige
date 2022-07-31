from cmath import nan
import os
import sys
from os.path import join
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(wdir, "Data-France-web-post_CS-fig4-4.csv")


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",", index_col=None)
        data.fillna(0, inplace=True)
        #print(data.head())
        return data


def prepare_data(data):
    # Remove unnecessary data
    #data.drop(["paige", "score", "decade", "year", "generic subtitle"], axis=1, inplace=True)
    # Filter out novels with more than 150k words
    data.drop(data[data["words"] > 150].index, inplace=True)
    # Filter out novels based on their genre subtitle
    data.drop(data[data["subtitles"] == "other"].index, inplace=True)
    data.drop(data[data["subtitles"] == "conte"].index, inplace=True)
    data.drop(data[data["subtitles"] == "roman"].index, inplace=True)
    data.drop(data[data["subtitles"] == "memoires"].index, inplace=True)
    data.drop(data[data["subtitles"] == "anecdote"].index, inplace=True)
    data.drop(data[data["subtitles"] == "chronique"].index, inplace=True)
    # Filter out novels based on their score of publication
    data.drop(data[data["score"] == "1741-1760"].index, inplace=True)
    data.drop(data[data["score"] == "1761-1780"].index, inplace=True)
    data.drop(data[data["score"] == "1781-1800"].index, inplace=True)
    data.drop(data[data["score"] == "1801-1820"].index, inplace=True)
    data.drop(data[data["score"] == "1821-1840"].index, inplace=True)
    # Filter out novels based on their decade of publication
    #data.drop(data[data["decade"] == "1730s"].index, inplace=True)
    #data.drop(data[data["decade"] == "1740s"].index, inplace=True)
    #data.drop(data[data["decade"] == "1750s"].index, inplace=True)
    #data.drop(data[data["decade"] == "1760s"].index, inplace=True)
    #data.drop(data[data["decade"] == "1770s"].index, inplace=True)
    #data.drop(data[data["decade"] == "1780s"].index, inplace=True)
    #data.drop(data[data["decade"] == "1790s"].index, inplace=True)
    #data.drop(data[data["decade"] == "1800s"].index, inplace=True)
    #data.drop(data[data["decade"] == "1810s"].index, inplace=True)
    #data.drop(data[data["decade"] == "1820s"].index, inplace=True)
    print(data.head())
    return data


def make_snsplot(prepared, filename):
    target = "score"
    fig,ax = plt.subplots(figsize=(10, 6))
    ax = sns.boxplot(data=prepared, x=target, y="words", hue="subtitles", palette="light:grey", showfliers=False)
    ax = sns.stripplot(data=prepared, x=target, y="words", hue="subtitles", jitter=0.15, size=2.5, palette="dark:black", dodge=True)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)


def main(datafile):
    filename = join(wdir, "fig4-4_violinplot-scores.svg")
    data = read_data(datafile)
    prepared = prepare_data(data)
    make_snsplot(prepared, filename)
    

main(datafile)

