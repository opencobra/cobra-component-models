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
    obj = CompoundSerializer(
        session=session, namespaces={}, biology_qualifiers={}
    ).serialize(cmpd)
    assert obj.id == "1"


def test_serialize_full_compound(session, biology_qualifiers):
    cmpd = Compound(
        inchi="InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3",
        inchi_key="LFQSCWFLJHTTHZ-UHFFFAOYSA-N",
        smiles="CCO",
        charge=0,
        chemical_formula="C2H6O",
        notes="bla bla bla",
    )
    chebi = Namespace(miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$")
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
        session=session,
        biology_qualifiers=biology_qualifiers,
        namespaces=Namespace.get_map(session),
    ).serialize(cmpd)
    assert obj.id == "1"
    assert obj.charge == 0
    assert obj.chemical_formula == "C2H6O"
    assert obj.notes == "bla bla bla"
    assert obj.names == {"chebi": ["ethanol", "Aethanol", "Alkohol"]}
    assert obj.annotation == {
        "inchi": [("is", "InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3")],
        "inchikey": [("is", "LFQSCWFLJHTTHZ-UHFFFAOYSA-N")],
        "smiles": [("is", "CCO")],
        "chebi": [("is", "CHEBI:16236"), ("is", "CHEBI:44594"), ("is", "CHEBI:42377")],
    }


def test_deserialize_full_compound(session, biology_qualifiers):
    # Add namespace to database so that it can be used in validation later.
    chebi = Namespace(miriam_id="MIR:00000002", prefix="chebi", pattern=r"^CHEBI:\d+$")
    session.add(chebi)
    session.commit()
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
        session=session,
        biology_qualifiers=biology_qualifiers,
        namespaces=Namespace.get_map(session),
    ).deserialize(obj)
    session.add(cmpd)
    session.commit()
    assert cmpd.inchi == "InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3"
    assert cmpd.inchi_key == "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"
    assert cmpd.smiles == "CCO"
    assert cmpd.charge == 0.0
    assert cmpd.chemical_formula == "C2H6O"
    assert cmpd.notes == "bla bla bla"
    for name, expected in zip(cmpd.names, ["ethanol", "Aethanol", "Alkohol"]):
        assert name.namespace.prefix == "chebi"
        assert name.name == expected
    for ann, expected in zip(
        cmpd.annotation,
        [("is", "CHEBI:16236"), ("is", "CHEBI:44594"), ("is", "CHEBI:42377")],
    ):
        assert ann.namespace.prefix == "chebi"
        assert (ann.biology_qualifier.qualifier, ann.identifier) == expected
