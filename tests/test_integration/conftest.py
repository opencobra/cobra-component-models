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


from pathlib import Path
from typing import Dict

import pytest
import toml
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm import sessionmaker

from cobra_component_models.builder import CompartmentBuilder, CompoundBuilder
from cobra_component_models.io import CompartmentModel, CompoundModel
from cobra_component_models.orm import Base, Compartment, Compound, Namespace


data_path = Path(__file__).parent / "data"


Session = sessionmaker()


@pytest.fixture(scope="session")
def connection() -> Connection:
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
def session(connection: Connection) -> Session:
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


@pytest.fixture(scope="session")
def namespaces_data() -> dict:
    """Return the namespaces data objects."""
    with (data_path / "namespaces.toml").open() as handle:
        namespaces = toml.load(handle)
    return namespaces


@pytest.fixture(scope="session")
def compounds_data() -> dict:
    """Return the compounds data objects."""
    with (data_path / "compounds.toml").open() as handle:
        compounds = toml.load(handle)
    return compounds


@pytest.fixture(scope="session")
def compartments_data() -> dict:
    """Return the compartments data objects."""
    with (data_path / "compartments.toml").open() as handle:
        compartments = toml.load(handle)
    return compartments


@pytest.fixture(scope="session")
def reactions_data() -> dict:
    """Return the reactions data objects."""
    with (data_path / "reactions.toml").open() as handle:
        reactions = toml.load(handle)
    return reactions


@pytest.fixture(scope="function")
def namespaces(session: Session, namespaces_data: dict) -> Dict[str, Namespace]:
    """Return a map from namespace prefix to database instance."""
    result = {}
    for prefix, data in namespaces_data.items():
        ns = Namespace(**data)
        session.add(ns)
        result[prefix] = ns
    session.commit()
    return result


@pytest.fixture(scope="function")
def id2compartments(
    session: Session,
    namespaces: Dict[str, Namespace],
    compartments_data: dict,
) -> Dict[str, Compartment]:
    """Return a map from identifier to compartment database instance."""
    builder = CompartmentBuilder(namespaces=namespaces)
    result = {}
    for id, data in compartments_data.items():
        model = CompartmentModel.parse_obj(data)
        compartment = builder.build_orm(model)
        session.add(compartment)
        result[id] = compartment
    session.commit()
    return result


@pytest.fixture(scope="function")
def compartments2id(id2compartments: Dict[str, Compartment]) -> Dict[Compartment, str]:
    """Return a map from compartment database instance to identifier ."""
    return {c: i for i, c in id2compartments.items()}


@pytest.fixture(scope="function")
def id2compounds(
    session: Session,
    namespaces: Dict[str, Namespace],
    compounds_data: dict,
) -> Dict[str, Compound]:
    """Return a map from identifier to compound database instance."""
    builder = CompoundBuilder(namespaces=namespaces)
    result = {}
    for id, data in compounds_data.items():
        model = CompoundModel.parse_obj(data)
        compound = builder.build_orm(model)
        session.add(compound)
        result[id] = compound
    session.commit()
    return result


@pytest.fixture(scope="function")
def compounds2id(id2compounds: Dict[str, Compound]) -> Dict[Compound, str]:
    """Return a map from compound database instance to identifier ."""
    return {c: i for i, c in id2compounds.items()}
