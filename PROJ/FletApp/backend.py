from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
import random  # Import for random selection

app = FastAPI()

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
