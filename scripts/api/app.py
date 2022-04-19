
import pandas as pd
import click
from pycaret.classification import load_model, predict_model
from fastapi import FastAPI
import uvicorn

# Create the app
app = FastAPI()


# Load trained Pipeline
model = load_model('./artifacts/LGBM/lgbm_model')


@app.get('/')
async def root():
    '''
    This is the index page!
    '''
    return {'Instructions': 'Type [/docs] after the localhost address for viewing the Swagger UI'}


@app.get('/healthcheck', status_code=200)
async def healthcheck():
    return 'Mental Health Predictor is all ready to go!'



# Define predict function
@app.post('/predict')
def predict(gender, age, education, marital, income, loan, friend_no, friend_help, friend_interact, share_feel, have_someone, lonely, bullied, family_support, compare_life, social_media, hangout, home_time, religious, goal, suicidal, sleep_disorder, love_someone, die_someone, thoughts_command, self_harm, thoughts_acted, thoughts_acted2, thoughts_time, voices, harming_others, suicide, suicidal_thoughts, therapy):
    data = [gender, age, education, marital, income, loan, friend_no, friend_help, friend_interact, share_feel, have_someone, lonely, bullied, family_support, compare_life, social_media, hangout, home_time, religious, goal, suicidal, sleep_disorder, love_someone, die_someone, thoughts_command, self_harm, thoughts_acted, thoughts_acted2, thoughts_time, voices, harming_others, suicide, suicidal_thoughts, therapy]
    data = pd.DataFrame([data])
    data.columns = ['gender', 'age', 'education', 'marital', 'income', 'loan', 'friend_no', 'friend_help', 'friend_interact', 'share_feel', 'have_someone', 'lonely', 'bullied', 'family_support', 'compare_life', 'social_media', 'hangout', 'home_time', 'religious', 'goal', 'suicidal', 'sleep_disorder', 'love_someone', 'die_someone', 'thoughts_command', 'self_harm', 'thoughts_acted', 'thoughts_acted2', 'thoughts_time', 'voices', 'harming_others', 'suicide', 'suicidal_thoughts', 'therapy']
    
    
    predictions = predict_model(model, data=data) 
    return {'prediction': list(predictions['Label'])}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)