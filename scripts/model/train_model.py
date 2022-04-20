import click
import pandas as pd
from pycaret.classification import *

@click.command()
@click.argument('data_path', type=click.Path())
@click.argument('target_path', type=click.Path())
def train_model(data_path,target_path):
    """ Read the final processed data, train the optimal model and save the pkl file."""
    target_path = target_path + 'finalRFmodel_21APR2022'
    data_path = data_path + 'processed_data.csv'


    df = pd.read_csv(data_path)
    print("Reading processed data - Successful")

    s = setup(df, target = 'mental_disorder')
    print("Setting up pycaret env - Successful")

    rf = create_model("rf")
    print("Creating Random Forest model - Successful")

    save_model(rf,target_path)
    print(f"Successfuly save model pickel file to {target_path}")



if __name__ == "__main__":
    train_model()
