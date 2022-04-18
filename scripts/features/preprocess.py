import pandas as pd
from sklearn import preprocessing

#creating object of LabelEncoder
le = preprocessing.LabelEncoder()

#reading the dataset
df = pd.read_csv('/home/raghav/codes_new/mental-health/data/raw/Mental Health Checker.csv')

#removing 'Timstamp' column
df.drop(['Timestamp'],axis = 1,inplace=True)

#filling null values
for x in df.columns:
    if df[x].isnull().sum()>0:
        df[x].fillna(df[x].mode()[0],inplace=True)

#label encoding
for x in df.columns:
    df[x] = le.fit_transform(df[x])





