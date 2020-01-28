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
from cobra_component_models.orm import Compound, CompoundAnnotation, CompoundName
from cobra_component_models.serializer import CompoundSerializer


def test_serialize_default_compound(session):
    """Expect that a default compound can be serialized."""
    cmpd = Compound()
    session.add(cmpd)
    session.commit()
    obj = CompoundSerializer(namespaces={}, biology_qualifiers={}).serialize(cmpd)
    assert obj.id == "1"


def test_serialize_full_compound(session, biology_qualifiers, namespaces):
    """Expect that a fully fleshed out compound can be serialized."""
    chebi = namespaces["chebi"]
    cmpd = Compound(
        inchi="InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3",
        inchi_key="LFQSCWFLJHTTHZ-UHFFFAOYSA-N",
        smiles="CCO",
        charge=0,
        chemical_formula="C2H6O",
        notes="bla bla bla",
    )
    cmpd.names = [
        CompoundName(name=n, namespace=chebi)
        for n in ["ethanol", "Aethanol", "Alkohol"]
    ]
    qual = biology_qualifiers["is"]
    cmpd.annotation = [
        CompoundAnnotation(identifier=i, namespace=chebi, biology_qualifier=qual)
        for i in ["CHEBI:16236", "CHEBI:44594", "CHEBI:42377"]
    ]
    session.add(cmpd)
    session.commit()
    obj = CompoundSerializer(
        biology_qualifiers=biology_qualifiers, namespaces=namespaces
    ).serialize(cmpd)
    assert obj.id == "1"
    assert obj.charge == 0
    assert obj.chemical_formula == "C2H6O"
    assert obj.notes == "bla bla bla"
    assert "chebi" in obj.names
    assert set(obj.names["chebi"]) == {"ethanol", "Aethanol", "Alkohol"}
    assert set(obj.annotation) == {"inchi", "inchikey", "smiles", "chebi"}
    assert set(obj.annotation["inchi"]) == {("is", "InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3")}
    assert set(obj.annotation["inchikey"]) == {("is", "LFQSCWFLJHTTHZ-UHFFFAOYSA-N")}
    assert set(obj.annotation["smiles"]) == {("is", "CCO")}
    assert set(obj.annotation["chebi"]) == {
        ("is", "CHEBI:16236"),
        ("is", "CHEBI:44594"),
        ("is", "CHEBI:42377"),
    }


def test_deserialize_full_compound(session, biology_qualifiers, namespaces):
    """Expect that a fully fleshed out compound can be deserialized."""
    obj = CompoundModel(
        **{
            "id": "1",
            "notes": "bla bla bla",
            "names": {"chebi": ["ethanol", "Aethanol", "Alkohol"]},
            "annotation": {
                "chebi": [
                    ["is", "CHEBI:16236"],
                    ["is", "CHEBI:44594"],
                    ["is", "CHEBI:42377"],
                ],
                "inchi": [["is", "InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3"]],
                "inchikey": [["is", "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"]],
                "smiles": [["is", "CCO"]],
            },
            "charge": 0.0,
            "chemicalFormula": "C2H6O",
        }
    )
    cmpd = CompoundSerializer(
        biology_qualifiers=biology_qualifiers, namespaces=namespaces
    ).deserialize(obj)
    session.add(cmpd)
    session.commit()
    assert cmpd.inchi == "InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3"
    assert cmpd.inchi_key == "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"
    assert cmpd.smiles == "CCO"
    assert cmpd.charge == 0.0
    assert cmpd.chemical_formula == "C2H6O"
    assert cmpd.notes == "bla bla bla"
    assert "chebi" in {n.namespace.prefix for n in cmpd.names}
    assert {n.name for n in cmpd.names} == {"ethanol", "Aethanol", "Alkohol"}
    assert "chebi" in {a.namespace.prefix for a in cmpd.annotation}
    assert {(a.biology_qualifier.qualifier, a.identifier) for a in cmpd.annotation} == {
        ("is", "CHEBI:16236"),
        ("is", "CHEBI:44594"),
        ("is", "CHEBI:42377"),
    }
