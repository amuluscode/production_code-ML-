from fastapi import FastAPI, HTTPException,Path,Query
import json
app=FastAPI()
def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data
@app.get("/") 
async def root() -> dict[str,str]:
    return {"message": "this is a fully functional fastapi app"}
@app.get("/view")
async def about()  :
    data=load_data()
    return data
@app.get("/patient/{patient_id}")
async def get_patient(patient_id: str= Path(..., description="The ID of the patient to retrieve",example='P001')):
    data=load_data()
    
    if  patient_id in data:
            return data[patient_id]
    HTTPException(status_code=404, detail="Patient not found")
@app.get('/sort')
def sort_values(sort_by: str =Query(...,description="sort by age,name,height,bmi",example='age'),order: str = Query('asc', description="Order of sorting: asc or desc", example='asc')):
    valid_data=['height','age','name','bmi','weight']
    if sort_by not in valid_data:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by parameter{valid_data}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=False if order == 'asc' else True)
    return sorted_data
   
