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


"""Expect that compound names function as designed."""


import pytest

from cobra_component_models.orm import CompoundName


@pytest.mark.parametrize(
    "attributes",
    [
        {"name": "water"},
        {"name": "water", "is_preferred": False},
        {"name": "water", "is_preferred": True},
    ],
)
def test_init(attributes):
    """Expect that an object can be instantiated with the right attributes."""
    instance = CompoundName(**attributes)
    for attr, value in attributes.items():
        assert getattr(instance, attr) == value


@pytest.mark.parametrize(
    "attributes, expected",
    [
        (
            {},
            "CompoundName(compound=None, name=None, namespace=None)",
        ),
        (
            {"compound_id": 22},
            "CompoundName(compound=22, name=None, namespace=None)",
        ),
        (
            {"compound_id": 22, "name": "glucose"},
            "CompoundName(compound=22, name=glucose, namespace=None)",
        ),
        (
            {"compound_id": 22, "name": "glucose", "namespace_id": 1},
            "CompoundName(compound=22, name=glucose, namespace=1)",
        ),
    ],
)
def test_repr(attributes: dict, expected: str):
    """Expect a specific string representation of a compound object."""
    instance = CompoundName(**attributes)
    assert repr(instance) == expected
