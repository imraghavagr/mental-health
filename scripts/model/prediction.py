import click
import pandas as pd
from pycaret.classification import *

@click.command()
@click.argument('data_path', type=click.Path())
@click.argument('model_path', type=click.Path())
def train_model(data_path,model_path):
    """ Loading saved model and making prediction on new data"""
    model_path = model_path + 'finalRFmodel2_20APR2022'
    data_path = data_path + 'processed_data.csv'


    df = pd.read_csv(data_path)

    # s = setup(df, target = 'mental_disorder')
    # print("Setting up pycaret env - Successful")

    # rf = create_model("rf")
    # print("Creating Random Forest model - Successful")

    loaded_model = load_model(model_path)
    prediction = predict_model(loaded_model,data = df.iloc[[23]])
    print(f"Actual class is {df.iloc[[23]]['mental_disorder']}")
    print(f"Predicted class is {prediction.Label} with {prediction.Score} confidence")
    
if __name__ == "__main__":
    train_model()
