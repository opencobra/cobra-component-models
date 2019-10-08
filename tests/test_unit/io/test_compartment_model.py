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


"""Expect that compartment models function as designed."""


import pytest

from cobra_component_models.io import CompartmentModel


def test_empty_init():
    """Expect that a compartment model can be instantiated without arguments."""
    obj = CompartmentModel()
    assert obj.sbo_term is None
    assert obj.notes is None
    assert obj.names == []
    assert obj.annotation == {}


@pytest.mark.parametrize(
    "attributes",
    [
        {"sbo_term": "SBO:007"},
        {"notes": "bla bla bla"},
        {"names": ["one", "two", "three"]},
        {"annotation": {"prefix": [("is", "one"), ("is", "two")]}},
    ],
)
def test_init(attributes):
    """Expect that the object is properly initialized."""
    old_value = getattr(CompartmentModel.Config, "allow_population_by_alias", False)
    CompartmentModel.Config.allow_population_by_alias = True
    obj = CompartmentModel(**attributes)
    CompartmentModel.Config.allow_population_by_alias = old_value
    for attr, value in attributes.items():
        assert getattr(obj, attr) == value
