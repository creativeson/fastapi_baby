from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):
    # marriage_couples: float
    # female_marriage_age: float
    # male_marriage_age: float
    marriage_couples: int
    female_marriage_age: int
    male_marriage_age: int


# loading the saved model
predict_model = pickle.load(open('predict_model.sav', 'rb'))

@app.post('/prediction')
def babies_pred(input_parameters: model_input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    marriage = input_dictionary['marriage_couples']
    f_age = input_dictionary['female_marriage_age']
    m_age = input_dictionary['male_marriage_age']

    input_list = [marriage, f_age, m_age]

    prediction = predict_model.predict([input_list])

    if prediction[0][0] > 0:
        return prediction[0][0]
    else:
        return "Zero taiwanese baby was born"


