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


"""Provide abstract base components."""


from abc import ABC
from typing import List

from .compartment import Compartment
from .compartment_annotation import CompartmentAnnotation
from .compartment_name import CompartmentName
from .compound import Compound
from .compound_annotation import CompoundAnnotation
from .compound_name import CompoundName
from .namespace import Namespace
from .reaction import Reaction
from .reaction_annotation import ReactionAnnotation
from .reaction_name import ReactionName


class AbstractComponentAnnotation(ABC):
    """Define an abstract base for component annotation."""

    def __init__(
        self,
        *,
        identifier: str,
        namespace: Namespace,
        is_deprecated: bool = False,
        **kwargs
    ) -> None:  # pragma: no cover
        """Define the attributes for the abstract class."""
        super().__init__(**kwargs)
        self.identifier = identifier
        self.namespace = namespace
        self.is_deprecated = is_deprecated


class AbstractComponentName(ABC):
    """Define an abstract base for component names."""

    def __init__(
        self, *, name: str, namespace: Namespace, is_preferred: bool = False, **kwargs
    ) -> None:  # pragma: no cover
        """Define the attributes for the abstract class."""
        super().__init__(**kwargs)
        self.name = name
        self.namespace = namespace
        self.is_preferred = is_preferred


class AbstractComponent(ABC):
    """Define an abstract base component."""

    def __init__(
        self,
        *,
        names: List[AbstractComponentName],
        annotation: List[AbstractComponentAnnotation],
        **kwargs
    ) -> None:  # pragma: no cover
        """Define the attributes for the abstract class."""
        super().__init__(**kwargs)
        self.names = names
        self.annotation = annotation


AbstractComponent.register(Compartment)
AbstractComponent.register(Compound)
AbstractComponent.register(Reaction)
AbstractComponentAnnotation.register(CompartmentAnnotation)
AbstractComponentAnnotation.register(CompoundAnnotation)
AbstractComponentAnnotation.register(ReactionAnnotation)
AbstractComponentName.register(CompartmentName)
AbstractComponentName.register(CompoundName)
AbstractComponentName.register(ReactionName)
