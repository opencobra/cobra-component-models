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


"""Expect that compartment names function as designed."""


import pytest

from cobra_component_models.orm import CompartmentName


@pytest.mark.parametrize(
    "attributes",
    [
        {"name": "cytoplasm"},
        {"name": "cytoplasm", "is_preferred": False},
        {"name": "cytoplasm", "is_preferred": True},
    ],
)
def test_init(attributes):
    """Expect that an object can be instantiated with the right attributes."""
    instance = CompartmentName(**attributes)
    for attr, value in attributes.items():
        assert getattr(instance, attr) == value


@pytest.mark.parametrize(
    "attributes, expected",
    [
        (
            {},
            "CompartmentName(compartment=None, name=None, namespace=None)",
        ),
        (
            {"compartment_id": 22},
            "CompartmentName(compartment=22, name=None, namespace=None)",
        ),
        (
            {"compartment_id": 22, "name": "glucose"},
            "CompartmentName(compartment=22, name=glucose, namespace=None)",
        ),
        (
            {"compartment_id": 22, "name": "glucose", "namespace_id": 1},
            "CompartmentName(compartment=22, name=glucose, namespace=1)",
        ),
    ],
)
def test_repr(attributes: dict, expected: str):
    """Expect a specific string representation of a compartment object."""
    instance = CompartmentName(**attributes)
    assert repr(instance) == expected
