import logging
from typing import Optional
from sqlalchemy.orm import Session
from models.mission import Mission
from models.target import Target
from schemas.mission import MissionCreate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create a new mission and adds its targets to the database
def create_mission(db: Session, mission: MissionCreate):
    logger.info(f"Creating a new mission with spy_cat_id: {mission.spy_cat_id}")
    db_mission = Mission(spy_cat_id=mission.spy_cat_id)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    logger.info(f"Mission created with ID: {db_mission.id}")

    # Add targets to the newly created mission
    for target in mission.targets:
        logger.info(f"Adding target {target.name} for mission ID: {db_mission.id}")
        db_target = Target(name=target.name, country=target.country, notes=target.notes, mission_id=db_mission.id)
        db.add(db_target)
        db.commit()
        db.refresh(db_target)
        logger.info(f"Target {target.name} added with ID: {db_target.id}")

    return db_mission


# Fetch a mission by its ID from the database
def get_mission(db: Session, mission_id: int):
    logger.info(f"Fetching mission with ID: {mission_id}")
    return db.query(Mission).filter(Mission.id == mission_id).first()


# List of missions with pagination support (skip and limit)
def list_missions(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"Listing missions with skip: {skip}, limit: {limit}")
    return db.query(Mission).offset(skip).limit(limit).all()


# Update a target's notes and/or completion status, and updates the associated mission if all targets are complete
def update_target(db: Session, target_id: int, notes: Optional[str], complete: Optional[bool]):
    logger.info(f"Updating target with ID: {target_id}" )
    db_target = db.query(Target).filter(Target.id == target_id).first()
    if notes is not None:
        logger.info(f"Updating notes for target ID {target_id}")
        db_target.notes = notes

    if complete is not None:
        logger.info(f"Marking target ID {target_id} as complete: {complete}")
        db_target.complete = complete

    db.commit()
    db.refresh(db_target)
    logger.info(f"Target ID {target_id} updated successfully")

    # If all targets for the mission are complete, the mission mark as complete
    mission_targets = db.query(Target).filter(Target.mission_id == db_target.mission_id).all()
    if all(target.complete for target in mission_targets):  # Если все таргеты завершены
        logger.info(f"All targets for mission ID {db_target.mission_id} are complete. Marking mission as complete.")
        db_mission = db.query(Mission).filter(Mission.id == db_target.mission_id).first()
        db_mission.complete = True
        db.commit()
        db.refresh(db_mission)
        logger.info(f"Mission ID {db_target.mission_id} marked as complete.")

    return db_target


# Assign a spy cat to a mission
def assign_cat_to_mission(db: Session, mission_id: int, spy_cat_id: int):
    logger.info(f"Assigning cat ID {spy_cat_id} to mission ID {mission_id}")
    db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
    db_mission.spy_cat_id = spy_cat_id
    db.commit()
    db.refresh(db_mission)
    logger.info(f"Cat ID {spy_cat_id} successfully assigned to mission ID {mission_id}")
    return db_mission


# Delete a mission by its ID from the database
def delete_mission(db: Session, mission_id: int):
    logger.info(f"Deleting mission with ID: {mission_id}")
    db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
    db.delete(db_mission)
    db.commit()
    logger.warning(f"Mission with ID {mission_id} not found")
    return {"message": "Mission deleted"}
