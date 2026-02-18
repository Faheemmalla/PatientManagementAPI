from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
#description add krne k liye in pydantic model annoted ko isseliye import kiya
import json

class Patient(BaseModel):
    # three dots ka matlab compulsory wala field
    id: Annotated[str,Field(...,description="ID of the patient",examples=["P001"])]
    name:Annotated[str,Field(...,description="Name of the patient")]
    city:Annotated[str,Field(...,description="City Where the paatient lives")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the Patient")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(...,description="Height of the patient in mtrs")]
    weight:Annotated[float,Field(...,description="Weight of the patient in kgs")]

    #bmi humay khud se calculate krna hai isseliye hum computed field ko import karenge iesko @property
    # computed field se hum apne existing field , eg id name weight height etc , dynamically naye field compute kr sakte hai
    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            verdict = "Underweight"
        elif self.bmi < 25:
            verdict = "Normal"
        elif self.bmi < 30:
            verdict = "Normal"
        else:
            return "Obese"




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
#file mai write krne k liye utility function
def save_data(data):
    with open('patients.json','w') as f:
            json.dump(data,f) # dump yaane hum ies file mai likh rahe hai jo data pass kiya
            #matlab hum json file ko dictionary mai daal rahe hai
    
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

@app.post('/create')

def create_patient(patient: Patient): # yaane humne patient(saara data ) data bhja jo pydantic model Patient ko call karega to check kya data sahi hai agr sahi nhi tha then issi step pe error aajayega and sath mai computed field wala bhi automatically calculate ho raha hai

    #load existing data
    data = load_data()
    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    #new patient add to database
    data[patient.id] = patient.model_dump(exclude=['id']) # model dump model ko dictionary mai convert krta hai id is our key isseliye exlcude and baaki data[patient.id] is our value , see in json id is key baaki is value
    #auppar utilitty function banayi for to write in the json file 
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'Patient created Sucessfully.'})
