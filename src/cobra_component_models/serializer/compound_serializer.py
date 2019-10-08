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
from ..orm import BiologyQualifier, Compound, Namespace


class CompoundSerializer:
    """Define a compound serializer."""

    def __init__(self, session, **kwargs):
        super().__init__(**kwargs)
        self.session = session
        self.biology_qualifiers = BiologyQualifier.get_map(session)
        self.namespaces = Namespace.get_map(session)

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
                (ann.qualifier.qualifier, ann.identifier)
            )
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
        self.biology_qualifiers
        self.namespaces
        return Compound(**compound.dict())
