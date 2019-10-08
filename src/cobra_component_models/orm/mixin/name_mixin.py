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


"""Provide a component name mixin with the corresponding ORM columns."""


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


class NameMixin:
    """
    Define a component name mixin.

    Attributes
    ----------
    name : str
        A common name for a component.
    namespace_id : int
        The foreign key of the related Identifiers.org namespace.

    """

    name: str = Column(String, nullable=False, index=True)

    @declared_attr
    def namespace_id(cls):
        """Defer the namespace id field instantiation."""
        return Column(Integer, ForeignKey("namespaces.id"), nullable=False)

    @declared_attr
    def namespace(cls):
        """Defer the namespace field instantiation."""
        return relationship("Namespace")
