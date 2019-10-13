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


"""Provide a compound serializer."""


from ..io import CompoundModel
from ..orm import Compound, CompoundAnnotation, CompoundName
from .abstract_serializer import AbstractSerializer


class CompoundSerializer(AbstractSerializer):
    """Define a compound serializer."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self, compound: Compound) -> CompoundModel:
        """
        Serialize a compound ORM model to a pydantic data model.

        Parameters
        ----------
        compound : cobra_component_models.orm.Compound
            The compound ORM model instance to be serialized.

        Returns
        -------
        cobra_component_models.io.CompoundModel
            A corresponding pydantic compound data model.

        Warnings
        --------
        Please ensure that all relationships of the compound object have been eagerly
        loaded in order to avoid N+1 [1]_ problems that may easily occur here.

        References
        ----------
        .. [1] https://docs.sqlalchemy.org/en/13/glossary.html#term-n-plus-one-problem

        """
        names = self.serialize_names(compound.names)
        annotation = self.serialize_annotation(compound.annotation)
        annotation["inchi"] = [("is", compound.inchi)]
        annotation["inchikey"] = [("is", compound.inchi_key)]
        # SMILES are not yet Identifiers.org conform.
        annotation["smiles"] = [("is", compound.smiles)]
        return CompoundModel(
            id=str(compound.id),
            notes=compound.notes,
            charge=compound.charge,
            chemicalFormula=compound.chemical_formula,
            names=names,
            annotation=annotation,
        )

    def deserialize(self, compound: CompoundModel) -> Compound:
        """
        Deserialize a pydantic compound data model to an ORM model.

        Parameters
        ----------
        compound : cobra_component_models.io.CompoundModel
            The pydantic compound data model instance to be deserialized.

        Returns
        -------
        cobra_component_models.orm.Compound
            A corresponding compound ORM model.

        """
        cmpnd = Compound(
            charge=compound.charge,
            chemical_formula=compound.chemical_formula,
            notes=compound.notes,
        )
        for structure in ["inchi", "smiles"]:
            if structure in compound.annotation:
                # Set the structure and remove it from the annotations for later use.
                setattr(cmpnd, structure, compound.annotation.pop(structure)[0][1])
        if "inchikey" in compound.annotation:
            setattr(cmpnd, "inchi_key", compound.annotation.pop("inchikey")[0][1])
        cmpnd.names.extend(self.deserialize_names(compound.names, CompoundName))
        cmpnd.annotation.extend(
            self.deserialize_annotation(compound.annotation, CompoundAnnotation)
        )
        return cmpnd
