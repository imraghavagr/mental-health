import click
import pandas as pd
from sklearn import preprocessing
from sklearn.utils import resample

#creating object of LabelEncoder
le = preprocessing.LabelEncoder()


@click.command()
@click.argument('path', type=click.Path())
@click.argument('target_path', type=click.Path())
def preprocess(path, target_path):
    """Preprocess the locally downloaded file and store it in a new directory."""
    path = path+"completeData.csv"
    target_path = target_path+"processed_data.csv"
    df = pd.read_csv(path)
    print(f"Reading data from {path} - Successful")
    #filling null values
    for x in df.columns:
        if df[x].isnull().sum()>0:
            df[x].fillna(df[x].mode()[0],inplace=True)
    print("Dealing with null values - Successful")
    
    #changing number of target classes from 5 to 4
    df['mental_disorder'].replace(to_replace="anxiety",value="stress",inplace=True)
    print("Changing number of target classes from 5 to 4 - Successful")

    #resampling data in order to fix target imbalance
    target0=df[df['mental_disorder']=="depression"]
    target1=df[df['mental_disorder']=="None"]
    target2=df[df['mental_disorder']=="stress"]
    target3 = df[df['mental_disorder']=="Panic attack"]
    target1=resample(target1,replace=True,n_samples=len(target0),random_state=40)
    target2 = resample(target2,replace=True,n_samples=len(target0),random_state=40)
    target3 = resample(target3,replace=True,n_samples=75,random_state=40)
    target=pd.concat([target0,target1,target2,target3])
    print("Fixing imbalance - Successful")

    
    # #label encoding
    # for x in df.columns:
    #     df[x] = le.fit_transform(df[x])
    
    target.to_csv(target_path, index=False, )
    print(f'Preprocessed the raw data from {path} and saved it to {target_path}')
    

if __name__ == '__main__':
    preprocess()