#!/usr/bin/env python3
"""DB module
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict

from user import Base
from user import User

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """returns a User object.
        The method saves the user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)

        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """returns the first row found in the users table as
        filtered by the method's input arguments"""
        query = self._session.query(User)

        try:
            query_fil = query.filter_by(**kwargs).one()

        # except InvalidRequestError:
        #    raise InvalidRequestError()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()

        return query_fil

    def update_user(self, user_id: int, **kwargs: Dict[str, str]) -> None:
        """method that takes as argument a required user_id
        integer and arbitrary keyword arguments, and returns None"""
        