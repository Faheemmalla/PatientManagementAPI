from fastapi import FastAPI,Path,HTTPException,Query
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
def view_patient(patient_id : str = Path(...,description = 'ID of the Patient in the DB', example = "P001") ):
    #loading all patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient Not Found")
@app.get('/sort')
#teen dots ka matlab ye required hai , yaane sort by required hai
#without teen dots yaane optional
def sort_patients(sort_by : str = Query(...,description='Sort on the basis of height,weight and bmi'),
                  order : str = Query('asc',description='Sort in order of asc or desc order')):
    valid_feilds = ['height','weight','bmi']
    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400,detail=f'Invalid Field select From {valid_feilds}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')
    
    data = load_data()
    sort_order = True if order=='desc' else False
    #reverse=True desending mai sort krta hai and False Ascending mai krta hai
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0),reverse=sort_order) # ye samjho gpt se

    return sorted_data


