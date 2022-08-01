
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint as scf


datafile = "Data-France-web-post_CS_fig3-3_mod1.csv"
aggregations = ["decade", "scores", "halfcents"]


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep="\t")
        data.fillna(0, inplace=True)
        #print(data.head())
        return data


def group_data(data, agg):
    grouped = data.groupby(by=agg).sum()
    grouped.drop("year", axis=1, inplace=True)
    grouped["proportion"] = grouped["titled"] / grouped["total"]
    #print(grouped)
    return grouped


def get_confints(grouped): 
    # https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.proportion_confint.html
    rows = []
    for name,row in grouped.iterrows(): 
        confint = scf(row["titled"], row["total"], alpha=0.05, method="wilson") 
        row["confint_min"] = confint[0]
        row["confint_max"] = confint[1]
        row["confint_size"] = confint[1] - confint[0]
        row["confint_lower"] = row["proportion"] - row["confint_min"] 
        row["confint_upper"] = row["confint_max"] - row["proportion"] 
        rows.append(row)
    confints = pd.DataFrame(rows)
    #print(confints)
    return confints


def plot_data(data, filename): 
    labels = data.index
    errors = [data["confint_lower"], data["confint_upper"]]
    ns = data["total"]
    avgs = [np.mean(data["proportion"])] * len(labels)
    fig,ax = plt.subplots(figsize=(8, 6))
    x = np.arange(len(labels))
    y = data["proportion"]
    plt.errorbar(x, y, 
        yerr=errors, 
        xerr=None, 
        fmt="s", 
        mfc="DarkSlateBlue", 
        mew=0, 
        markersize=10, 
        ecolor="Teal", 
        elinewidth=4, 
        label="proportion with confidence interval")
    plt.ylim(0,1)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title('Proportion of titled insets over time')
    ax.set_ylabel('Proportion of titled insets')
    ax.set_xlabel('Time interval')
    for i in range(len(labels)):
        ax.text(x[i]+0.15, y[i]-0.02, "n="+str(int(ns[i])), size=8)
    ax.plot(x, avgs, label="average proportion across all data")
    ax.yaxis.grid(True)
    plt.legend(loc="lower center")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)



def main(datafile, aggregations):
    data = read_data(datafile)
    for agg in aggregations: 
        filename = "fig3-3_errorplot-"+agg+".png"
        grouped = group_data(data, agg)
        confints = get_confints(grouped)
        plot_data(confints, filename)

main(datafile, aggregations)

