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


"""Provide a compartment annotation ORM model."""


from sqlalchemy import Column, ForeignKey, Integer

from .base import Base
from .mixin import AnnotationMixin


class CompartmentAnnotation(AnnotationMixin, Base):
    """
    Define a compartment annotation ORM model.

    Attributes
    ----------
    compartment_id : int
        The compartment being annotated.

    """

    __tablename__ = "compartment_annotations"

    compartment_id: int = Column(Integer, ForeignKey("compartments.id"), nullable=False)

    def __repr__(self):
        """Return a string representation of the object."""
        return (
            f"{type(self).__name__}(compartment={self.compartment_id}, "
            f"identifier={self.identifier}, "
            f"namespace={self.namespace_id}, "
            f"qualifier={self.qualifier_id})"
        )
