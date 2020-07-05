import sys, sqlite3
import pandas as pd

from sqlalchemy import create_engine
from functools import reduce

# Get command line arguments
messages_path = sys.argv[1]
categories_path = sys.argv[2]
db_path = sys.argv[3]

# Read in data
with open(messages_path, encoding='utf-8') as f:
    df_messages = pd.read_csv(f)

with open(categories_path, encoding='utf-8') as f:
    df_categories = pd.read_csv(f)

# Merge data
df_merged = pd.concat([df_messages, df_categories], axis=1)

# Transform features
drop_features = lambda df: df.drop(columns=['id', 'original'])

def get_categories(df):
    """
    Converts semicolon-separated categores with binary indicators into boolean categories.

    Takes a dataframe.
    Returns a dataframe with semicolon-separated values replaced with boolean categories.
    """
    column_names = list(map(lambda s: s[:-2], df['categories'].str.split(';')[0]))
    df_dummies = df['categories'].str.split(';', expand=True).apply(lambda x: x.str[-1] == '1')
    df_dummies.columns = column_names
    df_merged = pd.concat([df, df_dummies], axis=1).drop(columns='categories')
    return df_merged

drop_duplicates = lambda df: df.drop_duplicates()

fns = [drop_features, get_categories, drop_duplicates]
df_trans = reduce(lambda res, fn: fn(res), fns, df_merged)

# Save to an SQLite database
engine = create_engine(f'sqlite:///{db_path}')

with engine.connect() as connection:
    df_trans.to_sql('messages', connection, index=False, if_exists='replace')