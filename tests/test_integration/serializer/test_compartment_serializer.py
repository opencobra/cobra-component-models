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


"""Expect that compartments can be de-/serialized and selected/inserted."""


from cobra_component_models.io import CompartmentModel
from cobra_component_models.orm import (
    Compartment,
    CompartmentAnnotation,
    CompartmentName,
)
from cobra_component_models.serializer import CompartmentSerializer


def test_serialize_default_compartment(session):
    """Expect that a default compartment can be serialized."""
    cmpd = Compartment()
    session.add(cmpd)
    session.commit()
    obj = CompartmentSerializer(namespaces={}, biology_qualifiers={}).serialize(cmpd)
    assert obj.id == "1"


def test_serialize_full_compartment(session, biology_qualifiers, namespaces):
    """Expect that a fully fleshed out compartment can be serialized."""
    compartment = Compartment(notes="bla bla bla")
    go = namespaces["go"]
    compartment.names = [
        CompartmentName(name=n, namespace=go) for n in ["cytosol", "cytoplasm"]
    ]
    qual = biology_qualifiers["is"]
    compartment.annotation = [
        CompartmentAnnotation(identifier=i, namespace=go, biology_qualifier=qual)
        for i in ["GO:0005737"]
    ]
    session.add(compartment)
    session.commit()
    obj = CompartmentSerializer(
        biology_qualifiers=biology_qualifiers, namespaces=namespaces
    ).serialize(compartment)
    assert obj.id == "1"
    assert obj.notes == "bla bla bla"
    assert obj.names == {"go": ["cytosol", "cytoplasm"]}
    assert obj.annotation == {"go": [("is", "GO:0005737")]}


def test_deserialize_full_compartment(session, biology_qualifiers, namespaces):
    """Expect that a fully fleshed out compartment can be deserialized."""
    obj = CompartmentModel(
        **{
            "id": "1",
            "notes": "bla bla bla",
            "names": {"go": ["cytosol", "cytoplasm"]},
            "annotation": {"go": [["is", "GO:0005737"]]},
        }
    )
    compartment = CompartmentSerializer(
        biology_qualifiers=biology_qualifiers, namespaces=namespaces
    ).deserialize(obj)
    session.add(compartment)
    session.commit()
    assert compartment.notes == "bla bla bla"
    for name, expected in zip(compartment.names, ["cytosol", "cytoplasm"]):
        assert name.namespace.prefix == "go"
        assert name.name == expected
    for ann, expected in zip(compartment.annotation, [("is", "GO:0005737")]):
        assert ann.namespace.prefix == "go"
        assert (ann.biology_qualifier.qualifier, ann.identifier) == expected
