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


"""Provide a component name model."""


from pydantic import Field

from .io_base import IOBase


class NameModel(IOBase):
    """
    Define a component name model.

    Names are simple strings and should be interpretable by human beings. They can also
    be the preferred name to describe a component.

    """

    name: str
    is_preferred: bool = Field(False, alias="isPreferred")
