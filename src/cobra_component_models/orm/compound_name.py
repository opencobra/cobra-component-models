# Copyright (c) 2019, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide a compound name ORM model."""


from sqlalchemy import Column, ForeignKey, Integer

from .base import Base
from .mixin import NameMixin, TimestampMixin


class CompoundName(NameMixin, TimestampMixin, Base):
    """
    Define a compound name ORM model.

    Attributes
    ----------
    id : int
        The primary key in the table.
    compound_id : int
        The compound being named.

    """

    __tablename__ = "compound_names"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    compound_id: int = Column(Integer, ForeignKey("compounds.id"), nullable=False)

    def __repr__(self):
        return (
            f"{type(self).__name__}(compound={self.compound_id}, "
            f"name={self.name}, "
            f"namespace={self.namespace_id})"
        )
