from fastapi import FastAPI,Path
import json

app = FastAPI()
@app.get('/') #yaane hamari http wali link k baad / ye daale toh he will get helloworld
def hello():
    return {'message':"Patient Management System API"}
@app.get('/about') # ye hum alag alag route define krte hai 
#and ies route k andar alag alag endpoints like here its /about
#fir ieske neeche function likhte hai yaane logic

def hello2():
    return {'message':"A Fully Functional API to manage your Patient Records "}

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    
    return data
@app.get('/view')
def view():
    data = load_data()

    return data
@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(...,description = 'ID of the Patient in the DB') ):
    #loading all patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {'error':'patient not found'}