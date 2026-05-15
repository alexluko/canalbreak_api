from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()




class TripRequest(BaseModel):
    budget: float
    duration: int
    group_size: int
    interests: List[str]


@app.get("/")
def root():
    return {"message": "CanalBreak API is running"}


@app.post("/generate-trip")
def generate_trip(request: TripRequest):

    if request.budget <= 0:
        raise HTTPException(
            status_code=400,
            detail="Budget must be greater than 0."
        )

    return {
        "trip_plan": {
            "destination": "Panama City + San Blas",
            "duration": request.duration,
            "group_size": request.group_size,
            "recommended_hotels": [
                "W Panama",
                "Selina Casco Viejo"
            ],
            "activities": [
                "San Blas island hopping",
                "Casco Viejo nightlife",
                "Rooftop dining",
                "Panama Canal visit"
            ],
            "estimated_budget": request.budget
        }
    }

@app.get("/destinations")
def get_destinations():

    return {
        "destinations": [
            "Panama City",
            "San Blas",
            "Bocas del Toro",
            "Boquete",
            "Playa Venao"
        ]
    }


class BudgetRequest(BaseModel):
    travelers: int
    duration: int


@app.post("/estimate-budget")
def estimate_budget(request: BudgetRequest):

    hotel_cost = request.travelers * request.duration * 120
    activity_cost = request.travelers * request.duration * 60
    transportation_cost = request.travelers * 80

    total = (
        hotel_cost
        + activity_cost
        + transportation_cost
    )

    return {
        "hotel_cost": hotel_cost,
        "activity_cost": activity_cost,
        "transportation_cost": transportation_cost,
        "estimated_total": total
    }