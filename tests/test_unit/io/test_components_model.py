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


"""Expect that components models function as designed."""


import pytest

from cobra_component_models.io import ComponentsModel


def test_empty_init():
    """Expect that a components model can be instantiated without arguments."""
    obj = ComponentsModel()
    assert obj.reactions == {}
    assert obj.compartments == {}
    assert obj.compounds == {}


@pytest.mark.parametrize(
    "attributes",
    [
        {"reactions": {"1": {"id": "1"}}},
        {"compartments": {"1": {"id": "1"}}},
        {"compounds": {"1": {"id": "1"}}},
    ],
)
def test_init(attributes):
    """Expect that the object is properly initialized."""
    ComponentsModel(**attributes)
