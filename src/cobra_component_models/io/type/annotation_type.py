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


"""Provide a custom pydantic type for component annotations."""


from importlib.resources import open_text
from typing import List, Tuple

from ... import data


# A list of qualifiers taken from https://co.mbine.org/standards/qualifiers.
with open_text(data, "biology_qualifiers.txt") as handler:
    BIOLOGY_QUALIFIERS = frozenset(l.strip() for l in handler.readlines())


class AnnotationType(tuple):
    """
    Define a custome pydantic type for component annotations.

    An annotation consists of a pair of strings representing a biology qualifier and
    an identifier from a specific namespace.

    """

    @classmethod
    def __get_validators__(cls):
        """Implement pydantic special behavior."""
        yield cls.validate

    @classmethod
    def validate(cls, value: List[str]) -> Tuple[str, str]:
        """Validate and transform the given annotation."""
        try:
            qualifier, identifier = value
        except (ValueError, TypeError) as exc:
            raise ValueError(
                "Each annotation must consist of a biology qualifier "
                "(https://co.mbine.org/standards/qualifiers), "
                "identifier pair."
            ) from exc
        if qualifier not in BIOLOGY_QUALIFIERS:
            raise ValueError(
                "The qualifier must be one of the valid biology qualifiers defined "
                "at https://co.mbine.org/standards/qualifiers."
            )
        return qualifier, identifier
