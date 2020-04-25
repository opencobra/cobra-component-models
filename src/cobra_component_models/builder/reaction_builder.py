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


"""Provide a reaction builder."""


from typing import Dict, List, Optional, Tuple

from ..io import ParticipantModel, ReactionModel
from ..orm import (
    Compartment,
    Compound,
    Participant,
    Reaction,
    ReactionAnnotation,
    ReactionName,
)
from .abstract_builder import AbstractBuilder


class ReactionBuilder(AbstractBuilder):
    """Define a reaction builder."""

    def __init__(
        self,
        compartment2id: Optional[Dict[Compartment, str]] = None,
        compound2id: Optional[Dict[Compound, str]] = None,
        id2compartment: Optional[Dict[str, Compartment]] = None,
        id2compound: Optional[Dict[str, Compound]] = None,
        **kwargs
    ):
        """
        Initialize a reaction builder.

        Parameters
        ----------
        compartment2id : dict
            A map from compartment database instances to string identifiers for them.
            Needed for serialization only.
        compound2id : dict
            A map from compound database instances to string identifiers for them.
            Needed for serialization only.
        id2compartment : dict
            A map from string identifiers to compartment database instances.
            Needed for deserialization only.
        id2compound : dict
            A map from string identifiers to compound database instances.
            Needed for deserialization only.

        Other Parameters
        ----------------
        kwargs
            Passed on to super class init method.

        """
        super().__init__(**kwargs)
        self.compartment2id = {} if compartment2id is None else compartment2id
        self.compound2id = {} if compound2id is None else compound2id
        self.id2compartment = {} if id2compartment is None else id2compartment
        self.id2compound = {} if id2compound is None else id2compound

    def build_io(self, orm_model: Reaction) -> ReactionModel:
        """
        Build an IO reaction model from an ORM reaction model.

        Parameters
        ----------
        orm_model : cobra_component_models.orm.Reaction
            The reaction ORM model instance to be serialized.

        Returns
        -------
        cobra_component_models.io.ReactionModel
            A corresponding pydantic reaction data model.

        Warnings
        --------
        Please ensure that all relationships of the reaction object have been eagerly
        loaded in order to avoid :math:`N+1` [R1]_ problems that may easily occur here.

        References
        ----------
        .. [R1] https://docs.sqlalchemy.org/en/13/glossary.html#term-n-plus-one-problem

        """
        names = self.build_io_names(orm_model.names)
        annotation = self.build_io_annotation(orm_model.annotation)
        reactants, products = self.build_io_participants(orm_model.participants)
        return ReactionModel(
            id=str(orm_model.id),
            notes=orm_model.notes,
            names=names,
            annotation=annotation,
            reactants=reactants,
            products=products,
        )

    def build_io_participants(
        self, participants: List[Participant]
    ) -> Tuple[Dict[str, ParticipantModel], Dict[str, ParticipantModel]]:
        """Build the IO model reactants and products."""
        reactants = {}
        products = {}
        for part in participants:
            if part.is_product:
                products[self.compound2id[part.compound]] = ParticipantModel(
                    stoichiometry=part.stoichiometry,
                    compartment=self.compartment2id[part.compartment],
                )
            else:
                reactants[self.compound2id[part.compound]] = ParticipantModel(
                    stoichiometry=part.stoichiometry,
                    compartment=self.compartment2id[part.compartment],
                )
        return reactants, products

    def build_orm(self, data_model: ReactionModel) -> Reaction:
        """
        Build an ORM reaction model from an IO reaction model.

        Parameters
        ----------
        data_model : cobra_component_models.io.ReactionModel
            The pydantic reaction data model instance to be deserialized.

        Returns
        -------
        cobra_component_models.orm.Reaction
            A corresponding reaction ORM model.

        """
        reaction = Reaction(notes=data_model.notes)
        reaction.names.extend(self.build_orm_names(data_model.names, ReactionName))
        reaction.annotation.extend(
            self.build_orm_annotation(data_model.annotation, ReactionAnnotation)
        )
        reaction.participants.extend(
            self.build_orm_participants(
                reactants=data_model.reactants, products=data_model.products
            )
        )
        return reaction

    def build_orm_participants(
        self,
        reactants: Dict[str, ParticipantModel],
        products: Dict[str, ParticipantModel],
    ) -> List[Participant]:
        """Build the ORM model reactants and products."""
        participants = []
        for compound_id, part in reactants.items():
            participants.append(
                Participant(
                    compound=self.id2compound[compound_id],
                    compartment=self.id2compartment[part.compartment],
                    stoichiometry=part.stoichiometry,
                    is_product=False,
                )
            )
        for compound_id, part in products.items():
            participants.append(
                Participant(
                    compound=self.id2compound[compound_id],
                    compartment=self.id2compartment[part.compartment],
                    stoichiometry=part.stoichiometry,
                    is_product=True,
                )
            )
        return participants
