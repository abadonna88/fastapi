from fastapi import APIRouter, Body, HTTPException, status, Request, Depends
from database.connection import get_session, Database
from models.events import Event, EventUpdate
from typing import List
from beanie import PydanticObjectId


event_database = Database(Event)
event_router = APIRouter(tags=["Events"])
events = []


@event_router.get("/d", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_router.get("/d/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event with supplied ID doesn't exists")
    return event

@event_router.post("/d/new")
async def create_event(body: Event) -> dict:
    await event_database.save(body)
    return {"message": "Event created successfully"}


@event_router.put("/d/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event with supplied ID doesn't exists")
    return updated_event


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId) -> dict:
    event = await event_database.delete(d)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event with supplied ID doesn't exists")
    return {"message": "Event deleted successfully."}


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    events = session.all()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    ) 


@event_router.post("/new")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {"message": "Event created successfully"}


@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    ) 


@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {"message": "Events deleted successfully"}


@event_router.delete("/delete/{id}")
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return {"message": "Event deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
    
