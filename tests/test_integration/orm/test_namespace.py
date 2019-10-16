# Copyright (c) 2019, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Expect that namespaces function as designed."""


import re

import pytest
from sqlalchemy.exc import IntegrityError

from cobra_component_models.orm import Namespace


@pytest.mark.parametrize(
    "attributes",
    [
        {
            "miriam_id": "MIR:00000258",
            "prefix": "combine.specifications",
            "pattern": r"^\w+(\-|\.|\w)*$",
        },
        {
            "id": 22,
            "miriam_id": "MIR:00000258",
            "prefix": "combine.specifications",
            "pattern": r"^\w+(\-|\.|\w)*$",
        },
        {
            "miriam_id": "MIR:00000258",
            "prefix": "combine.specifications",
            "pattern": r"^\w+(\-|\.|\w)*$",
            "embedded_prefix": True,
        },
        {
            "miriam_id": "MIR:00000258",
            "prefix": "combine.specifications",
            "pattern": r"^\w+(\-|\.|\w)*$",
            "name": "COMBINE specifications",
        },
        {
            "miriam_id": "MIR:00000258",
            "prefix": "combine.specifications",
            "pattern": r"^\w+(\-|\.|\w)*$",
            "description": "The 'COmputational Modeling in BIology' NEtwork (COMBINE) is an initiative to coordinate the development of the various community standards and formats for computational models, initially in Systems Biology and related fields. This collection pertains to specifications of the standard formats developed by the Computational Modeling in Biology Network.",  # noqa: E501
        },
    ],
)
def test_init(attributes):
    """Expect that an object can be instantiated with the right attributes."""
    instance = Namespace(**attributes)
    for attr, value in attributes.items():
        assert getattr(instance, attr) == value


@pytest.mark.parametrize(
    "identifier",
    [
        pytest.param(None, marks=pytest.mark.raises(exception=TypeError)),
        pytest.param("MIR:1234567", marks=pytest.mark.raises(exception=ValueError)),
        pytest.param("MIR:123456789", marks=pytest.mark.raises(exception=ValueError)),
    ],
)
def test_miriam_constraints(session, identifier):
    """Expect that the MIRIAM identifier is validated according to the pattern."""
    Namespace(
        miriam_id=identifier,
        prefix="combine.specifications",
        pattern=r"^\w+(\-|\.|\w)*$",
    )


def test_unique_miriam_id(session):
    """Expect that the same MIRIAM ID cannot be added twice to the same database."""
    ns_1 = Namespace(miriam_id="MIR:00000258", prefix="combine.spec", pattern="pattern")
    session.add(ns_1)
    session.commit()
    ns_2 = Namespace(
        miriam_id="MIR:00000258", prefix="combine.specifications", pattern="pattern"
    )
    session.add(ns_2)
    with pytest.raises(IntegrityError):
        session.commit()


def test_prefix_not_null(session):
    """Expect that the prefix cannot be null."""
    instance = Namespace(miriam_id="MIR:00000258", pattern=r"^\w+(\-|\.|\w)*$")
    session.add(instance)
    with pytest.raises(IntegrityError):
        session.commit()


@pytest.mark.xfail(
    reason="Length restriction is not implemented for in-memory SQLite.", strict=True
)
def test_prefix_cut_off(session):
    """Expect that the prefix has a maximum length of 22 characters."""
    prefix = "What a crazy long prefix. This is not allowed."
    instance = Namespace(
        prefix=prefix, miriam_id="MIR:00000258", pattern=r"^\w+(\-|\.|\w)*$"
    )
    session.add(instance)
    # FIXME: Maybe this is an integrity error instead.
    session.commit()
    loaded = session.query(Namespace).first()
    assert loaded.prefix == prefix[:22]


def test_unique_prefix(session):
    """Expect that the same prefix cannot be added twice to the same database."""
    ns_1 = Namespace(
        miriam_id="MIR:00000258", prefix="combine.specifications", pattern="pattern"
    )
    session.add(ns_1)
    session.commit()
    ns_2 = Namespace(
        miriam_id="MIR:00000259", prefix="combine.specifications", pattern="pattern"
    )
    session.add(ns_2)
    with pytest.raises(IntegrityError):
        session.commit()


def test_pattern_not_null():
    """Expect that the pattern cannot be null."""
    with pytest.raises(TypeError):
        Namespace(miriam_id="MIR:00000258", prefix="combine.specifications")


def test_pattern_is_compiled():
    """Expect that the pattern is compiled to a regex object."""
    instance = Namespace(
        miriam_id="MIR:00000258",
        prefix="combine.specifications",
        pattern=r"^(foo|bar)$",
    )
    assert isinstance(instance.compiled_pattern, re.Pattern)
    assert instance.compiled_pattern.match("foo") is not None


def test_pattern_is_compiled_on_load(session):
    """Expect that the pattern is compiled on load."""
    instance = Namespace(
        miriam_id="MIR:00000258",
        prefix="combine.specifications",
        pattern=r"^(foo|bar)$",
    )
    session.add(instance)
    session.commit()
    instance = session.query(Namespace).first()
    assert isinstance(instance.compiled_pattern, re.Pattern)
    assert instance.compiled_pattern.match("foo") is not None


def test_embedded_prefix_default(session):
    """Expect that the default value is false."""
    instance = Namespace(
        miriam_id="MIR:00000258",
        prefix="combine.specifications",
        pattern=r"^\w+(\-|\.|\w)*$",
    )
    session.add(instance)
    session.commit()
    assert instance.embedded_prefix is False


def test_get_map(session, namespaces):
    """Expect that the namespace map contains all elements."""
    mapping = Namespace.get_map(session)
    assert mapping == namespaces


def test_get_partial_map(session, namespaces):
    """Expect that the namespace map contains only specified elements."""
    prefixes = ["go", "chebi"]
    mapping = Namespace.get_map(session, prefixes)
    assert len(mapping) == len(prefixes)
    for prefix in prefixes:
        assert mapping[prefix] == namespaces[prefix]
