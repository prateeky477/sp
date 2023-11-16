from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LocationData(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime  # Change the type to datetime

previous_location: LocationData = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/speed")
async def get_speed(location_data: LocationData):
    global previous_location
    print(location_data)
    if previous_location is not None:
        time_difference = (location_data.timestamp - previous_location.timestamp).total_seconds()

        distance = ((location_data.latitude - previous_location.latitude)**2 +
                    (location_data.longitude - previous_location.longitude)**2)**0.5

        speed = distance / time_difference

        previous_location = location_data
        print(speed)
        return {"speed": speed}
    else:
        previous_location = location_data
        return {"speed": 0.0}
