import pandas as pd
from sqlalchemy import Engine

class Importer:

    def __init__(self, engine: Engine, file_path: str) -> None:
        pass
    
    def import_data(self) -> None:
        pass

    def _normalize_column_names(self, cols: [list](str)) -> None:
        pass

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
        pass

    def count_proteins(self) -> int:
        pass

    def count_organisms(self) -> int:
        pass

    def count_interactions(self) -> int:
        pass