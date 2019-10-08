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


"""Provide a pydantic components data model."""


from typing import Dict, Optional

from pydantic import BaseModel

from .compartment_model import CompartmentModel
from .compound_model import CompoundModel
from .reaction_model import ReactionModel


class ComponentsModel(BaseModel):
    """Define the components data model."""

    reactions: Optional[Dict[str, ReactionModel]] = {}
    compartments: Optional[Dict[str, CompartmentModel]] = {}
    compounds: Optional[Dict[str, CompoundModel]] = {}

    class Config:
        """Configure the SBase data model."""

        orm_mode = True
