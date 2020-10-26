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


"""Expect that reactions function as designed."""


import pytest

from cobra_component_models.orm import (
    Namespace,
    Reaction,
    ReactionAnnotation,
    ReactionName,
)


@pytest.mark.parametrize(
    "attributes", [{}, {"id": 22}, {"notes": "I should not forget about this!"}]
)
def test_init(attributes):
    """Expect that an object can be instantiated with the right attributes."""
    instance = Reaction(**attributes)
    for attr, value in attributes.items():
        assert getattr(instance, attr) == value


def test_names(session):
    """Expect that names can be added to a reaction."""
    reaction = Reaction()
    namespace = Namespace(miriam_id="MIR:00000082", prefix="rhea", pattern=r"^\d{5}$")
    reaction.names.append(
        ReactionName(namespace=namespace, name="alcohol dehydrogenase")
    )
    session.add(reaction)
    session.commit()


def test_annotation(session):
    """Expect that annotations can be added to a reaction."""
    reaction = Reaction()
    namespace = Namespace(miriam_id="MIR:00000082", prefix="rhea", pattern=r"^\d{5}$")
    reaction.annotation.append(
        ReactionAnnotation(identifier="25290", namespace=namespace)
    )
    session.add(reaction)
    session.commit()
