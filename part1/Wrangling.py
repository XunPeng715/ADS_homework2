import numpy as np
import pandas as pd

train_df = pd.read_csv("train_2016_v2.csv", parse_dates=["transactiondate"])
prop_df = pd.read_csv("data.csv")

train_df = pd.merge(train_df, prop_df, on='parcelid', how='left')

missing_df = train_df.isnull().sum().reset_index()
missing_df.columns = ['col', 'missing_cnt']
missing_df = missing_df[(missing_df['missing_cnt'] > 0) & (missing_df['missing_cnt'] < train_df.shape[0] * 0.93)]

numeric_cols = ['calculatedfinishedsquarefeet', 'longitude', 'latitude', 'taxamount']
enum_cols = list(set(missing_df['col'].tolist()) - set(numeric_cols))

for col in enum_cols:
    train_df[col].fillna(train_df[col].value_counts().reset_index().iloc[0, 0], inplace=True)

mean_values = train_df[numeric_cols].mean(axis=0)
train_df[numeric_cols] = train_df[numeric_cols].fillna(mean_values, inplace=True)

train_df.to_csv('cleanData.csv')
