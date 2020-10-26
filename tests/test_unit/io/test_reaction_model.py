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


"""Expect that reaction models function as designed."""


import pytest

from cobra_component_models.io import ReactionModel


def test_empty_init():
    """Expect that a reaction model can be instantiated without default arguments."""
    obj = ReactionModel(id="1")
    assert obj.reactants == {}
    assert obj.products == {}
    assert obj.sbo_term is None
    assert obj.notes is None
    assert obj.names == {}
    assert obj.annotation == {}


@pytest.mark.parametrize(
    "attributes",
    [
        {"id": "1", "reactants": {"1": {"stoichiometry": "2", "compartment": "2"}}},
        {"id": "1", "products": {"2": {"stoichiometry": "1", "compartment": "1"}}},
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
                    {"identifier": "one"},
                    {"identifier": "two"},
                ]
            },
        },
    ],
)
def test_init(attributes):
    """Expect that the object is properly initialized."""
    ReactionModel.parse_obj(attributes)
