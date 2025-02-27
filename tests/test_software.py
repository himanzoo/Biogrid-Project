import os.path

import pandas as pd
import pytest
from sqlalchemy import Engine, create_engine

from biogrid.db.manager import Importer, Query
from biogrid.db.models import Base, Interaction, Organism, Protein

file_path = os.path.join("tests", "data", "test_data.tsv")
connection_string = "sqlite:///biogrid.db"

engine: Engine = create_engine(url=connection_string)

data = [
    {
        "biogrid_interaction_id": 1,
        "official_symbol_interactor_a": "symbol_1",
        "official_symbol_interactor_b": "symbol_2",
        "experimental_system": "Two-hybrid",
        "experimental_system_type": "physical",
        "organism_id_interactor_a": 2697049,
        "organism_id_interactor_b": 2697049,
        "score": "-",
        "swiss_prot_accessions_interactor_a": "P1",
        "swiss_prot_accessions_interactor_b": "P2",
        "organism_name_interactor_a": "Severe acute respiratory syndrome coronavirus 2",
        "organism_name_interactor_b": "Severe acute respiratory syndrome coronavirus 2",
    },
    {
        "biogrid_interaction_id": 2,
        "official_symbol_interactor_a": "symbol_2",
        "official_symbol_interactor_b": "symbol_3",
        "experimental_system": "Two-hybrid",
        "experimental_system_type": "physical",
        "organism_id_interactor_a": 2697049,
        "organism_id_interactor_b": 9606,
        "score": "-",
        "swiss_prot_accessions_interactor_a": "P2",
        "swiss_prot_accessions_interactor_b": "P3",
        "organism_name_interactor_a": "Severe acute respiratory syndrome coronavirus 2",
        "organism_name_interactor_b": "Homo sapiens",
    },
    {
        "biogrid_interaction_id": 3,
        "official_symbol_interactor_a": "symbol_3",
        "official_symbol_interactor_b": "symbol_1",
        "experimental_system": "Proximity Label-MS",
        "experimental_system_type": "physical",
        "organism_id_interactor_a": 9606,
        "organism_id_interactor_b": 2697049,
        "score": "-",
        "swiss_prot_accessions_interactor_a": "P3",
        "swiss_prot_accessions_interactor_b": "P1",
        "organism_name_interactor_a": "Homo sapiens",
        "organism_name_interactor_b": "Severe acute respiratory syndrome coronavirus 2",
    },
]

data_interactions = [
    {
        "id": 1,
        "interactor_a_id": "P1",
        "interactor_b_id": "P2",
        "score": None,
        "experimental_system": "Two-hybrid",
        "experimental_system_type": "physical",
    },
    {
        "id": 2,
        "interactor_a_id": "P2",
        "interactor_b_id": "P3",
        "score": None,
        "experimental_system": "Two-hybrid",
        "experimental_system_type": "physical",
    },
    {
        "id": 3,
        "interactor_a_id": "P3",
        "interactor_b_id": "P1",
        "score": None,
        "experimental_system": "Proximity Label-MS",
        "experimental_system_type": "physical",
    },
]

data_organisms = [
    {"tax_id": 2697049, "name": "Severe acute respiratory syndrome coronavirus 2"},
    {"tax_id": 9606, "name": "Homo sapiens"},
]

data_proteins = [
    {"uniprot_id": "P1", "symbol": "symbol_1", "tax_id": 2697049},
    {"uniprot_id": "P2", "symbol": "symbol_2", "tax_id": 2697049},
    {"uniprot_id": "P3", "symbol": "symbol_3", "tax_id": 9606},
]

normalized_column_names = [
    "biogrid_interaction_id",
    "official_symbol_interactor_a",
    "official_symbol_interactor_b",
    "experimental_system",
    "experimental_system_type",
    "organism_id_interactor_a",
    "organism_id_interactor_b",
    "score",
    "swiss_prot_accessions_interactor_a",
    "swiss_prot_accessions_interactor_b",
    "organism_name_interactor_a",
    "organism_name_interactor_b",
]


@pytest.fixture
def importer() -> Importer:
    return Importer(engine=engine, file_path=file_path)


@pytest.fixture
def query() -> Query:
    importer: Importer = Importer(engine=engine, file_path=file_path)
    importer.import_data()
    return Query(engine=engine)


class TestImporter:

    def test_normalize_column_names(self, importer: Importer):
        test_cols = ["#BioGRID Interaction ID", "Entrez Gene Interactor A"]
        expected_cols = ["biogrid_interaction_id", "entrez_gene_interactor_a"]
        norm_cols = importer._normalize_column_names(test_cols)
        assert norm_cols == expected_cols

    def test_load_data(self, importer: Importer):
        df_test = pd.DataFrame(data)
        df: pd.DataFrame = importer.load_data()
        assert df.equals(df_test)

    def test_get_interaction_df(self, importer: Importer):
        df: pd.DataFrame = importer.load_data()
        interaction_df: pd.DataFrame = importer.get_interaction_df(df)
        interaction_df_test = pd.DataFrame(data_interactions)
        assert interaction_df.equals(interaction_df_test)

    def test_get_protein_df(self, importer: Importer):
        df = importer.load_data()
        protein_df: pd.DataFrame = importer.get_proteins_df(df)
        protein_df_test = pd.DataFrame(data_proteins)
        assert protein_df.equals(protein_df_test)

    def test_get_organism_df(self, importer: Importer):
        df: pd.DataFrame = importer.load_data()
        organism_df: pd.DataFrame = importer.get_organisms_df(df)
        organism_df_test = pd.DataFrame(data_organisms)
        assert organism_df.equals(organism_df_test)


class TestQuery:
    def test_count_proteins(self, query: Query):
        assert query.count_proteins() == 3

    def test_count_organisms(self, query: Query):
        assert query.count_organisms() == 2

    def test_count_interactions(self, query: Query):
        assert query.count_interactions() == 3
