import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import matplotlib.patches as mpatches
import os


#get to the root directory of a project
DIR_PATH = os.path.join( os.path.dirname( __file__ ), '..' )
DATA_FILE = os.path.join(DIR_PATH, "data/data/csv_pus/ss16pny.csv")


# RAC1P - race code PINCP - total income (past 12 months)
def load_data():
    d = pd.read_csv(DATA_FILE, usecols=['RAC1P', 'PINCP'])
    return d


agg = {
    "PINCP": {
        'income_25': lambda x: x.quantile(0.25),
        'income_50': lambda x: x.quantile(0.5),
        'income_75': lambda x: x.quantile(0.75),
        'income_mean': 'mean',
    }
}

race_dict = {
    '1': 'White',
    '2': 'Black or African American',
    '3': 'American Indian',
    '6': 'Asian'
}

def create_boxplot():
    x = load_data()

    # Get rid of NaNs in data
    w = x[x['RAC1P'] == 1]['PINCP'].dropna()
    af = x[x['RAC1P'] == 2]['PINCP'].dropna()
    nat = x[x['RAC1P'] == 3]['PINCP'].dropna()
    asi = x[x['RAC1P'] == 6]['PINCP'].dropna()

    # Cut out first and last quantile
    list_races = []
    for el in [w, af, nat, asi]:
        q25 = el[el > w.quantile(0.25)]
        q75 = q25[q25 < w.quantile(0.75)]
        list_races.append(q75)

    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)

    # Create the boxplot
    bp = ax.boxplot(list_races)

    #create legend
    red_patch = mpatches.Patch(color='red', label='1 - Whites')
    blue_patch = mpatches.Patch(color='blue', label='2 - African Americans')
    green_patch = mpatches.Patch(color='green', label='3 - Native Americans')
    yellow_patch = mpatches.Patch(color='yellow', label='4 - Asians')

    plt.legend(handles=[red_patch, blue_patch, green_patch, yellow_patch], bbox_to_anchor=(1, 1), loc=1, borderaxespad=0)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.suptitle("Income by race in 2016 in US Dollars in New York state", verticalalignment='center')
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d $'))
    plt.xlabel("Race declared in US Census")
    plt.ylabel("Income in USD")
    plt.show()


create_boxplot()
