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


from typing import Type

import pytest

from cobra_component_models.io import SBaseModel
from cobra_component_models.orm import (
    AbstractComponent,
    AbstractComponentAnnotation,
    AbstractComponentName,
    CompartmentAnnotation,
    CompartmentName,
    CompoundAnnotation,
    CompoundName,
    ReactionAnnotation,
    ReactionName,
)
from cobra_component_models.serializer import AbstractSerializer


class DummySerializer(AbstractSerializer):
    """Define a barebones concrete serializer."""

    def serialize(self, orm_model: AbstractComponent) -> SBaseModel:
        """Define a concrete method implementation."""
        pass

    def deserialize(self, data_model: SBaseModel) -> AbstractComponent:
        """Define a concrete method implementation."""
        pass


def test_init(session):
    """Expect that a direct child can be initialized."""
    DummySerializer(namespaces={}, biology_qualifiers={})


@pytest.mark.parametrize("name_class", [CompartmentName, CompoundName, ReactionName])
def test_serialize_names(namespaces, name_class: Type[AbstractComponentName]):
    """Expect that component names are serialized correctly."""
    chebi = namespaces["chebi"]
    names = [
        name_class(name=n, namespace=chebi) for n in ["ethanol", "Aethanol", "Alkohol"]
    ]
    serialized = DummySerializer(namespaces={}, biology_qualifiers={}).serialize_names(
        names
    )
    assert serialized == {"chebi": ["ethanol", "Aethanol", "Alkohol"]}


@pytest.mark.parametrize(
    "annotation_class", [CompartmentAnnotation, CompoundAnnotation, ReactionAnnotation]
)
def test_serialize_annotation(
    biology_qualifiers, namespaces, annotation_class: Type[AbstractComponentAnnotation]
):
    """Expect that component annotation is serialized correctly."""
    chebi = namespaces["chebi"]
    qual = biology_qualifiers["is"]
    annotation = [
        annotation_class(identifier=i, namespace=chebi, biology_qualifier=qual)
        for i in ["CHEBI:16236", "CHEBI:44594", "CHEBI:42377"]
    ]
    serialized = DummySerializer(
        namespaces={}, biology_qualifiers={}
    ).serialize_annotation(annotation)
    assert serialized == {
        "chebi": [("is", "CHEBI:16236"), ("is", "CHEBI:44594"), ("is", "CHEBI:42377")]
    }


@pytest.mark.parametrize("name_class", [CompartmentName, CompoundName, ReactionName])
def test_deserialize_names(
    biology_qualifiers, namespaces, name_class: Type[AbstractComponentName]
):
    """Expect that component names are deserialized correctly."""
    obj = {"chebi": ["ethanol", "Aethanol", "Alkohol"]}
    names = DummySerializer(
        biology_qualifiers=biology_qualifiers, namespaces=namespaces
    ).deserialize_names(obj, name_class)
    for name, expected in zip(names, ["ethanol", "Aethanol", "Alkohol"]):
        assert name.namespace.prefix == "chebi"
        assert name.name == expected


@pytest.mark.parametrize(
    "annotation_class", [CompartmentAnnotation, CompoundAnnotation, ReactionAnnotation]
)
def test_deserialize_annotation(
    biology_qualifiers, namespaces, annotation_class: Type[AbstractComponentAnnotation]
):
    """Expect that component annotation is deserialized correctly."""
    obj = {
        "chebi": [["is", "CHEBI:16236"], ["is", "CHEBI:44594"], ["is", "CHEBI:42377"]]
    }
    annotation = DummySerializer(
        biology_qualifiers=biology_qualifiers, namespaces=namespaces
    ).deserialize_annotation(obj, annotation_class)
    for ann, expected in zip(
        annotation,
        [("is", "CHEBI:16236"), ("is", "CHEBI:44594"), ("is", "CHEBI:42377")],
    ):
        assert ann.namespace.prefix == "chebi"
        assert (ann.biology_qualifier.qualifier, ann.identifier) == expected
