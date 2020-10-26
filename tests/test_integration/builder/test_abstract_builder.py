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


"""Expect that names and annotation IO & ORM models can be built."""


from typing import Dict, Type

import pytest

from cobra_component_models.builder import AbstractBuilder
from cobra_component_models.io import AbstractBaseModel, AnnotationModel, NameModel
from cobra_component_models.orm import (
    AbstractComponent,
    AbstractComponentAnnotation,
    AbstractComponentName,
    BiologyQualifier,
    CompartmentAnnotation,
    CompartmentName,
    CompoundAnnotation,
    CompoundName,
    Namespace,
    ReactionAnnotation,
    ReactionName,
)


class MockBuilder(AbstractBuilder):
    """Define a mock concrete builder."""

    def build_io(self, orm_model: AbstractComponent) -> AbstractBaseModel:
        """Define a concrete method implementation."""
        pass

    def build_orm(self, data_model: AbstractBaseModel) -> AbstractComponent:
        """Define a concrete method implementation."""
        pass


def test_init(session):
    """Expect that a direct child can be initialized."""
    MockBuilder(namespaces={}, biology_qualifiers={})


@pytest.mark.parametrize("cls", [CompartmentName, CompoundName, ReactionName])
def test_build_io_names(namespaces, cls: Type[AbstractComponentName]):
    """Expect that IO names are built correctly."""
    chebi = namespaces["chebi"]
    orm_names = [
        cls(name=n, namespace=chebi) for n in ("ethanol", "Aethanol", "Alkohol")
    ]
    io_names = MockBuilder(namespaces={}, biology_qualifiers={}).build_io_names(
        orm_names
    )
    assert {n.name for n in io_names["chebi"]} == {"ethanol", "Aethanol", "Alkohol"}


@pytest.mark.parametrize(
    "cls", [CompartmentAnnotation, CompoundAnnotation, ReactionAnnotation]
)
def test_build_io_annotation(
    biology_qualifiers: Dict[str, BiologyQualifier],
    namespaces: Dict[str, Namespace],
    cls: Type[AbstractComponentAnnotation],
):
    """Expect that component annotation is serialized correctly."""
    chebi = namespaces["chebi"]
    qual = biology_qualifiers["is"]
    orm_annotation = [
        cls(identifier=i, namespace=chebi, biology_qualifier=qual)
        for i in ("CHEBI:16236", "CHEBI:44594", "CHEBI:42377")
    ]
    io_annotation = MockBuilder(
        namespaces={}, biology_qualifiers={}
    ).build_io_annotation(orm_annotation)
    assert {a.identifier for a in io_annotation["chebi"]} == {
        "CHEBI:16236",
        "CHEBI:44594",
        "CHEBI:42377",
    }


@pytest.mark.parametrize("cls", [CompartmentName, CompoundName, ReactionName])
def test_build_orm_names(
    biology_qualifiers, namespaces, cls: Type[AbstractComponentName]
):
    """Expect that component names are deserialized correctly."""
    obj = {
        "chebi": [
            NameModel(name="ethanol"),
            NameModel(name="Aethanol"),
            NameModel(name="Alkohol"),
        ]
    }
    names = MockBuilder(
        biology_qualifiers=biology_qualifiers, namespaces=namespaces
    ).build_orm_names(obj, cls)
    for name, expected in zip(names, ["ethanol", "Aethanol", "Alkohol"]):
        assert name.namespace.prefix == "chebi"
        assert name.name == expected
        assert name.is_preferred is False


@pytest.mark.parametrize(
    "cls", [CompartmentAnnotation, CompoundAnnotation, ReactionAnnotation]
)
def test_deserialize_annotation(
    biology_qualifiers, namespaces, cls: Type[AbstractComponentAnnotation]
):
    """Expect that component annotation is deserialized correctly."""
    obj = {
        "chebi": [
            AnnotationModel(
                identifier="CHEBI:16236",
                biology_qualifier="is",
            ),
            AnnotationModel(
                identifier="CHEBI:44594",
                biology_qualifier="is",
            ),
            AnnotationModel(
                identifier="CHEBI:42377",
                biology_qualifier="is",
            ),
        ]
    }
    annotation = MockBuilder(
        biology_qualifiers=biology_qualifiers, namespaces=namespaces
    ).build_orm_annotation(obj, cls)
    for ann, expected in zip(
        annotation,
        ("CHEBI:16236", "CHEBI:44594", "CHEBI:42377"),
    ):
        assert ann.namespace.prefix == "chebi"
        assert ann.biology_qualifier.qualifier == "is"
        assert ann.identifier == expected
        assert ann.is_deprecated is False
