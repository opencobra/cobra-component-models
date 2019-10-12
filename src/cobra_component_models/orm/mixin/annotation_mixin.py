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


"""Provide a component annotation mixin with the corresponding ORM columns."""


import logging

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


logger = logging.getLogger(__name__)


class AnnotationMixin:
    """
    Define a component annotation mixin.

    Attributes
    ----------
    identifier : str
        The annotation identifier.
    namespace_id : int
        The foreign key of the related Identifiers.org namespace.
    qualifier_id : int
        The foreign key of the related biology qualifier.

    """

    identifier: str = Column(String, nullable=False, index=True)

    @declared_attr
    def namespace_id(cls):
        """Defer the namespace id field instantiation."""
        return Column(Integer, ForeignKey("namespaces.id"), nullable=False)

    @declared_attr
    def namespace(cls):
        """Defer the namespace field instantiation."""
        return relationship("Namespace")

    @declared_attr
    def biology_qualifier_id(cls):
        """Defer the biology qualifier id field instantiation."""
        return Column(Integer, ForeignKey("biology_qualifiers.id"), nullable=False)

    @declared_attr
    def biology_qualifier(cls):
        """Defer the biology qualifier field instantiation."""
        return relationship("BiologyQualifier")

    # FIXME: The namespace attribute is not initialized at the time of validation.
    #  Try to use events maybe
    #  (https://docs.sqlalchemy.org/en/13/orm/events.html#attribute-events)?
    # @validates("identifier")
    # def validate_identifier(self, _, identifier: str):
    #     """Use the namespace's pattern to validate the identifier."""
    #     if self.namespace.compiled_pattern.match(identifier) is None:
    #         logger.warning(
    #             f"Identifier '{identifier}' does not match "
    #             f"{self.namespace.name}'s pattern '{self.namespace.pattern}'."
    #         )
    #     return identifier
