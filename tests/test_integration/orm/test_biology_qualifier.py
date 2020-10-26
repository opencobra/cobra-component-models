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


"""Expect that biology qualifiers function as designed."""


from importlib.resources import open_text

import pytest
from sqlalchemy.exc import IntegrityError

from cobra_component_models import data
from cobra_component_models.orm import BiologyQualifier


@pytest.mark.parametrize(
    "attributes", [{"qualifier": "is"}, {"id": 3, "qualifier": "is"}]
)
def test_init(attributes):
    """Expect that an object can be instantiated with the right attributes."""
    instance = BiologyQualifier(**attributes)
    for attr, value in attributes.items():
        assert getattr(instance, attr) == value


def test_unique_qualifier(session):
    """Expect that the same qualifier cannot be added twice to the same database."""
    qual_1 = BiologyQualifier(qualifier="is")
    session.add(qual_1)
    session.commit()
    qual_2 = BiologyQualifier(qualifier="is")
    session.add(qual_2)
    with pytest.raises(IntegrityError):
        session.commit()


def test_load(session):
    """Expect that all biology qualifiers are inserted."""
    BiologyQualifier.load(session)
    with open_text(data, "biology_qualifiers.txt") as handle:
        expected = {line.strip() for line in handle.readlines()}
    qualifiers = {bq.qualifier for bq in session.query(BiologyQualifier.qualifier)}
    assert qualifiers == expected
