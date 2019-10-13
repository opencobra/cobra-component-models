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


"""Provide the pydantic SBase data model."""


from typing import Dict, List, Optional

from pydantic import BaseModel, Schema

from .type import AnnotationType, NotesType


class SBaseModel(BaseModel):
    """Define the SBase data model."""

    id: Optional[str] = None
    sbo_term: Optional[str] = Schema(None, alias="sboTerm")
    notes: Optional[NotesType] = None
    names: Dict[str, List[str]] = {}
    annotation: Dict[str, List[AnnotationType]] = {}

    class Config:
        """Configure the SBase data model."""

        orm_mode = True
