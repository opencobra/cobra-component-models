# Copyright (c) 2019-2020, Moritz E. Beber.
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


"""Provide a component annotation model."""


from importlib.resources import open_text

from pydantic import Field, validator

from .. import data
from .io_base import IOBase


# A list of qualifiers taken from https://co.mbine.org/standards/qualifiers.
with open_text(data, "biology_qualifiers.txt") as handler:
    BIOLOGY_QUALIFIERS = frozenset(line.strip() for line in handler.readlines())


class AnnotationModel(IOBase):
    """
    Define a component annotation model.

    An annotation consists of a pair of strings representing a biology qualifier and
    an identifier from a specific namespace.

    """

    biology_qualifier: str = Field(..., alias="biologyQualifier")
    identifier: str
    is_deprecated: bool = Field(False, alias="isDeprecated")

    @validator("biology_qualifier")
    def biology_qualifier_must_be_known(cls, qualifier: str):
        """Validate and transform the given biology qualifier."""
        if qualifier not in BIOLOGY_QUALIFIERS:
            raise ValueError(
                "The qualifier must be one of the valid biology qualifiers defined "
                "at https://co.mbine.org/standards/qualifiers."
            )
        return qualifier
