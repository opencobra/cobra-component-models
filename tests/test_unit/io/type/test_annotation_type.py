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


"""Expect that annotation types function as designed."""


from importlib.resources import open_text

import pytest
from pydantic import BaseModel

from cobra_component_models import data
from cobra_component_models.io.type import AnnotationType


with open_text(data, "biology_qualifiers.txt") as handler:
    BIOLOGY_QUALIFIERS = [l.strip() for l in handler.readlines()]


class DummyModel(BaseModel):
    """Define a dummy model for testing the annotation type."""

    annotation: AnnotationType


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param(
            {"annotation": ["single"]},
            marks=pytest.mark.raises(exception=ValueError, message="consist"),
        ),
        pytest.param(
            {"annotation": ["wrong", "single"]},
            marks=pytest.mark.raises(exception=ValueError, message="valid"),
        ),
    ],
)
def test_bad_init(attributes):
    """Expect that appropriate exceptions are raised for wrong arguments."""
    DummyModel(**attributes)


@pytest.mark.parametrize("qualifier", BIOLOGY_QUALIFIERS)
def test_all_qualifiers(qualifier):
    """Expect that all packaged biology qualifiers are acceptable."""
    obj = DummyModel(annotation=[qualifier, "foo"])
    assert obj.annotation[0] == qualifier
