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


"""Expect that the annotation model functions as designed."""


from importlib.resources import open_text

import pytest

from cobra_component_models import data
from cobra_component_models.io import AnnotationModel


with open_text(data, "biology_qualifiers.txt") as handler:
    BIOLOGY_QUALIFIERS = [line.strip() for line in handler.readlines()]


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param(
            {},
            marks=pytest.mark.raises(
                exception=ValueError, message="identifier\n  field required"
            ),
        ),
        pytest.param(
            {"identifier": "foo"},
            marks=pytest.mark.raises(
                exception=ValueError, message="biologyQualifier\n  field required"
            ),
        ),
        {"identifier": "foo", "biology_qualifier": "is"},
        {"identifier": "foo", "biology_qualifier": "is", "is_deprecated": False},
        {"identifier": "foo", "biology_qualifier": "is", "is_deprecated": True},
    ],
)
def test_annotation_init(attributes: dict):
    """Expect that appropriate exceptions are raised for wrong arguments."""
    annotation = AnnotationModel(**attributes)
    for attr, expected in attributes.items():
        assert getattr(annotation, attr) == expected


@pytest.mark.parametrize("qualifier", BIOLOGY_QUALIFIERS)
def test_all_qualifiers(qualifier: str):
    """Expect that all packaged biology qualifiers are acceptable."""
    annotation = AnnotationModel(identifier="foo", biology_qualifier=qualifier)
    assert annotation.biology_qualifier == qualifier
