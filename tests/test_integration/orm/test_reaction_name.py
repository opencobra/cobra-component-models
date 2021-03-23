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


"""Expect that reaction names function as designed."""


import pytest

from cobra_component_models.orm import Namespace, ReactionName


@pytest.mark.parametrize(
    "attributes",
    [
        {"name": "alcohol dehydrogenase"},
        {"name": "alcohol dehydrogenase", "is_preferred": False},
        {"name": "alcohol dehydrogenase", "is_preferred": True},
    ],
)
def test_init(attributes):
    """Expect that an object can be instantiated with the right attributes."""
    namespace = Namespace(miriam_id="MIR:00000082", prefix="rhea", pattern=r"^\d{5}$")
    instance = ReactionName(namespace=namespace, **attributes)
    for attr, value in attributes.items():
        assert getattr(instance, attr) == value


@pytest.mark.parametrize(
    "attributes, expected",
    [
        (
            {},
            "ReactionName(reaction=None, name=None, namespace=None)",
        ),
        (
            {"reaction_id": 22},
            "ReactionName(reaction=22, name=None, namespace=None)",
        ),
        (
            {"reaction_id": 22, "name": "glucose"},
            "ReactionName(reaction=22, name=glucose, namespace=None)",
        ),
        (
            {"reaction_id": 22, "name": "glucose", "namespace_id": 1},
            "ReactionName(reaction=22, name=glucose, namespace=1)",
        ),
    ],
)
def test_repr(attributes: dict, expected: str):
    """Expect a specific string representation of a reaction object."""
    instance = ReactionName(**attributes)
    assert repr(instance) == expected
