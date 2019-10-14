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
        """Initialize a compound serializer."""
        super().__init__(**kwargs)

    def serialize(self, component: Compound) -> CompoundModel:
        """
        Serialize a compound ORM model to a pydantic data model.

        Parameters
        ----------
        component : cobra_component_models.orm.Compound
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
        names = self.serialize_names(component.names)
        annotation = self.serialize_annotation(component.annotation)
        annotation["inchi"] = [("is", component.inchi)]
        annotation["inchikey"] = [("is", component.inchi_key)]
        # SMILES are not yet Identifiers.org conform.
        annotation["smiles"] = [("is", component.smiles)]
        return CompoundModel(
            id=str(component.id),
            notes=component.notes,
            charge=component.charge,
            chemicalFormula=component.chemical_formula,
            names=names,
            annotation=annotation,
        )

    def deserialize(self, component_model: CompoundModel) -> Compound:
        """
        Deserialize a pydantic compound data model to an ORM model.

        Parameters
        ----------
        component_model : cobra_component_models.io.CompoundModel
            The pydantic compound data model instance to be deserialized.

        Returns
        -------
        cobra_component_models.orm.Compound
            A corresponding compound ORM model.

        """
        compound = Compound(
            charge=component_model.charge,
            chemical_formula=component_model.chemical_formula,
            notes=component_model.notes,
        )
        for structure in ["inchi", "smiles"]:
            if structure in component_model.annotation:
                # Set the structure and remove it from the annotations for later use.
                setattr(
                    compound, structure, component_model.annotation.pop(structure)[0][1]
                )
        if "inchikey" in component_model.annotation:
            compound.inchi_key = component_model.annotation.pop("inchikey")[0][1]
        compound.names.extend(
            self.deserialize_names(component_model.names, CompoundName)
        )
        compound.annotation.extend(
            self.deserialize_annotation(component_model.annotation, CompoundAnnotation)
        )
        return compound
