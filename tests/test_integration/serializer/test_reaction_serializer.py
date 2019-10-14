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


"""Expect that reactions can be de-/serialized and selected/inserted."""


import pytest

from cobra_component_models.io import ReactionModel
from cobra_component_models.orm import (
    Participant,
    Reaction,
    ReactionAnnotation,
    ReactionName,
)
from cobra_component_models.serializer import ReactionSerializer


def test_serialize_default_reaction(session):
    """Expect that a default reaction can be serialized."""
    reaction = Reaction()
    session.add(reaction)
    session.commit()
    obj = ReactionSerializer(namespaces={}, biology_qualifiers={}).serialize(reaction)
    assert obj.id == "1"


@pytest.mark.parametrize("reaction_name", ["dehydrogenase"])
def test_serialize_full_reaction(
    session,
    biology_qualifiers,
    namespaces,
    id2compartments,
    id2compounds,
    compartments2id,
    compounds2id,
    reactions_data,
    reaction_name: str,
):
    """Expect that a fully fleshed out reaction can be serialized."""
    reaction_data = reactions_data[reaction_name]
    reaction = Reaction(notes=reaction_data["notes"])
    rhea = namespaces["rhea"]
    reaction.names = [
        ReactionName(name=n, namespace=rhea) for n in reaction_data["names"]["rhea"]
    ]
    qual = biology_qualifiers["is"]
    reaction.annotation = [
        ReactionAnnotation(identifier=i[1], namespace=rhea, biology_qualifier=qual)
        for i in reaction_data["annotation"]["rhea"]
    ]
    for compound_id, part in reaction_data["reactants"].items():
        reaction.participants.append(
            Participant(
                is_product=False,
                compound=id2compounds[compound_id],
                compartment=id2compartments[part["compartment"]],
                stoichiometry=part["stoichiometry"],
            )
        )
    for compound_id, part in reaction_data["products"].items():
        reaction.participants.append(
            Participant(
                is_product=True,
                compound=id2compounds[compound_id],
                compartment=id2compartments[part["compartment"]],
                stoichiometry=part["stoichiometry"],
            )
        )
    session.add(reaction)
    session.commit()
    obj = ReactionSerializer(
        biology_qualifiers=biology_qualifiers,
        namespaces=namespaces,
        compartment2id=compartments2id,
        compound2id=compounds2id,
    ).serialize(reaction)
    assert obj.notes == reaction_data["notes"]
    assert obj.names == reaction_data["names"]
    for prefix, annotation in reaction_data["annotation"].items():
        assert obj.annotation[prefix] == [tuple(a) for a in annotation]
    assert obj.reactants == reaction_data["reactants"]
    assert obj.products == reaction_data["products"]


@pytest.mark.parametrize("reaction_name", ["dehydrogenase"])
def test_deserialize_full_reaction(
    session,
    biology_qualifiers,
    namespaces,
    id2compartments,
    id2compounds,
    compartments2id,
    compounds2id,
    reactions_data,
    reaction_name: str,
):
    """Expect that a fully fleshed out reaction can be deserialized."""
    reaction_data = reactions_data[reaction_name]
    obj = ReactionModel(**reaction_data)
    reaction = ReactionSerializer(
        biology_qualifiers=biology_qualifiers,
        namespaces=namespaces,
        id2compartment=id2compartments,
        id2compound=id2compounds,
    ).deserialize(obj)
    session.add(reaction)
    session.commit()
    assert reaction.notes == reaction_data["notes"]
    for name, expected in zip(reaction.names, reaction_data["names"]["rhea"]):
        assert name.namespace.prefix == "rhea"
        assert name.name == expected
    for ann, expected in zip(reaction.annotation, reaction_data["annotation"]["rhea"]):
        assert ann.namespace.prefix == "rhea"
        assert (ann.biology_qualifier.qualifier, ann.identifier) == tuple(expected)
    for part in reaction.participants:
        compound_id = compounds2id[part.compound]
        if part.is_product:
            assert compound_id in reaction_data["products"]
            part_data = reaction_data["products"][compound_id]
        else:
            assert compound_id in reaction_data["reactants"]
            part_data = reaction_data["reactants"][compound_id]
        compartment_id = compartments2id[part.compartment]
        assert compartment_id == part_data["compartment"]
        assert part.stoichiometry == part_data["stoichiometry"]
