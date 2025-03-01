from typing import List
import pandas as pd
from sqlalchemy import Column, Engine, create_engine, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, sessionmaker
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

    
    def import_data(self) -> None:
        # Read the TSV file into a DataFrame
        df = pd.read_csv(self.file_path, sep="\t")

        # Create a session
        with self.Session() as session:
            for _, row in df.iterrows():
                # Create or get Organism instances
                organism_a = session.query(Organism).filter_by(id=row['Organism ID Interactor A']).first()
                if not organism_a:
                    organism_a = Organism(
                        id=row['Organism ID Interactor A'],
                        name=row['Organism Name Interactor A']
                    )
                    session.add(organism_a)

                organism_b = session.query(Organism).filter_by(id=row['Organism ID Interactor B']).first()
                if not organism_b:
                    organism_b = Organism(
                        id=row['Organism ID Interactor B'],
                        name=row['Organism Name Interactor B']
                    )
                    session.add(organism_b)

                # Create or get Protein instances
                protein_a = session.query(Protein).filter_by(id=row['BioGRID ID Interactor A']).first()
                if not protein_a:
                    protein_a = Protein(
                        id=row['BioGRID ID Interactor A'],
                        entrez_gene_id=row['Entrez Gene Interactor A'],
                        systematic_name=row['Systematic Name Interactor A'],
                        official_symbol=row['Official Symbol Interactor A'],
                        synonyms=row['Synonyms Interactor A'],
                        organism_id=organism_a.id
                    )
                    session.add(protein_a)

                protein_b = session.query(Protein).filter_by(id=row['BioGRID ID Interactor B']).first()
                if not protein_b:
                    protein_b = Protein(
                        id=row['BioGRID ID Interactor B'],
                        entrez_gene_id=row['Entrez Gene Interactor B'],
                        systematic_name=row['Systematic Name Interactor B'],
                        official_symbol=row['Official Symbol Interactor B'],
                        synonyms=row['Synonyms Interactor B'],
                        organism_id=organism_b.id
                    )
                    session.add(protein_b)

                # Create Interaction instance
                interaction = Interaction(
                    id=row['BioGRID Interaction ID'],
                    protein_a_id=protein_a.id,
                    protein_b_id=protein_b.id,
                    experimental_system=row['Experimental System'],
                    experimental_system_type=row['Experimental System Type'],
                    author=row['Author'],
                    publication_source=row['Publication Source'],
                    throughput=row['Throughput'],
                    score=row['Score'],
                    modification=row['Modification'],
                    qualifications=row['Qualifications'],
                    tags=row['Tags'],
                    source_database=row['Source Database']
                )
                session.add(interaction)

            # Commit the session to save all changes to the database
            session.commit()


        

    def _normalize_column_names(self, cols: list[str]) -> None:
        """
        Normalize column names by removing special characters, replacing spaces with underscores,
        and converting to lowercase.
        """
        normalized = []
        for col in cols:
            # Remove special characters (like #), replace spaces with underscores, and convert to lowercase
            col = col.replace("#", "").replace(" ", "_").lower()
            normalized.append(col)
        return normalized

    def load_data(self) -> pd.DataFrame:
        pass

    def get_interaction_df(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def get_protein_df(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def get_organism_df(self, df: pd.DataFrame) -> pd.DataFrame:
        pass




    
class Query:

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def count_proteins(self) -> int:
        pass

    def count_organisms(self) -> int:
        pass

    def count_interactions(self) -> int:
        pass