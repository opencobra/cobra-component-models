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


"""Provide a reaction annotation ORM model."""


from sqlalchemy import Column, ForeignKey, Integer

from .base import Base
from .mixin import AnnotationMixin


class ReactionAnnotation(AnnotationMixin, Base):
    """
    Define a reaction annotation ORM model.

    Attributes
    ----------
    reaction_id : int
        The reaction being annotated.

    """

    __tablename__ = "reaction_annotations"

    reaction_id: int = Column(Integer, ForeignKey("reactions.id"), nullable=False)

    def __repr__(self):
        """Return a string representation of the object."""
        return (
            f"{type(self).__name__}(reaction={self.reaction_id}, "
            f"identifier={self.identifier}, "
            f"namespace={self.namespace_id}, "
            f"qualifier={self.qualifier_id})"
        )
