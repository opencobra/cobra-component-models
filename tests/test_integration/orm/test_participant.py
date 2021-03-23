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


"""Expect that participants function as designed."""


import pytest

from cobra_component_models.orm import Participant


@pytest.mark.parametrize(
    "attributes",
    [
        {"stoichiometry": "1", "is_product": True},
        {"stoichiometry": "1", "is_product": False},
    ],
)
def test_init(attributes):
    """Expect that an object can be instantiated with the right attributes."""
    instance = Participant(**attributes)
    for attr, value in attributes.items():
        assert getattr(instance, attr) == value


@pytest.mark.parametrize(
    "attributes, expected",
    [
        (
            {"stoichiometry": "1.0", "is_product": True},
            "Participant(reaction=None, compound=None, stoichiometry=1.0)",
        ),
        (
            {"stoichiometry": "1.0", "is_product": False},
            "Participant(reaction=None, compound=None, stoichiometry=-1.0)",
        ),
        (
            {"reaction_id": 22, "stoichiometry": "1.0", "is_product": True},
            "Participant(reaction=22, compound=None, stoichiometry=1.0)",
        ),
        (
            {
                "reaction_id": 22,
                "compound_id": 2,
                "stoichiometry": "1.0",
                "is_product": True,
            },
            "Participant(reaction=22, compound=2, stoichiometry=1.0)",
        ),
    ],
)
def test_repr(attributes: dict, expected: str):
    """Expect a specific string representation of a compartment object."""
    instance = Participant(**attributes)
    assert repr(instance) == expected
