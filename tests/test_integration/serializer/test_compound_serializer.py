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


"""Expect that compounds can be de-/serialized and selected/inserted."""


from cobra_component_models.io import CompoundModel
from cobra_component_models.orm import (
    BiologyQualifier,
    Compound,
    CompoundAnnotation,
    CompoundName,
    Namespace,
)
from cobra_component_models.serializer import CompoundSerializer


def test_serialize_default_compound(session):
    cmpd = Compound()
    session.add(cmpd)
    session.commit()
    obj = CompoundSerializer(session).serialize(cmpd)
    assert obj.id == "1"


def test_serialize_full_compound(session):
    cmpd = Compound(charge=-3, chemical_formula="C2H6O", notes="bla bla bla")
    chebi = Namespace(miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$")
    cmpd.names = [
        CompoundName(name=n, namespace=chebi) for n in ["one", "two", "three"]
    ]
    qual = BiologyQualifier(qualifier="is")
    cmpd.annotation = [
        CompoundAnnotation(identifier=i, namespace=chebi, qualifier=qual)
        for i in ["CHEBI:16236", "CHEBI:44594", "CHEBI:42377"]
    ]
    session.add(cmpd)
    session.commit()
    obj = CompoundSerializer(session).serialize(cmpd)
    assert obj.id == "1"
    assert obj.charge == -3
    assert obj.chemical_formula == "C2H6O"
    assert obj.notes == "bla bla bla"
    assert obj.names == ["one", "two", "three"]
    assert obj.annotation == {
        "chebi": [("is", "CHEBI:16236"), ("is", "CHEBI:44594"), ("is", "CHEBI:42377")]
    }


def test_deserialize_full_compound(session):
    obj = CompoundModel(id="1")
    cmpd = Compound(charge=-3, chemical_formula="C2H6O", notes="bla bla bla")
    chebi = Namespace(miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$")
    cmpd.names = [
        CompoundName(name=n, namespace=chebi) for n in ["one", "two", "three"]
    ]
    qual = BiologyQualifier(qualifier="is")
    cmpd.annotation = [
        CompoundAnnotation(identifier=i, namespace=chebi, qualifier=qual)
        for i in ["CHEBI:16236", "CHEBI:44594", "CHEBI:42377"]
    ]
    session.add(cmpd)
    session.commit()
    obj = CompoundSerializer(session).serialize(cmpd)
    assert obj.id == "1"
    assert obj.charge == -3
    assert obj.chemical_formula == "C2H6O"
    assert obj.notes == "bla bla bla"
    assert obj.names == ["one", "two", "three"]
    assert obj.annotation == {
        "chebi": [("is", "CHEBI:16236"), ("is", "CHEBI:44594"), ("is", "CHEBI:42377")]
    }
