from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactBase, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Contact not found')
    return contact


@router.get('/', response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(db, current_user)
    return contacts


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact_email = await repository_contacts.get_contact_by_email(body.email, db, current_user)
    contact_phone_number = await repository_contacts.get_contact_by_phone(body.phone_number, db, current_user)
    if contact_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Email already exist')
    if contact_phone_number:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Phone number already exist')
    contact = await repository_contacts.create_contact(body, db, current_user)
    return contact


@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Contact not found')
    return contact


@router.delete('/{contact_id}', response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Contact not found')
    return contact


@router.get('/search/keyword={keyword}', response_model=List[ContactResponse])
async def search_contact(keyword: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contact(keyword, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Contact with keyword "{keyword}" not found')
    return contacts


@router.get('/birthdays/{days}', response_model=List[ContactResponse])
async def get_birthdays_list(days: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    birthdays = await repository_contacts.get_birthdays(days, db, current_user)
    return birthdays
