# Copyright (c) 2019, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide fixtures for managing a SQLAlchemy session."""


import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cobra_component_models.orm import Base, BiologyQualifier


Session = sessionmaker()


@pytest.fixture(scope="session")
def connection():
    """
    Use a SQLAlchemy connection such that transactions can be used.

    Notes
    -----
    Follows a transaction pattern described in the following documentation:
    http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#session-begin-nested

    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture(scope="function")
def session(connection):
    """
    Create a transaction and session per test unit.

    Rolling back a transaction removes even committed rows
    (``session.commit``) from the database.

    """
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()


@pytest.fixture(scope="function")
def biology_qualifiers(session):
    """Return a map from biology qualifiers to model instances."""
    BiologyQualifier.load(session)
    return BiologyQualifier.get_map(session)
