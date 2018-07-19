import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import os


#get to the root directory of a project
DIR_PATH = os.path.join( os.path.dirname( __file__ ), '..' )
DATA_FILE = os.path.join(DIR_PATH, "data/data/csv_pus/ss16pny.csv")

# RAC1P - race code
# PINCP - total income (past 12 months)


def load_data():
    d = pd.read_csv(DATA_FILE, usecols=['RAC1P', 'PINCP'])
    # magic
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



def get_race(i):
    i = str(int(i))
    if i in race_dict:
        return race_dict[i]
    else:
        print(i)
        pass


def plot_income_by_race():
    df = load_data()
    raceg_data = df.groupby(['RAC1P']).agg(agg)
    # # choose the columns for 1,2,3,6
    for i in [1,2,3]:
        raceg_data = raceg_data.drop(raceg_data.index[-1])
    raceg_data = raceg_data.drop(raceg_data.index[[3,4]])

    print(raceg_data)
    raceg_data.plot(kind='bar')
    plt.legend()

    plt.suptitle("Income by race in 2016 in US Dollars in the state of New York", verticalalignment='center')
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d $'))
    plt.xlabel("Race")
    plt.ylabel("Income in USD")

    plt.show()
    # return raceg_data.groupby('RAC1P').count()

plot_income_by_race()



# PLOTTING THE DATA

