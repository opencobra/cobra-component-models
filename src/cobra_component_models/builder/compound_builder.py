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


"""Provide a compound builder."""


from ..io import AnnotationModel, CompoundModel
from ..orm import Compound, CompoundAnnotation, CompoundName
from .abstract_builder import AbstractBuilder


class CompoundBuilder(AbstractBuilder):
    """Define a compound builder."""

    def __init__(self, **kwargs):
        """Initialize a compound builder."""
        super().__init__(**kwargs)

    def build_io(self, orm_model: Compound) -> CompoundModel:
        """
        Build an IO compound model from an ORM compound model.

        Parameters
        ----------
        orm_model : cobra_component_models.orm.Compound
            The compound ORM model instance to be serialized.

        Returns
        -------
        cobra_component_models.io.CompoundModel
            A corresponding pydantic compound data model.

        Warnings
        --------
        Please ensure that all relationships of the compound object have been eagerly
        loaded in order to avoid :math:`N+1` [C1]_ problems that may easily occur here.

        References
        ----------
        .. [C1] https://docs.sqlalchemy.org/en/13/glossary.html#term-n-plus-one-problem

        """
        names = self.build_io_names(orm_model.names)
        annotation = self.build_io_annotation(orm_model.annotation)
        if orm_model.inchi:
            annotation["inchi"] = [AnnotationModel(identifier=orm_model.inchi)]
        if orm_model.inchi_key:
            annotation["inchikey"] = [AnnotationModel(identifier=orm_model.inchi_key)]
        if orm_model.smiles:
            # SMILES are not yet Identifiers.org conform.
            annotation["smiles"] = [AnnotationModel(identifier=orm_model.smiles)]
        return CompoundModel(
            id=str(orm_model.id),
            notes=orm_model.notes,
            charge=orm_model.charge,
            chemical_formula=orm_model.chemical_formula,
            names=names,
            annotation=annotation,
        )

    def build_orm(self, data_model: CompoundModel) -> Compound:
        """
        Build an ORM compound model from an IO compound model.

        Parameters
        ----------
        data_model : cobra_component_models.io.CompoundModel
            The pydantic compound data model instance to be deserialized.

        Returns
        -------
        cobra_component_models.orm.Compound
            A corresponding compound ORM model.

        """
        compound = Compound(
            charge=data_model.charge,
            chemical_formula=data_model.chemical_formula,
            notes=data_model.notes,
        )
        # We want to remove elements from the annotation dictionary so that they are
        # not used in building the normal annotation but without modifying the data
        # model.
        annotation = data_model.annotation.copy()
        if "inchi" in annotation:
            # We expect a single element in the list of annotation.
            (inchi,) = annotation.pop("inchi")
            compound.inchi = inchi.identifier
        if "inchikey" in annotation:
            # We expect a single element in the list of annotation.
            (inchi_key,) = annotation.pop("inchikey")
            compound.inchi_key = inchi_key.identifier
        if "smiles" in annotation:
            # We expect a single element in the list of annotation.
            (smiles,) = annotation.pop("smiles")
            compound.smiles = smiles.identifier
        compound.names.extend(self.build_orm_names(data_model.names, CompoundName))
        compound.annotation.extend(
            self.build_orm_annotation(annotation, CompoundAnnotation)
        )
        return compound
