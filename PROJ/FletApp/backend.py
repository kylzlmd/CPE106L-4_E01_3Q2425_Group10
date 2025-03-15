from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
import random  # Import for random selection
import requests # for the weather

app = FastAPI()

# weather api data reciever
WEATHER_API_KEY = "b742978032940364a419eb9ab1de7a51"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Connect to MongoDB
MONGO_URI = "mongodb+srv://jom:jom123@irricluster.dkeaq.mongodb.net/?retryWrites=true"
client = MongoClient(MONGO_URI)
db = client["RandomSeedSystem"]
users_collection = db["users"]
schedules_collection = db["schedules"]
plants_collection = db["plants"]  # New collection for storing grown plants

# Ensure admin user exists
if not users_collection.find_one({"username": "admin"}):
    users_collection.insert_one({"username": "admin", "password": "123456"})

# Models
class User(BaseModel):
    username: str
    password: str

class Schedule(BaseModel):
    username: str
    date: str  # Expected format: YYYY-MM-DD

# Plant color and species options
PLANT_COLORS = ["Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
PLANT_SPECIES = ["Coleus", "Dianthus", "Penstemon", "Sedum", "Lamium"]


def get_weather_data():
    api_key = WEATHER_API_KEY
    city = "Manila"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()
    
    return data


# get the weather function
@app.get("/get-weather/{location}")
def get_weather(location: str):
    params = {"q": location, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {"temperature": data["main"]["temp"], "condition": data["weather"][0]["description"]}
    return {"error": "Could not fetch weather data"}

@app.get("/weather")
def weather():
    data = get_weather_data()
    # Extract temperature data for the next 7 days (or as required)
    temperatures = [item['main']['temp'] for item in data['list'][:7]]
    days = [item['dt_txt'].split(' ')[0] for item in data['list'][:7]]  # Dates for the next 7 days
    
    return {"temperatures": temperatures, "days": days}


@app.get("/get-all-plants-by-species")
def get_all_plants_by_species():
    all_plants = list(plants_collection.find({}, {"_id": 0}))
    sorted_plants = sorted(all_plants, key=lambda p: p["species"].lower())
    return {"plants": sorted_plants}

@app.get("/get-all-plants-by-color")
def get_all_plants_by_color():
    all_plants = list(plants_collection.find({}, {"_id": 0}))
    color_order = ["Red", "Orange", "Yellow", "Green", "Blue", "Violet"]
    sorted_plants = sorted(all_plants, key=lambda p: color_order.index(p["color"]))
    return {"plants": sorted_plants}

      
# Register a new user
@app.post("/register")
def register_user(user: User):
    if users_collection.find_one({"username": user.username}):
        return {"error": "Username already exists!"}
    
    users_collection.insert_one({
        "username": user.username,
        "password": user.password,
        "seeds": 0,
        "seed_stage": 1,
        "watered": 0,
        "fertilized": 0
    })
    return {"message": "Registration successful!"}

# Login a user
@app.post("/login")
def login_user(user: User):
    user_data = users_collection.find_one({"username": user.username, "password": user.password})
    if user_data:
        return {"message": "Login successful!", "seeds": user_data.get("seeds", 0)}
    return {"error": "Invalid credentials."}

# Claim a seed
@app.post("/claim-seed/{username}")
def claim_seed(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return {"error": "User not found!"}

    # Prevent claiming a new seed until the previous one is fully grown
    if user["seeds"] > 0 and user["seed_stage"] < 3:
        return {"error": "You must fully grow your current seed before claiming another one!"}

    users_collection.update_one({"username": username}, {"$set": {"seed_stage": 1, "watered": 0, "fertilized": 0}})
    users_collection.update_one({"username": username}, {"$inc": {"seeds": 1}})
    return {"message": "You claimed a new seed!"}

# Assign a schedule (Admin only)
@app.post("/assign-schedule")
def assign_schedule(schedule: Schedule):
    user = users_collection.find_one({"username": schedule.username})
    if not user:
        return {"error": "User not found!"}
    
    schedules_collection.insert_one({"username": schedule.username, "date": schedule.date})
    return {"message": f"Schedule assigned to {schedule.username} on {schedule.date}."}

# Get a volunteer's schedule
@app.get("/get-schedule/{username}")
def get_schedule(username: str):
    schedule = list(schedules_collection.find({"username": username}, {"_id": 0}))
    return {"schedule": schedule}

# Get user seed information
@app.get("/get-user/{username}")
def get_user(username: str):
    user = users_collection.find_one({"username": username}, {"_id": 0})
    if not user:
        return {"error": "User not found!"}
    return user

# Water seed
@app.post("/water-seed/{username}")
def water_seed(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return {"error": "User not found!"}

    if user["seed_stage"] >= 3:
        return {"message": "Your seed is fully grown! You can't water it anymore."}

    users_collection.update_one({"username": username}, {"$inc": {"watered": 1}})

    user = users_collection.find_one({"username": username})
    if user["watered"] >= 5 and user["fertilized"] >= 3 and user["seed_stage"] < 3:
        users_collection.update_one({"username": username}, {"$inc": {"seed_stage": 1}})

        # Check if fully grown
        if user["seed_stage"] + 1 == 3:
            return grow_seed(username)

        return {"message": "Your seed has grown to the next stage!"}

    return {"message": "You watered your seed!"}

# Get all plants from all users (Admin only)
@app.get("/get-all-plants")
def get_all_plants():
    all_plants = []
    users = users_collection.find({}, {"_id": 0, "username": 1})  # Get all users
    for user in users:
        username = user["username"]
        plants = plants_collection.find({"username": username}, {"_id": 0, "color": 1, "species": 1})
        for plant in plants:
            plant["username"] = username  # Add username to identify which user owns the plant
            all_plants.append(plant)
    return {"plants": all_plants}



# Fertilize seed
@app.post("/fertilize-seed/{username}")
def fertilize_seed(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return {"error": "User not found!"}

    if user["seed_stage"] >= 3:
        return {"message": "Your seed is fully grown! You can't fertilize it anymore."}

    users_collection.update_one({"username": username}, {"$inc": {"fertilized": 1}})

    user = users_collection.find_one({"username": username})
    if user["watered"] >= 5 and user["fertilized"] >= 3 and user["seed_stage"] < 3:
        users_collection.update_one({"username": username}, {"$inc": {"seed_stage": 1}})

        # Check if fully grown
        if user["seed_stage"] + 1 == 3:
            return grow_seed(username)

        return {"message": "Your seed has grown to the next stage!"}

    return {"message": "You fertilized your seed!"}

# Grow seed into a random plant
def grow_seed(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        return {"error": "User not found!"}

    if user["seed_stage"] < 3:
        return {"error": "Seed is not fully grown yet!"}

    # Randomly select plant color and species
    plant_color = random.choice(PLANT_COLORS)
    plant_species = random.choice(PLANT_SPECIES)

    # Store plant in database
    plants_collection.insert_one({
        "username": username,
        "color": plant_color,
        "species": plant_species
    })

    # Reset seed state
    users_collection.update_one({"username": username}, {"$set": {"seed_stage": 3}})

    return {"message": f"🎉 Your seed has fully grown into a {plant_color} {plant_species}! 🎉 You can now claim another seed."}

# Get all users (Admin only)
@app.get("/users")
def get_all_users():
    users = list(users_collection.find({}, {"_id": 0, "password": 0}))  # Exclude `_id` and `password` fields
    return {"users": users}

# Get all plants grown by a user
@app.get("/get-plants/{username}")
def get_plants(username: str):
    plants = list(plants_collection.find({"username": username}, {"_id": 0}))
    return {"plants": plants}
