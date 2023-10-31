#!/usr/bin/python3
""" holds class User"""
import models
import hashlib
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
        places = relationship(
            "Place",
            cascade="all, delete, delete-orphan",
            backref="user"
        )
        reviews = relationship(
            "Review",
            cascade="all, delete, delete-orphan",
            backref="user"
        )
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, __name: str, __value) -> None:
        '''Setting attribute of a class to a value.'''
        if __name == 'password':
            if type(__value) is str:
                md_hash = hashlib.md5(bytes(__value, 'utf-8'))
                super().__setattr__(__name, m_hash.hexdigest())
        else:
            super().__setattr__(__name, __value)
