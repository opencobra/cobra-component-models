# Copyright (c) 2019, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide an abstract serializer."""


from abc import ABC, abstractmethod
from typing import Dict, List, Type

from ..io import SBaseModel
from ..io.type import AnnotationType
from ..orm import (
    AbstractComponent,
    AbstractComponentAnnotation,
    AbstractComponentName,
    BiologyQualifier,
    Namespace,
)


class AbstractSerializer(ABC):
    """Define an abstract serializer."""

    def __init__(
        self,
        biology_qualifiers: Dict[str, BiologyQualifier],
        namespaces: Dict[str, Namespace],
        **kwargs
    ):
        """
        Initialize the abstract base serializer.

        Parameters
        ----------
        biology_qualifiers : dict
            A mapping from biology qualifiers to their database instances.
        namespaces : dict
            A mapping from namespace prefixes to their database instances.

        Other Parameters
        ----------------
        kwargs
            Passed on to super class init method.

        """
        super().__init__(**kwargs)
        self.biology_qualifiers = biology_qualifiers
        self.namespaces = namespaces

    @abstractmethod
    def serialize(self, component: AbstractComponent) -> SBaseModel:
        """Serialize an ORM model to a pydantic data model."""
        pass

    def serialize_names(
        self, names: List[AbstractComponentName]
    ) -> Dict[str, List[str]]:
        """Serialize the component names."""
        obj = {}
        for name_model in names:
            obj.setdefault(name_model.namespace.prefix, []).append(name_model.name)
        return obj

    def serialize_annotation(
        self, annotation: List[AbstractComponentAnnotation]
    ) -> Dict[str, List[AnnotationType]]:
        """Serialize the component annotation."""
        obj = {}
        for ann in annotation:
            obj.setdefault(ann.namespace.prefix, []).append(
                (ann.biology_qualifier.qualifier, ann.identifier)
            )
        return obj

    @abstractmethod
    def deserialize(self, component_model: SBaseModel) -> AbstractComponent:
        """Deserialize a pydantic data model to an ORM model."""
        pass

    def deserialize_names(
        self, names_data: Dict[str, List[str]], orm_class: Type[AbstractComponentName]
    ) -> List[AbstractComponentName]:
        """Deserialize the component names."""
        result = []
        for prefix, names in names_data.items():
            namespace = self.namespaces[prefix]
            for name in names:
                result.append(orm_class(name=name, namespace=namespace))
        return result

    def deserialize_annotation(
        self,
        annotation_data: Dict[str, List[AnnotationType]],
        orm_class: Type[AbstractComponentAnnotation],
    ) -> List[AbstractComponentAnnotation]:
        """Deserialize the component annotation."""
        result = []
        for prefix, annotations in annotation_data.items():
            namespace = self.namespaces[prefix]
            for ann in annotations:
                qualifier = self.biology_qualifiers[ann[0]]
                result.append(
                    orm_class(
                        identifier=ann[1],
                        biology_qualifier=qualifier,
                        namespace=namespace,
                    )
                )
        return result
