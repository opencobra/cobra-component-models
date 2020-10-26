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


"""Expect that compounds function as designed."""


import pytest

from cobra_component_models.orm import (
    Compound,
    CompoundAnnotation,
    CompoundName,
    Namespace,
)


@pytest.mark.parametrize(
    "attributes",
    [
        {},
        {"id": 22},
        {"inchi": "InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3"},
        {"inchi_key": "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"},
        {"smiles": "CCO"},
        {"charge": 0},
        {"chemical_formula": "C2H6O"},
        {"notes": "I should not forget about this!"},
    ],
)
def test_init(attributes):
    """Expect that an object can be instantiated with the right attributes."""
    instance = Compound(**attributes)
    for attr, value in attributes.items():
        assert getattr(instance, attr) == value


def test_names(session):
    """Expect that names can be added to a compound."""
    compound = Compound()
    namespace = Namespace(
        miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$"
    )
    compound.names.append(CompoundName(name="ethanol", namespace=namespace))
    session.add(compound)
    session.commit()


def test_annotation(session):
    """Expect that names can be added to a compound."""
    compound = Compound()
    namespace = Namespace(
        miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$"
    )
    compound.annotation.append(
        CompoundAnnotation(identifier="CHEBI:16236", namespace=namespace)
    )
    session.add(compound)
    session.commit()
