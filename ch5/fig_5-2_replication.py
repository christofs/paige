import pandas as pd
import numpy as np
import os
import sys
from os.path import join
import pygal

wdir = os.path.dirname(os.path.realpath(sys.argv[0]))
datafile = join(os.path.dirname(wdir), "Data-France-web-post-CS.csv")


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile:
        data = pd.read_csv(infile, sep=",")
    data.fillna(0, inplace=True)
    # Check and return
    #print(data.head())
    #print(data.shape)
    #print(data.columns)
    return data


def filter_data(data): 
    filtered = data[["decade", "mode", "words", "inset", "count", "temporality1", "temporality2", "truth-rw", "characters-rw"]]
    filtered = filtered[filtered["mode"] == "rw"] 
    del_decades = ["1750s", "1760s", "1770s", "1780s", "1790s", "1800s", "1810s", "1820s"]
    for item in del_decades: 
        filtered.drop(filtered[filtered["decade"] == item].index, inplace=True)
    # Check and return
    #print(filtered.head())
    #print(filtered.shape)
    return filtered


def prepare_data(data):
    totals = data.groupby(by="decade").sum().drop("words", axis=1)
    #print(totals)

    # Define relevant decades
    decades = ["1600s","1610s","1620s","1630s","1640s","1650s","1660s","1670s","1680s","1690s","1700s","1710s","1720s","1730s","1740s"]

    # Establish the data for "roman", length group 1
    roman1A = data[(data["words"] > 79) & (data["inset"] == "i1") & (data["truth-rw"] == "keyed")] 
    roman1B = data[(data["words"] > 79) & (data["inset"] == "i1") & (data["characters-rw"] == "combo")] 
    roman1C = data[(data["words"] > 79) & (data["inset"] == "i1") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "biblical")] 
    roman1D = data[(data["words"] > 79) & (data["inset"] == "i1") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "myth")] 
    roman1E = data[(data["words"] > 79) & (data["inset"] == "i1") & (data["temporality1"] == "his") & (data["characters-rw"] == "nobodies")] 
    roman1F = data[(data["words"] > 79) & (data["inset"] == "i1") & (data["temporality1"] == "con") & (data["truth-rw"] == "fict")] 
    roman1G = data[(data["words"] > 79) & (data["inset"] == "i1") & (data["temporality1"] == "con") & (data["truth-rw"] == "ind")] 
    roman1H = data[(data["words"] > 79) & (data["inset"] == "i1") & (data["temporality1"] == "uns") & (data["truth-rw"] == "fict")] 
    roman1I = data[(data["words"] > 79) & (data["inset"] == "i1") & (data["temporality1"] == "uns") & (data["truth-rw"] == "ind")] 

    roman1J = data[(data["words"] > 79) & (data["inset"] == "i2") & (data["truth-rw"] == "keyed")] 
    roman1K = data[(data["words"] > 79) & (data["inset"] == "i2") & (data["characters-rw"] == "combo")] 
    roman1L = data[(data["words"] > 79) & (data["inset"] == "i2") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "biblical")] 
    roman1M = data[(data["words"] > 79) & (data["inset"] == "i2") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "myth")] 
    roman1N = data[(data["words"] > 79) & (data["inset"] == "i2") & (data["temporality1"] == "his") & (data["characters-rw"] == "nobodies")] 
    roman1O = data[(data["words"] > 79) & (data["inset"] == "i2") & (data["temporality1"] == "con") & (data["truth-rw"] == "fict")] 
    roman1P = data[(data["words"] > 79) & (data["inset"] == "i2") & (data["temporality1"] == "con") & (data["truth-rw"] == "ind")] 
    roman1Q = data[(data["words"] > 79) & (data["inset"] == "i2") & (data["temporality1"] == "uns") & (data["truth-rw"] == "fict")] 
    roman1R = data[(data["words"] > 79) & (data["inset"] == "i2") & (data["temporality1"] == "uns") & (data["truth-rw"] == "ind")] 

    # Establish the data for "roman", length group 2
    roman2A = data[(data["words"] > 118) & (data["inset"] == "i1") & (data["truth-rw"] == "keyed")] 
    roman2B = data[(data["words"] > 118) & (data["inset"] == "i1") & (data["characters-rw"] == "combo")] 
    roman2C = data[(data["words"] > 118) & (data["inset"] == "i1") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "biblical")] 
    roman2D = data[(data["words"] > 118) & (data["inset"] == "i1") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "myth")] 
    roman2E = data[(data["words"] > 118) & (data["inset"] == "i1") & (data["temporality1"] == "his") & (data["characters-rw"] == "nobodies")] 
    roman2F = data[(data["words"] > 118) & (data["inset"] == "i1") & (data["temporality1"] == "con") & (data["truth-rw"] == "fict")] 
    roman2G = data[(data["words"] > 118) & (data["inset"] == "i1") & (data["temporality1"] == "con") & (data["truth-rw"] == "ind")] 
    roman2H = data[(data["words"] > 118) & (data["inset"] == "i1") & (data["temporality1"] == "uns") & (data["truth-rw"] == "fict")] 
    roman2I = data[(data["words"] > 118) & (data["inset"] == "i1") & (data["temporality1"] == "uns") & (data["truth-rw"] == "ind")] 

    roman2J = data[(data["words"] > 118) & (data["inset"] == "i2") & (data["truth-rw"] == "keyed")] 
    roman2K = data[(data["words"] > 118) & (data["inset"] == "i2") & (data["characters-rw"] == "combo")] 
    roman2L = data[(data["words"] > 118) & (data["inset"] == "i2") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "biblical")] 
    roman2M = data[(data["words"] > 118) & (data["inset"] == "i2") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "myth")] 
    roman2N = data[(data["words"] > 118) & (data["inset"] == "i2") & (data["temporality1"] == "his") & (data["characters-rw"] == "nobodies")] 
    roman2O = data[(data["words"] > 118) & (data["inset"] == "i2") & (data["temporality1"] == "con") & (data["truth-rw"] == "fict")] 
    roman2P = data[(data["words"] > 118) & (data["inset"] == "i2") & (data["temporality1"] == "con") & (data["truth-rw"] == "ind")] 
    roman2Q = data[(data["words"] > 118) & (data["inset"] == "i2") & (data["temporality1"] == "uns") & (data["truth-rw"] == "fict")] 
    roman2R = data[(data["words"] > 118) & (data["inset"] == "i2") & (data["temporality1"] == "uns") & (data["truth-rw"] == "ind")] 


    # Establish the data for "roman", length group 3
    roman3A = data[(data["words"] > 173) & (data["inset"] == "i1") & (data["truth-rw"] == "keyed")] 
    roman3B = data[(data["words"] > 173) & (data["inset"] == "i1") & (data["characters-rw"] == "combo")] 
    roman3C = data[(data["words"] > 173) & (data["inset"] == "i1") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "biblical")] 
    roman3D = data[(data["words"] > 173) & (data["inset"] == "i1") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "myth")] 
    roman3E = data[(data["words"] > 173) & (data["inset"] == "i1") & (data["temporality1"] == "his") & (data["characters-rw"] == "nobodies")] 
    roman3F = data[(data["words"] > 173) & (data["inset"] == "i1") & (data["temporality1"] == "con") & (data["truth-rw"] == "fict")] 
    roman3G = data[(data["words"] > 173) & (data["inset"] == "i1") & (data["temporality1"] == "con") & (data["truth-rw"] == "ind")] 
    roman3H = data[(data["words"] > 173) & (data["inset"] == "i1") & (data["temporality1"] == "uns") & (data["truth-rw"] == "fict")] 
    roman3I = data[(data["words"] > 173) & (data["inset"] == "i1") & (data["temporality1"] == "uns") & (data["truth-rw"] == "ind")] 

    roman3J = data[(data["words"] > 173) & (data["inset"] == "i2") & (data["truth-rw"] == "keyed")] 
    roman3K = data[(data["words"] > 173) & (data["inset"] == "i2") & (data["characters-rw"] == "combo")] 
    roman3L = data[(data["words"] > 173) & (data["inset"] == "i2") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "biblical")] 
    roman3M = data[(data["words"] > 173) & (data["inset"] == "i2") & (data["characters-rw"] == "somebodies") & (data["temporality2"] == "myth")] 
    roman3N = data[(data["words"] > 173) & (data["inset"] == "i2") & (data["temporality1"] == "his") & (data["characters-rw"] == "nobodies")] 
    roman3O = data[(data["words"] > 173) & (data["inset"] == "i2") & (data["temporality1"] == "con") & (data["truth-rw"] == "fict")] 
    roman3P = data[(data["words"] > 173) & (data["inset"] == "i2") & (data["temporality1"] == "con") & (data["truth-rw"] == "ind")] 
    roman3Q = data[(data["words"] > 173) & (data["inset"] == "i2") & (data["temporality1"] == "uns") & (data["truth-rw"] == "fict")] 
    roman3R = data[(data["words"] > 173) & (data["inset"] == "i2") & (data["temporality1"] == "uns") & (data["truth-rw"] == "ind")] 


    # roman1: Combine all subtypes that belong to a definition of "roman": roman1
    roman1 = pd.concat([roman1A, roman1B, roman1C, roman1D, roman1E, roman1F, roman1G, roman1H, roman1I])
    roman1 = roman1.drop(["mode", "words", "inset", "temporality1", "temporality2", "truth-rw", "characters-rw" ], axis=1)
    roman1 = roman1.groupby(by="decade").sum().T
    roman1 = roman1.reindex(columns=decades, fill_value=0).T
    roman1 = np.divide(roman1, totals)*100

    # roman2: Combine all subtypes that belong to a definition of "roman": roman2
    roman2 = pd.concat([roman2A, roman2B, roman2C, roman2D, roman2E, roman2F, roman2G, roman2H, roman2I])
    roman2 = roman2.drop(["mode", "words", "inset", "temporality1", "temporality2", "truth-rw", "characters-rw" ], axis=1)
    roman2 = roman2.groupby(by="decade").sum().T
    roman2 = roman2.reindex(columns=decades, fill_value=0).T
    roman2 = np.divide(roman2, totals)*100

    # roman3: Combine all subtypes that belong to a definition of "roman": roman2
    roman3 = pd.concat([roman3A, roman3B, roman3C, roman3D, roman3E, roman3F, roman3G, roman3H, roman3I])
    roman3 = roman3.drop(["mode", "words", "inset", "temporality1", "temporality2", "truth-rw", "characters-rw" ], axis=1)
    roman3 = roman3.groupby(by="decade").sum().T
    roman3 = roman3.reindex(columns=decades, fill_value=0).T
    roman3 = np.divide(roman3, totals)*100

    # roman4: Combine all subtypes that belong to a definition of "roman": roman2
    roman4 = pd.concat([roman1A, roman1B, roman1C, roman1D, roman1E, roman1F, roman1G, roman1H, roman1I, roman1J, roman1K, roman1L, roman1M, roman1N, roman1O, roman1P, roman1Q, roman1R])
    roman4 = roman4.drop(["mode", "words", "inset", "temporality1", "temporality2", "truth-rw", "characters-rw" ], axis=1)
    roman4 = roman4.groupby(by="decade").sum().T
    roman4 = roman4.reindex(columns=decades, fill_value=0).T
    roman4 = np.divide(roman4, totals)*100

    # roman5: Combine all subtypes that belong to a definition of "roman": roman2
    roman5 = pd.concat([roman2A, roman2B, roman2C, roman2D, roman2E, roman2F, roman2G, roman2H, roman2I, roman2J, roman2K, roman2L, roman2M, roman2N, roman2O, roman2P, roman2Q, roman2R])
    roman5 = roman5.drop(["mode", "words", "inset", "temporality1", "temporality2", "truth-rw", "characters-rw" ], axis=1)
    roman5 = roman5.groupby(by="decade").sum().T
    roman5 = roman5.reindex(columns=decades, fill_value=0).T
    roman5 = np.divide(roman5, totals)*100

    # roman6: Combine all subtypes that belong to a definition of "roman": roman2
    roman6 = pd.concat([roman3A, roman3B, roman3C, roman3D, roman3E, roman3F, roman3G, roman3H, roman3I, roman3J, roman3K, roman3L, roman3M, roman3N, roman3O, roman3P, roman3Q, roman3R])
    roman6 = roman6.drop(["mode", "words", "inset", "temporality1", "temporality2", "truth-rw", "characters-rw" ], axis=1)
    roman6 = roman6.groupby(by="decade").sum().T
    roman6 = roman6.reindex(columns=decades, fill_value=0).T
    roman6 = np.divide(roman6, totals)*100



    # Establish the data for "nouvelle" group 1
    nouvelle1A = data[(data["words"] < 57) & (data["inset"] == "0") & (data["truth-rw"] == "keyed")] 


    # Check and return
    #print(roman1.head(10))
    data = [roman1, roman2, roman3, roman4, roman5, roman6]
    return data

def plot_data(data, filename): 
    from pygal.style import BlueStyle
    plot = pygal.Line(range=(0,100), style=BlueStyle, legend_at_bottom=True)
    plot.add("roman1 (>79km, i1)", data[0]["count"])
    plot.add("roman2 (>118k, i1)", data[1]["count"])
    plot.add("roman3 (>173k, i1)", data[2]["count"])
    plot.add("roman4 (>79km, i1|i2)", data[3]["count"])
    plot.add("roman5 (>118k, i1|i2)", data[4]["count"])
    plot.add("roman6 (>173k, i1|i2)", data[5]["count"])
    plot.render_to_file(filename)
    print("Figure saved.")



def main(datafile):
    data = read_data(datafile)
    filename = join(wdir, "dataset-years+mode.svg")
    filtered = filter_data(data)
    prepared = prepare_data(filtered)
    plot_data(prepared, filename)

main(datafile)

