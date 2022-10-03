
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

steps = ["decade", "score"]


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",")
    data.fillna(0, inplace=True)
    #print(data.head())
    return data


def filter_data(data, step): 
    filtered = data[[step, "inset", "halfcentury", "titled insets?"]]
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


def prepare_data(data, step):
    binary = pd.get_dummies(data["titled"])
    prepared = pd.concat((binary, data), axis=1)
    prepared = prepared.drop(["titled"], axis=1)
    prepared = prepared.rename(columns={"y": "titled", "n" : "untitled"})
    prepared = prepared.groupby(by=step).sum()
    prepared["total"] = prepared["titled"] + prepared["untitled"]        
    prepared["proportion"] = prepared["titled"] / prepared["total"]*100
    prepared.reset_index(inplace=True)

    # Average
    total_titled = np.sum(prepared["titled"])
    total_untitled = np.sum(prepared["untitled"])
    total_all = total_titled + total_untitled
    print(total_titled, total_untitled, total_all)
    avg_prop_titled =  total_titled / total_all
    print("Average across all data:", avg_prop_titled)

    # Check and return
    #print(prepared)
    print("prepared", prepared.shape)
    return prepared, avg_prop_titled


def check_correlation(prepared, step): 
    rho = np.corrcoef(prepared["proportion"], prepared["total"])
    print("Pearson's R for the relation between proportion and total number of inset novels for", step, "is:", rho)


def get_confints(grouped): 
    # https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.proportion_confint.html
    rows = []
    for name,row in grouped.iterrows(): 
        confint = scf(row["titled"], row["total"], alpha=0.05, method="wilson") 
        row["confint_min"] = confint[0]*100
        row["confint_max"] = confint[1]*100
        row["confint_size"] = (confint[1] - confint[0])*100
        row["confint_lower"] = row["proportion"] - row["confint_min"] 
        row["confint_upper"] = row["confint_max"] - row["proportion"] 
        rows.append(row)
    confints = pd.DataFrame(rows)
    #print(confints)
    return confints


def plot_data(data, step, avg_prop_titled, filename): 
    labels = data[step]
    errors = [data["confint_lower"], data["confint_upper"]]
    ns = data["total"]
    avgs = [(avg_prop_titled*100)] * len(labels)
    fig,ax = plt.subplots(figsize=(16, 10))
    x = np.arange(len(labels))
    y = data["proportion"]
    eb = plt.errorbar(x, y, 
        yerr=errors, 
        xerr=None, 
        fmt="s", 
        mfc="black", 
        mew=0, 
        markersize=16, 
        ecolor="SlateGrey", 
        elinewidth=8,
        label="proportion with confidence interval")
    eb[-1][0].set_linestyle((1,(3,0.5)))
    plt.ylim(0,110)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Re-analysis of Figure 3.3: Titled insets in Type 1 novels", fontsize=16)
    ax.set_ylabel("Proportion of titled insets", fontsize=14)
    ax.set_xlabel("Time interval: "+step, fontsize=14)
    for i in range(len(labels)):
        ax.text(x[i]+0.15, y[i]-0.02, "n="+str(int(ns[i])), size=12)
    ax.plot(x, avgs, label="average proportion across all data", color="grey", linewidth=3, dashes=(1,1))
    ax.yaxis.grid(True)
    plt.legend(loc="lower center")
    #plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print("Figure saved.")



def main(datafile, steps, wdir):
    data = read_data(datafile)
    for step in steps: 
        filename = join(wdir, "fig_3-3_errorplot-"+step+".svg")
        filtered = filter_data(data, step)
        prepared, avg_prop_titled = prepare_data(filtered, step)
        confints = get_confints(prepared)
        check_correlation(prepared, step)
        plot_data(confints, step, avg_prop_titled, filename)

main(datafile, steps, wdir)

