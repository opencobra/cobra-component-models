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


"""Expect that names and annotation can be de-/serialized and selected/inserted."""


from cobra_component_models.io import SBaseModel
from cobra_component_models.orm import (
    AbstractComponent,
    CompoundAnnotation,
    CompoundName,
    Namespace,
)
from cobra_component_models.serializer import AbstractSerializer


class DummySerializer(AbstractSerializer):
    pass

    def serialize(self, orm_model: AbstractComponent) -> SBaseModel:
        pass

    def deserialize(self, data_model: SBaseModel) -> AbstractComponent:
        pass


def test_init(session):
    """Expect that a direct child can be initialized."""
    DummySerializer(session=session, namespaces={}, biology_qualifiers={})


def test_serialize_names(session):
    chebi = Namespace(miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$")
    names = [
        CompoundName(name=n, namespace=chebi)
        for n in ["ethanol", "Aethanol", "Alkohol"]
    ]
    serialized = DummySerializer(
        session=session, namespaces={}, biology_qualifiers={}
    ).serialize_names(names)
    assert serialized == {"chebi": ["ethanol", "Aethanol", "Alkohol"]}


def test_serialize_annotation(session, biology_qualifiers):
    chebi = Namespace(miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$")
    qual = biology_qualifiers["is"]
    annotation = [
        CompoundAnnotation(identifier=i, namespace=chebi, biology_qualifier=qual)
        for i in ["CHEBI:16236", "CHEBI:44594", "CHEBI:42377"]
    ]
    serialized = DummySerializer(
        session=session, namespaces={}, biology_qualifiers={}
    ).serialize_annotation(annotation)
    assert serialized == {
        "chebi": [("is", "CHEBI:16236"), ("is", "CHEBI:44594"), ("is", "CHEBI:42377")]
    }


def test_deserialize_names(session, biology_qualifiers):
    # Add namespace to database so that it can be used in validation later.
    chebi = Namespace(miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$")
    session.add(chebi)
    session.commit()
    obj = {"chebi": ["ethanol", "Aethanol", "Alkohol"]}
    names = DummySerializer(
        session=session,
        biology_qualifiers=biology_qualifiers,
        namespaces=Namespace.get_map(session),
    ).deserialize_names(obj, CompoundName)
    for name, expected in zip(names, ["ethanol", "Aethanol", "Alkohol"]):
        assert name.namespace.prefix == "chebi"
        assert name.name == expected


def test_deserialize_annotation(session, biology_qualifiers):
    # Add namespace to database so that it can be used in validation later.
    chebi = Namespace(miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$")
    session.add(chebi)
    session.commit()
    obj = {
        "chebi": [["is", "CHEBI:16236"], ["is", "CHEBI:44594"], ["is", "CHEBI:42377"]]
    }
    annotation = DummySerializer(
        session=session,
        biology_qualifiers=biology_qualifiers,
        namespaces=Namespace.get_map(session),
    ).deserialize_annotation(obj, CompoundAnnotation)
    for ann, expected in zip(
        annotation,
        [("is", "CHEBI:16236"), ("is", "CHEBI:44594"), ("is", "CHEBI:42377")],
    ):
        assert ann.namespace.prefix == "chebi"
        assert (ann.biology_qualifier.qualifier, ann.identifier) == expected
