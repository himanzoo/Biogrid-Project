import pandas as pd
from typing import List
from sqlalchemy import Column, Engine, create_engine, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, sessionmaker, Session
from biogrid.db.models import Base, Interaction, Organism, Protein


class Importer:
    """Represent importer class"""

    def __init__(self, engine: Engine = create_engine("sqlite:///biogrid.db"), file_path: str = "/Users/hira/Desktop/biogrid/tests/data/test_data.tsv") -> None:
        """initialize the importer class

        Args:
            engine (_str_): Defaults to create_engine("sqlite:///biogrid.db").
            path_test_data (_str_): Defaults to "/Users/hira/Desktop/biogrid/tests/data/test_data.tsv".
        """
        self.engine = engine
        self.file_path = file_path
        self.Session = sessionmaker(self.engine)

    
    def _normalize_column_names(self, columns):
        """Normalize column names to lowercase and replace spaces with underscores."""
        return [col.lower().replace(" ", "_").replace("#", "") for col in columns]


    def load_data(self):
        """Load data from the TSV file and normalize column names."""
        df = pd.read_csv(self.file_path, sep="\t")
        df.columns = self._normalize_column_names(df.columns)
        return df

    def get_interaction_df(self, df):
        pass

    def get_proteins_df(self, df):
        """Extract proteins data from the DataFrame."""
        proteins_a = df[[
            "swiss-prot_accessions_interactor_a", "official_symbol_interactor_a",
            "organism_id_interactor_a"
        ]].rename(columns={
            "swiss-prot_accessions_interactor_a": "uniprot_id",
            "official_symbol_interactor_a": "symbol",
            "organism_id_interactor_a": "tax_id"
        })
        proteins_b = df[[
            "swiss-prot_accessions_interactor_b", "official_symbol_interactor_b",
            "organism_id_interactor_b"
        ]].rename(columns={
            "swiss-prot_accessions_interactor_b": "uniprot_id",
            "official_symbol_interactor_b": "symbol",
            "organism_id_interactor_b": "tax_id"
        })
        return pd.concat([proteins_a, proteins_b]).drop_duplicates()

    def get_organisms_df(self, df):
        pass

    def import_data(self):
       pass




    
class Query:
    def __init__(self, engine: Engine):
        self.engine = engine

    def count_proteins(self) -> int:
        """Count the number of proteins in the database."""
        with Session(self.engine) as session:
            return session.query(Protein).count()

    def count_organisms(self) -> int:
        """Count the number of organisms in the database."""
        with Session(self.engine) as session:
            return session.query(Organism).count()

    def count_interactions(self) -> int:
        """Count the number of interactions in the database."""
        with Session(self.engine) as session:
            return session.query(Interaction).count()