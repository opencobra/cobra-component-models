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


"""Provide a compartment serializer."""


from ..io import CompartmentModel
from ..orm import Compartment, CompartmentAnnotation, CompartmentName
from .abstract_serializer import AbstractSerializer


class CompartmentSerializer(AbstractSerializer):
    """Define a compartment serializer."""

    def __init__(self, **kwargs):
        """Initialize a compartment serializer."""
        super().__init__(**kwargs)

    def serialize(self, component: Compartment) -> CompartmentModel:
        """
        Serialize a compartment ORM model to a pydantic data model.

        Parameters
        ----------
        component : cobra_component_models.orm.Compartment
            The compartment ORM model instance to be serialized.

        Returns
        -------
        cobra_component_models.io.CompartmentModel
            A corresponding pydantic compartment data model.

        Warnings
        --------
        Please ensure that all relationships of the compartment object have been eagerly
        loaded in order to avoid :math:`N+1` [CC1]_ problems that may easily occur here.

        References
        ----------
        .. [CC1] https://docs.sqlalchemy.org/en/13/glossary.html#term-n-plus-one-problem

        """
        names = self.serialize_names(component.names)
        annotation = self.serialize_annotation(component.annotation)
        return CompartmentModel(
            id=str(component.id),
            notes=component.notes,
            names=names,
            annotation=annotation,
        )

    def deserialize(self, component_model: CompartmentModel) -> Compartment:
        """
        Deserialize a pydantic compartment data model to an ORM model.

        Parameters
        ----------
        component_model : cobra_component_models.io.CompartmentModel
            The pydantic compartment data model instance to be deserialized.

        Returns
        -------
        cobra_component_models.orm.Compartment
            A corresponding compartment ORM model.

        """
        compartment = Compartment(notes=component_model.notes)
        compartment.names.extend(
            self.deserialize_names(component_model.names, CompartmentName)
        )
        compartment.annotation.extend(
            self.deserialize_annotation(
                component_model.annotation, CompartmentAnnotation
            )
        )
        return compartment
