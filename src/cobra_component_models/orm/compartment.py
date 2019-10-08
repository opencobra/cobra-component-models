# Copyright (c) 2019, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide a compartment ORM model."""


from typing import List, Optional

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base
from .compartment_annotation import CompartmentAnnotation
from .compartment_name import CompartmentName


class Compartment(Base):
    """
    Define a compartment ORM model.

    Attributes
    ----------
    notes : str, optional
    names : list of cobra_component_models.orm.CompoundName, optional
    annotation : list of cobra_component_models.orm.CompoundAnnotation, optional

    """

    __tablename__ = "compartments"

    notes: Optional[str] = Column(String, nullable=True)
    names: List[CompartmentName] = relationship("CompartmentName")
    annotation: List[CompartmentAnnotation] = relationship("CompartmentAnnotation")
