from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from database import Base, engine
from service import create_shipment
from sqlalchemy.orm import Session
from database import get_db

Base.metadata.create_all(bind=engine)
app = FastAPI()

class ShipmentCreate(BaseModel):
    tracking_number:str
    # status:str = Field(default="PREPARING")



@app.post("/shipments")
def create_ship(new_shipment:ShipmentCreate, db:Session = Depends(get_db)):
    shipment = create_shipment(db=db, tracking_number=new_shipment.tracking_number)
    # return {
    #     # "status":shipment.status,
    #     "tracking_number":shipment.tracking_number
    # }
