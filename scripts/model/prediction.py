import click
import pandas as pd
from pycaret.classification import *

@click.command()
@click.argument('data_path', type=click.Path())
@click.argument('model_path', type=click.Path())
def train_model(data_path,model_path):
    """ Loading saved model and making prediction on new data"""
    model_path = model_path + 'finalRFmodel_21APR2022'
    data_path = data_path + 'processed_data.csv'


    df = pd.read_csv(data_path)

    # s = setup(df, target = 'mental_disorder')
    # print("Setting up pycaret env - Successful")

    # rf = create_model("rf")
    # print("Creating Random Forest model - Successful")
    record_num = 408
    loaded_model = load_model(model_path)
    prediction = predict_model(loaded_model,data = df.iloc[[record_num]])
    print(f"Actual class is {list(df.iloc[[record_num]]['mental_disorder'])[0]}")
    print(f"Predicted class is {list(prediction.Label)[0]} with {list(prediction.Score)[0]*100}% confidence")
    
if __name__ == "__main__":
    train_model()
