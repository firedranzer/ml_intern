import pandas as pd
import re


def load_data():
    #Importing CSV file
    df = pd.read_csv("./data/olympics.csv", header=1)
    
    #Substituting numbers with corresponding medals
    df = df.rename(columns=lambda x : re.sub('^01 !', 'Gold', x))
    df = df.rename(columns=lambda x : re.sub('^02 !', 'Siver', x))
    df = df.rename(columns=lambda x : re.sub('^03 !', 'Bronze', x))
    
    #Make seperate list of country names and codes.
    country_name, country_code = []
    for i in df['Unnamed: 0']:
        country_name.append(i[0:i.find('(')].replace(u'\xa0', u''))
        country_code.append(i[i.find('(')+1: i.find(')')])

    #Inserting updated rows
    del df['Unnamed: 0']
    df.insert(0, 'country_name', country_name)
    df.insert(1, 'country_code', country_code)
    df = df.set_index('country_name')

    #drop Totals column
    df.drop(df.tail(1).index, inplace=True)
    return df
    
def first_country(df):
    return df.iloc[0]


def gold_medal(df):
    return df.loc[df['Gold'].argmax()].name


def biggest_difference_in_gold_medal(df):
    return df.loc[(df['Gold']-df['Gold.1']).abs().idxmax()].name

def get_points(df):
    Points = []
    for index, row in df.iterrows():
        Points.append(row['Gold.2']*3 + row['Silver.2']*2 + row['Bronze']*1)
    