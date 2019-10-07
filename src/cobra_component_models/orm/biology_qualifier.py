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


"""Provide a biology qualifier ORM model."""


from __future__ import annotations

from importlib.resources import open_text

from sqlalchemy import Column, Integer, String, exists

from .. import data
from .base import Base
from .timestamp_mixin import TimestampMixin


class BiologyQualifier(TimestampMixin, Base):
    """
    Define a BioModels biology qualifier ORM model.

    You can read more about them at http://co.mbine.org/standards/qualifiers.

    Attributes
    ----------
    id : int
        The integer primary key in the table.
    qualifier : str
        The text value of the qualifier.

    """

    __tablename__ = "biology_qualifiers"

    id: int = Column(Integer, primary_key=True)
    qualifier: str = Column(String, nullable=False, index=True, unique=True)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{type(self).__name__}(qualifier={self.qualifier})"

    @classmethod
    def load(cls, session):
        """Load all known biology qualifiers into the given database."""
        with open_text(data, "biology_qualifiers.txt") as handler:
            qualifiers = [l.strip() for l in handler.readlines()]
        for qual in qualifiers:
            if (
                qual
                and not session.query(exists().where(cls.qualifier == qual)).scalar()
            ):
                session.add(cls(qualifier=qual))
        session.commit()
