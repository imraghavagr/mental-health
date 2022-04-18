import click
import pandas as pd
from sklearn import preprocessing

#creating object of LabelEncoder
le = preprocessing.LabelEncoder()


@click.command()
@click.argument('path', type=click.Path())
@click.argument('target_path', type=click.Path())
def preprocess(path, target_path):
    """Preprocess the locally downloaded file and store it in a new directory."""
    path = path+"Mental Health Checker.csv"
    target_path = target_path+"processed_data.csv"
    df = pd.read_csv(path)
    #removing 'Timestamp' column
    df.drop(['Timestamp'],axis = 1,inplace=True)

    #filling null values
    for x in df.columns:
        if df[x].isnull().sum()>0:
            df[x].fillna(df[x].mode()[0],inplace=True)
    
    #label encoding
    # for x in df.columns:
    #     df[x] = le.fit_transform(df[x])
    
    df.to_csv(target_path, index=False, )
    print(f'Preprocessed the raw data from {path} and saved it to {target_path}')
    

if __name__ == '__main__':
    preprocess()