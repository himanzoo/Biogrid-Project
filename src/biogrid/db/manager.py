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

    
    def _normalize_column_names(self, columns)   -> None:
        """Normalize column names to lowercase and replace spaces with underscores."""
        return [col.lower().replace(" ", "_").replace("#", "").replace("-", "_") for col in columns]


    def load_data(self)   -> pd.DataFrame:
        """Load data from the TSV file and normalize column names."""
        df = pd.read_csv(self.file_path, sep="\t")
        df.columns = self._normalize_column_names(df.columns)
        return df

    def get_interaction_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract interaction data from the raw DataFrame.

        Args:
            df: Raw DataFrame containing interaction data.

        Returns:
            DataFrame with columns: id, interactor_a_id, interactor_b_id, score,
            experimental_system, experimental_system_type.
        """
        # Create a DataFrame with the required columns for Interaction
        interaction_df = pd.DataFrame({
            'id': df['biogrid_interaction_id'],
            'interactor_a_id': df['swiss_prot_accessions_interactor_a'],
            'interactor_b_id': df['swiss_prot_accessions_interactor_b'],
            'score': df['score'].replace('-', None),
            'experimental_system': df['experimental_system'],
            'experimental_system_type': df['experimental_system_type']
        })
        return interaction_df

 
    def get_proteins_df(self, df: pd.DataFrame)   -> pd.DataFrame:
        """Extract proteins data from the DataFrame."""

        #Extract proteins a
        proteins_a = df[[
            "swiss_prot_accessions_interactor_a", "official_symbol_interactor_a",
            "organism_id_interactor_a"
        ]].rename(columns={
            "swiss_prot_accessions_interactor_a": "uniprot_id",
            "official_symbol_interactor_a": "symbol",
            "organism_id_interactor_a": "tax_id"
        })

        # Extract proteins b
        proteins_b = df[[
            "swiss_prot_accessions_interactor_b", "official_symbol_interactor_b",
            "organism_id_interactor_b"
        ]].rename(columns={
            "swiss_prot_accessions_interactor_b": "uniprot_id",
            "official_symbol_interactor_b": "symbol",
            "organism_id_interactor_b": "tax_id"
        })

        # Combine all proteins and drop duplicates
        return pd.concat([proteins_a, proteins_b]).drop_duplicates()

    def get_organisms_df(self, df: pd.DataFrame)   -> pd.DataFrame:
        """Extract organisms from DataFrame.

        Args:
            df (pd.DataFrame): _represent organisms for example in our case, two organisms_

        Returns:
            pd.DataFrame: _return organisms_
        """
        
        # Extract unique organisms from the raw data
        organisms_a = df[["organism_id_interactor_a", "organism_name_interactor_a"]]
        organisms_b = df[["organism_id_interactor_b", "organism_name_interactor_b"]]

        # Rename columns to match the expected format
        organisms_a = organisms_a.rename(
            columns={
                "organism_id_interactor_a": "tax_id",
                "organism_name_interactor_a": "name",
            }
        )
        organisms_b = organisms_b.rename(
            columns={
                "organism_id_interactor_b": "tax_id",
                "organism_name_interactor_b": "name",
            }
        )

        # Combine and drop duplicates
        organisms_df = pd.concat([organisms_a, organisms_b]).drop_duplicates().reset_index(drop=True)

        return organisms_df


    def import_data(self)   -> None:
        """Import data into the database."""
        df = self.load_data()
        interaction_df = self.get_interaction_df(df)
        protein_df = self.get_proteins_df(df)
        organism_df = self.get_organisms_df(df)

        with Session(self.engine) as session:
            # Import organisms
            for _, row in organism_df.iterrows():
                organism = Organism(tax_id=row["tax_id"], name=row["name"])
                session.merge(organism)

            # Import proteins
            for _, row in protein_df.iterrows():
                protein = Protein(
                uniprot_id=row["uniprot_id"],
                symbol=row["symbol"],
                tax_id=row["tax_id"]
                )
                session.merge(protein)

            # Import interactions
            for _, row in interaction_df.iterrows():
                interaction = Interaction(
                    id=row["id"],
                    interactor_a_id=row["interactor_a_id"],
                    interactor_b_id=row["interactor_b_id"],
                    score=row["score"],
                    experimental_system=row["experimental_system"],
                    experimental_system_type=row["experimental_system_type"]
                )
                session.merge(interaction)

            session.commit()




class Query:
    def __init__(self, engine: Engine)  -> None:
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