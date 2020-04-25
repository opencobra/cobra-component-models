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


"""Provide a compartment builder."""


from ..io import CompartmentModel
from ..orm import Compartment, CompartmentAnnotation, CompartmentName
from .abstract_builder import AbstractBuilder


class CompartmentBuilder(AbstractBuilder):
    """Define a compartment builder."""

    def __init__(self, **kwargs):
        """Initialize a compartment builder."""
        super().__init__(**kwargs)

    def build_io(self, orm_model: Compartment) -> CompartmentModel:
        """
        Build an IO compartment model from an ORM compartment model.

        Parameters
        ----------
        orm_model : cobra_component_models.orm.Compartment
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
        names = self.build_io_names(orm_model.names)
        annotation = self.build_io_annotation(orm_model.annotation)
        return CompartmentModel(
            id=str(orm_model.id),
            notes=orm_model.notes,
            names=names,
            annotation=annotation,
        )

    def build_orm(self, data_model: CompartmentModel) -> Compartment:
        """
        Build an ORM compartment model from an IO compartment model.

        Parameters
        ----------
        data_model : cobra_component_models.io.CompartmentModel
            The pydantic compartment data model instance to be deserialized.

        Returns
        -------
        cobra_component_models.orm.Compartment
            A corresponding compartment ORM model.

        """
        compartment = Compartment(notes=data_model.notes)
        compartment.names.extend(
            self.build_orm_names(data_model.names, CompartmentName)
        )
        compartment.annotation.extend(
            self.build_orm_annotation(data_model.annotation, CompartmentAnnotation)
        )
        return compartment
