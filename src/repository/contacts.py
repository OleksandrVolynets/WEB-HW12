from datetime import date
from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase


async def create_contact(body: ContactBase, db: Session, user=User):
    contact = Contact(**body.model_dump(), user_id=user.id)
    db.add(contact)
    db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactBase, db: Session, user=User):
    contact = await get_contact_by_id(contact_id, db, user_id=user.id)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user=User):
    contact = await get_contact_by_id(contact_id, db, user_id=user.id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contact(keyword: str, db: Session):
    contacts = db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{keyword}%")) |
        (Contact.last_name.ilike(f"%{keyword}%")) |
        (Contact.email.ilike(f"%{keyword}%"))
    ).all()
    return contacts


async def get_contacts(db: Session, user=User):
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session, user=User):
    contact = db.query(Contact).filter(
        Contact.id == contact_id, Contact.user_id == user.id).first()
    return contact


async def get_contact_by_email(email: str, db: Session, user=User):
    contact = db.query(Contact).filter(
        Contact.email == email, Contact.user_id == user.id).first()
    return contact


async def get_contact_by_phone(phone_number: str, db: Session, user=User):
    contact = db.query(Contact).filter(
        Contact.phone_number == phone_number, Contact.user_id == user.id).first()
    return contact


async def get_birthdays(days: int, db: Session, user=User):
    contacts_with_birthdays = []
    today = date.today()
    current_year = today.year
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in contacts:
        td = contact.birthday.replace(year=current_year) - today
        if 0 <= td.days <= days:
            contacts_with_birthdays.append(contact)
        else:
            continue
    print(contacts_with_birthdays)
    return contacts_with_birthdays
