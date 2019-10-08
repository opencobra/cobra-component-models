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


"""Provide a reaction participant (reagent/product) ORM model."""


from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .compartment import Compartment
from .compound import Compound


class Participant(Base):
    """
    Define a reaction participant (reagent/product) ORM model.

    Attributes
    ----------
    stoichiometry : str

    """

    __tablename__ = "participants"

    reaction_id: int = Column(Integer, ForeignKey("reactions.id"), nullable=False)
    compound_id: int = Column(Integer, ForeignKey("compounds.id"), nullable=False)
    compound: Compound = relationship("Compound")
    stoichiometry: str = Column(String, nullable=False)
    is_product: bool = Column(Boolean, nullable=False)
    compartment_id: Optional[int] = Column(
        Integer, ForeignKey("compartments.id"), nullable=True
    )
    compartment: Compartment = relationship("Compartment")

    def __repr__(self):
        """Return a string representation of the object."""
        return (
            f"{type(self).__name__}(id={self.id}, stoichiometry={self.stoichiometry})"
        )
