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


from cobra_component_models.builder import CompartmentBuilder
from cobra_component_models.io import CompartmentModel
from cobra_component_models.orm import (
    Compartment,
    CompartmentAnnotation,
    CompartmentName,
)


def test_build_io_default_compartment(session):
    """Expect that a default compartment can be serialized."""
    cmpd = Compartment()
    session.add(cmpd)
    session.commit()
    obj = CompartmentBuilder(namespaces={}).build_io(cmpd)
    assert obj.id == "1"


def test_build_full_io_compartment(session, namespaces):
    """Expect that a fully fleshed out compartment can be serialized."""
    compartment = Compartment(notes="bla bla bla")
    go = namespaces["go"]
    compartment.names = [
        CompartmentName(name=n, namespace=go) for n in ["cytosol", "cytoplasm"]
    ]
    compartment.annotation = [
        CompartmentAnnotation(identifier=i, namespace=go) for i in ["GO:0005737"]
    ]
    session.add(compartment)
    session.commit()
    obj = CompartmentBuilder(namespaces=namespaces).build_io(compartment)
    assert obj.id == "1"
    assert obj.notes == "bla bla bla"
    assert "go" in obj.names
    assert {n.name for n in obj.names["go"]} == {"cytosol", "cytoplasm"}
    assert {a.identifier for a in obj.annotation["go"]} == {"GO:0005737"}


def test_build_full_orm_compartment(session, namespaces):
    """Expect that a fully fleshed out compartment can be deserialized."""
    obj = CompartmentModel.parse_obj(
        {
            "id": "1",
            "notes": "bla bla bla",
            "names": {"go": [{"name": "cytosol"}, {"name": "cytoplasm"}]},
            "annotation": {"go": [{"identifier": "GO:0005737"}]},
        }
    )
    compartment = CompartmentBuilder(namespaces=namespaces).build_orm(obj)
    session.add(compartment)
    session.commit()
    assert compartment.notes == "bla bla bla"
    assert "go" in {n.namespace.prefix for n in compartment.names}
    assert {n.name for n in compartment.names} == {"cytosol", "cytoplasm"}
    for ann, expected in zip(compartment.annotation, ("GO:0005737",)):
        assert ann.namespace.prefix == "go"
        assert ann.identifier == expected
