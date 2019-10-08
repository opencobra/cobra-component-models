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


"""Provide a custom pydantic type for component notes."""


class NotesType(str):
    """Define a custom pydantic type for component notes."""

    @classmethod
    def __get_validators__(cls):
        """Implement pydantic special behavior."""
        yield cls.validate

    @classmethod
    def validate(cls, value: str):
        """Validate the notes value."""
        if not isinstance(value, str):
            raise ValueError(f"Notes need to be of type str not {type(value)}.")
        # TODO (Moritz Beber): Check XML. See also
        #  SBML spec section 3.2.5 Notes.
        # elif False:
        #     raise ValueError("SBML notes need to be well-formed XHTML content.")
        return value
