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


from typing import Dict

from ..io import CompoundModel
from ..orm import (
    BiologyQualifier,
    Compound,
    CompoundAnnotation,
    CompoundName,
    Namespace,
)


class CompoundSerializer:
    """Define a compound serializer."""

    def __init__(
        self,
        session,
        biology_qualifiers: Dict[str, BiologyQualifier],
        namespaces: Dict[str, Namespace],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.session = session
        self.biology_qualifiers = biology_qualifiers
        self.namespaces = namespaces

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
        annotation = {}
        for ann in compound.annotation:
            annotation.setdefault(ann.namespace.prefix, []).append(
                (ann.biology_qualifier.qualifier, ann.identifier)
            )
        annotation["inchi"] = [("is", compound.inchi)]
        annotation["inchikey"] = [("is", compound.inchi_key)]
        # SMILES are not yet Identifiers.org conform.
        annotation["smiles"] = [("is", compound.smiles)]
        return CompoundModel(
            id=str(compound.id),
            notes=compound.notes,
            charge=compound.charge,
            chemicalFormula=compound.chemical_formula,
            names=[n.name for n in compound.names],
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
        for structure in ["inchi", "inchikey", "smiles"]:
            if structure in compound.annotation:
                # Set the structure and remove it from the annotations for later use.
                setattr(cmpnd, structure, compound.annotation.pop(structure)[0][1])
        for name in compound.names:
            cmpnd.names.append(CompoundName(name=name))
        for prefix, annotations in compound.annotation.items():
            namespace = self.namespaces[prefix]
            for ann in annotations:
                qualifier = self.biology_qualifiers[ann[0]]
                cmpnd.annotation.append(
                    CompoundAnnotation(
                        identifier=ann[1],
                        biology_qualifier=qualifier,
                        namespace=namespace,
                    )
                )
        return cmpnd
