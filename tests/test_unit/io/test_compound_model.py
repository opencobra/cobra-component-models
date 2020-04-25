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


"""Expect that compound models function as designed."""


import pytest

from cobra_component_models.io import CompoundModel


def test_empty_init():
    """Expect that a compound model can be instantiated without default arguments."""
    obj = CompoundModel(id="1")
    assert obj.charge is None
    assert obj.chemical_formula is None
    assert obj.sbo_term is None
    assert obj.notes is None
    assert obj.names == {}
    assert obj.annotation == {}


@pytest.mark.parametrize(
    "attributes",
    [
        {"id": "1", "charge": -2.0},
        {"id": "1", "chemical_formula": "C2H6O"},
        {"id": "1", "sbo_term": "SBO:007"},
        {"id": "1", "notes": "bla bla bla"},
        {
            "id": "1",
            "names": {
                "synonyms": [{"name": "one"}, {"name": "two"}, {"name": "three"}]
            },
        },
        {
            "id": "1",
            "annotation": {
                "prefix": [
                    {"biology_qualifier": "is", "identifier": "one"},
                    {"biology_qualifier": "is", "identifier": "two"},
                ]
            },
        },
    ],
)
def test_init(attributes):
    """Expect that the object is properly initialized."""
    CompoundModel.parse_obj(attributes)
