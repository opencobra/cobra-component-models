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


"""Provide an abstract builder."""


from abc import ABC, abstractmethod
from typing import Dict, List, Type

from ..io import AbstractBaseModel, AnnotationModel, NameModel
from ..orm import (
    AbstractComponent,
    AbstractComponentAnnotation,
    AbstractComponentName,
    Namespace,
)


class AbstractBuilder(ABC):
    """Define an abstract builder."""

    def __init__(self, *, namespaces: Dict[str, Namespace], **kwargs):
        """
        Initialize the abstract base builder.

        Parameters
        ----------
        namespaces : dict
            A mapping from namespace prefixes to their database instances.

        Other Parameters
        ----------------
        kwargs
            Passed on to super class init method.

        """
        super().__init__(**kwargs)
        self.namespaces = namespaces

    @abstractmethod
    def build_io(self, orm_model: AbstractComponent) -> AbstractBaseModel:
        """Build an IO model from an ORM model."""
        raise NotImplementedError()  # pragma: no cover

    def build_io_names(
        self, names: List[AbstractComponentName]
    ) -> Dict[str, List[NameModel]]:
        """Build IO model names from ORM names."""
        obj = {}
        for name in names:
            obj.setdefault(name.namespace.prefix, []).append(
                NameModel(name=name.name, is_preferred=name.is_preferred)
            )
        return obj

    def build_io_annotation(
        self,
        annotation: List[AbstractComponentAnnotation],
    ) -> Dict[str, List[AnnotationModel]]:
        """Build IO model annotation from ORM annotation."""
        obj = {}
        for ann in annotation:
            obj.setdefault(ann.namespace.prefix, []).append(
                AnnotationModel(
                    identifier=ann.identifier,
                    is_deprecated=ann.is_deprecated,
                )
            )
        return obj

    @abstractmethod
    def build_orm(self, data_model: AbstractBaseModel) -> AbstractComponent:
        """Build an ORM model from an IO model."""
        raise NotImplementedError()  # pragma: no cover

    def build_orm_names(
        self, names_data: Dict[str, List[NameModel]], cls: Type[AbstractComponentName]
    ) -> List[AbstractComponentName]:
        """Build ORM model names from IO names."""
        result = []
        for prefix, names in names_data.items():
            namespace = self.namespaces[prefix]
            for name in names:
                result.append(
                    cls(
                        name=name.name,
                        namespace=namespace,
                        is_preferred=name.is_preferred,
                    )
                )
        return result

    def build_orm_annotation(
        self,
        annotation_data: Dict[str, List[AnnotationModel]],
        cls: Type[AbstractComponentAnnotation],
    ) -> List[AbstractComponentAnnotation]:
        """Build ORM annotation names from IO annotation."""
        result = []
        for prefix, annotations in annotation_data.items():
            namespace = self.namespaces[prefix]
            for ann in annotations:
                result.append(
                    cls(
                        identifier=ann.identifier,
                        is_deprecated=ann.is_deprecated,
                        namespace=namespace,
                    )
                )
        return result
