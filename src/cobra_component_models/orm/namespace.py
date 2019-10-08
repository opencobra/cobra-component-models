# The MIT License (MIT)
#
# Copyright (c) 2019, Moritz E. Beber.
# Copyright (c) 2018 Institute for Molecular Systems Biology, ETH Zurich.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Provide a MIRIAM compliant Identifiers.org namespace ORM model."""


from __future__ import annotations

import re
from typing import ClassVar, Dict, Optional, Pattern

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import reconstructor, validates

from .base import Base


class Namespace(Base):
    r"""
    Define a MIRIAM compliant Identifiers.org namespace ORM model.

    Attributes
    ----------
    miriam_id : str
        The MIRIAM namespace identifier for itself, e.g., MIR:00000567.
    prefix : str
        The MIRIAM namespace prefix, e.g., 'metanetx.chemical'.
    pattern : str
        The regular expression pattern to validate against identifiers in the
        namespace, e.g., ``^(MNXM\d+|BIOMASS)$``.
    embedded_prefix : bool
        Whether or not identifiers of this namespace have an embedded `prefix`, e.g.,
        'CHEBI:52971'.
    name : str, optional
        The namespace's common name.
    description : str, optional
        A short description of the namespace.

    """

    __tablename__ = "namespaces"

    miriam_id: str = Column(String(12), nullable=False, index=True, unique=True)
    # The currently longest prefix on Identifiers.org is 22.
    prefix: str = Column(String(22), nullable=False, index=True, unique=True)
    pattern: str = Column(String, nullable=False)
    embedded_prefix: bool = Column(Boolean, default=False, nullable=False)
    name: Optional[str] = Column(String, nullable=True)
    description: Optional[str] = Column(String, nullable=True)

    # Define normal Python class variables.
    _identifier_pattern: ClassVar[Pattern] = re.compile(r"^MIR:\d{8}$")

    def __init__(self, **kwargs):
        """
        Initialize a namespace object.

        While defining an init method is usually not necessary for SQLAlchemy
        declarative models, we do it here to insert the `compiled_pattern` attribute.

        """
        super().__init__(**kwargs)
        self.compiled_pattern = re.compile(self.pattern)

    def __repr__(self):
        """Return a string representation of the object."""
        return f"{type(self).__name__}(prefix={self.prefix})"

    @reconstructor
    def init_on_load(self):
        """Compile the identifier pattern on load from database."""
        self.compiled_pattern = re.compile(self.pattern)

    @validates("miriam_id")
    def validate_identifier(self, _, miriam_id: str) -> str:
        """Validate the MIRIAM identifier against the pattern."""
        if self._identifier_pattern.match(miriam_id) is None:
            raise ValueError(
                f"The namespace's identifier '{miriam_id}' does not match the "
                f"official pattern '^MIR:\\d{8}$'."
            )
        return miriam_id

    @classmethod
    def get_map(cls, session) -> Dict[str, Namespace]:
        """Extract a mapping from namespace prefix to ORM instances."""
        return {ns.prefix: ns for ns in session.query(cls)}
