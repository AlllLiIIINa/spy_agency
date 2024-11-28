import logging
import httpx
from sqlalchemy.orm import Session
from models.spy_cat import SpyCat
from schemas.spy_cat import SpyCatCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CAT_API_URL = "https://api.thecatapi.com/v1/breeds"


# Fetch cat breeds data from TheCatAPI
def fetch_breeds_from_api():
    logger.info("Fetching breeds from TheCatAPI...")
    with httpx.Client() as client:
        response = client.get(CAT_API_URL)
        response.raise_for_status()
        logger.info("Breeds fetched successfully.")
        return response.json()


# Validate if the provided breed exists in the API's list of breeds
def validate_breed(breed_name: str) -> bool:
    logger.info(f"Validating breed: {breed_name}")
    breeds = fetch_breeds_from_api()
    breed_names = {breed["name"].lower() for breed in breeds}
    return breed_name.lower() in breed_names


# Create a new spy cat and adds it to the database
def create_cat(db: Session, spy_cat: SpyCatCreate):
    logger.info(f"Creating a new spy cat: {spy_cat.name}")
    new_spy_cat = SpyCat(name=spy_cat.name,
                         years_of_experience=spy_cat.years_of_experience,
                         breed=spy_cat.breed,
                         salary=spy_cat.salary)
    db.add(new_spy_cat)
    db.commit()
    db.refresh(new_spy_cat)
    logger.info(f"Spy cat {new_spy_cat.name} created successfully with ID: {new_spy_cat.id}")
    return new_spy_cat


# Retrieve a spy cat from the database by its ID
def get_spy_cat(db: Session, spy_cat_id: int):
    logger.info(f"Fetching spy cat with ID: {spy_cat_id}")
    return db.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()


# Lists all spy cats with pagination (skip and limit)
def list_spy_cats(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"Listing spy cats with skip: {skip}, limit: {limit}")
    return db.query(SpyCat).offset(skip).limit(limit).all()


# Updates the salary of an existing spy cat
def update_spy_cat_salary(db: Session, spy_cat_id: int, salary: int):
    logger.info(f"Updating salary for spy cat with ID: {spy_cat_id}")
    cat = db.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()
    cat.salary = salary
    db.commit()
    db.refresh(cat)
    logger.info(f"Salary for spy cat ID {spy_cat_id} updated to {salary}.")
    return cat


# Deletes a spy cat from the database by its ID
def delete_spy_cat(db: Session, spy_cat_id: int):
    logger.info(f"Deleting spy cat with ID: {spy_cat_id}")
    db_mission = db.query(SpyCat).filter(SpyCat.id == spy_cat_id).first()
    db.delete(db_mission)
    db.commit()
    logger.info(f"Spy cat with ID {spy_cat_id} deleted successfully.")
    return {"message": f"Spy cat with ID {spy_cat_id} deleted successfully."}
