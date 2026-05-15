from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="CanalBreak Travel API",
    description="Backend API for a travel planning platform that collects client preferences, estimates budgets, suggests destinations, and generates structured itineraries.",
    version="1.0.0"
)


class TripRequest(BaseModel):
    destination: str
    number_of_days: int
    budget: float
    travelers: int
    interests: List[str]
    travel_style: Optional[str] = "balanced"


class BudgetRequest(BaseModel):
    destination: str
    number_of_days: int
    travelers: int
    hotel_level: Optional[str] = "mid-range"
    activities_level: Optional[str] = "standard"


class ClientIntakeRequest(BaseModel):
    name: str
    departure_city: str
    destination: str
    start_date: str
    end_date: str
    travelers: int
    budget: float
    travel_style: str
    interests: List[str]
    hotel_preference: Optional[str] = "mid-range"
    food_preferences: Optional[str] = "local food"
    pace: Optional[str] = "balanced"
    must_do_activities: Optional[List[str]] = []
    avoid: Optional[List[str]] = []
    special_needs: Optional[str] = None


@app.get(
    "/",
    summary="API welcome message",
    description="Returns a basic confirmation that the CanalBreak API is running."
)
def root():
    return {
        "message": "Welcome to the CanalBreak Travel API",
        "docs": "/docs",
        "status": "running"
    }


@app.get(
    "/health",
    summary="Health check",
    description="Checks whether the API is currently running correctly."
)
def health_check():
    return {
        "status": "ok",
        "message": "CanalBreak API is healthy and running"
    }


@app.get(
    "/required-inputs",
    summary="Get required client inputs",
    description="Returns the information needed from a travel client before generating a trip plan."
)
def required_inputs():
    return {
        "basic_information": [
            "departure_city",
            "destination",
            "start_date",
            "end_date",
            "number_of_travelers",
            "budget"
        ],
        "preferences": [
            "travel_style",
            "interests",
            "hotel_preference",
            "food_preferences",
            "pace"
        ],
        "constraints": [
            "must_do_activities",
            "avoid",
            "special_needs"
        ]
    }


@app.get(
    "/destinations",
    summary="Get suggested destinations",
    description="Returns sample destination options with travel categories and average daily budget estimates."
)
def get_destinations():
    return [
        {
            "name": "Panama City",
            "country": "Panama",
            "best_for": ["culture", "food", "canal", "nightlife"],
            "average_daily_budget_per_person": 150
        },
        {
            "name": "Bocas del Toro",
            "country": "Panama",
            "best_for": ["beaches", "surfing", "relaxation"],
            "average_daily_budget_per_person": 120
        },
        {
            "name": "Boquete",
            "country": "Panama",
            "best_for": ["nature", "coffee farms", "hiking", "cool weather"],
            "average_daily_budget_per_person": 100
        },
        {
            "name": "San Blas",
            "country": "Panama",
            "best_for": ["islands", "beaches", "unique culture", "relaxation"],
            "average_daily_budget_per_person": 180
        }
    ]


@app.post(
    "/client-intake",
    summary="Submit client travel intake",
    description="Collects client travel preferences and returns a clean summary that a travel agency could use to start planning."
)
def client_intake(request: ClientIntakeRequest):
    return {
        "client_name": request.name,
        "trip_summary": {
            "route": f"{request.departure_city} to {request.destination}",
            "dates": f"{request.start_date} to {request.end_date}",
            "travelers": request.travelers,
            "budget": request.budget,
            "style": request.travel_style,
            "pace": request.pace
        },
        "preferences": {
            "interests": request.interests,
            "hotel_preference": request.hotel_preference,
            "food_preferences": request.food_preferences,
            "must_do_activities": request.must_do_activities,
            "avoid": request.avoid,
            "special_needs": request.special_needs
        },
        "next_step": "Use this intake information to generate a customized itinerary and budget estimate."
    }


@app.post(
    "/estimate-budget",
    summary="Estimate trip budget",
    description="Creates a basic budget estimate based on destination, trip length, number of travelers, hotel level, and activity level."
)
def estimate_budget(request: BudgetRequest):
    hotel_costs = {
        "budget": 70,
        "mid-range": 140,
        "luxury": 300
    }

    activity_costs = {
        "low": 30,
        "standard": 60,
        "premium": 120
    }

    hotel_daily = hotel_costs.get(request.hotel_level.lower(), 140)
    activity_daily = activity_costs.get(request.activities_level.lower(), 60)
    food_daily = 45
    transport_daily = 30

    total_per_day_per_person = hotel_daily + activity_daily + food_daily + transport_daily
    total_estimated_budget = total_per_day_per_person * request.number_of_days * request.travelers

    return {
        "destination": request.destination,
        "travelers": request.travelers,
        "number_of_days": request.number_of_days,
        "hotel_level": request.hotel_level,
        "activities_level": request.activities_level,
        "estimated_daily_cost_per_person": total_per_day_per_person,
        "estimated_total_budget": total_estimated_budget,
        "currency": "USD"
    }


@app.post(
    "/generate-trip",
    summary="Generate a custom travel itinerary",
    description="Generates a structured day-by-day itinerary based on destination, trip length, budget, traveler count, interests, and travel style."
)
def generate_trip(request: TripRequest):
    days = []

    for day in range(1, request.number_of_days + 1):
        if day == 1:
            theme = "Arrival and orientation"
            morning = "Arrive, check in, and get settled"
            afternoon = f"Explore the main area of {request.destination}"
            evening = "Enjoy a relaxed local dinner"
        elif day == request.number_of_days:
            theme = "Final highlights and departure"
            morning = "Visit one final attraction or local market"
            afternoon = "Pack, check out, and prepare for departure"
            evening = "Depart or enjoy a final meal if time allows"
        else:
            main_interest = request.interests[(day - 2) % len(request.interests)] if request.interests else "local culture"
            theme = f"{main_interest.title()} day"
            morning = f"Start with a guided or self-planned {main_interest} activity"
            afternoon = f"Continue exploring {request.destination} with time for photos and local stops"
            evening = "Dinner and optional evening activity"

        days.append({
            "day": day,
            "theme": theme,
            "morning": morning,
            "afternoon": afternoon,
            "evening": evening
        })

    return {
        "destination": request.destination,
        "number_of_days": request.number_of_days,
        "travelers": request.travelers,
        "budget": request.budget,
        "travel_style": request.travel_style,
        "interests": request.interests,
        "summary": f"A {request.number_of_days}-day {request.travel_style} trip to {request.destination} focused on {', '.join(request.interests)}.",
        "itinerary": days,
        "recommendations": {
            "hotel_area": "Stay near the main city center or safest tourist area",
            "transportation": "Use a mix of rideshare, walking, and private transportation depending on the destination",
            "planning_note": "This itinerary is a first draft and can be adjusted based on client preferences."
        }
    }