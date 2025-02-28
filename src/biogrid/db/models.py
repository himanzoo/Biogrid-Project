from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column

class Base(DeclarativeBase):
    """Represent Declarative Base class, that is the base of all ORM models."""
    pass 

class Interaction(Base):
    """Represent interaction class that use Base class of ORM model.

    Args:
        id (_int_): _this represent id column (identification) of interaction_
        interactor_a_id (_str_): _represent id of iteraction a_
        interactor_b_id (_str_): _represent id of iteraction b_
        experimental_system (_str_): _this represent system of experiment like in our case Two-hybrid_
        experimental_system_type (_str_): _type of experiment like in our case physical experiment_
        score (_float_): _give score to show confidence level of experiment_
    """

    __tablename__ = "interactions"  # table name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Unique ID
    interactor_a_id: Mapped[str] = mapped_column(String, ForeignKey("proteins.uniprot_id"))  # Foreign key to Protein A
    interactor_b_id: Mapped[str] = mapped_column(String, ForeignKey("proteins.uniprot_id"))  # Foreign key to Protein B
    experimental_system: Mapped[str] = mapped_column(String, nullable=False)
    experimental_system_type: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=True)  # i assume score are given in float, not string form.

    # Relationships: An interaction links two proteins
    interactor_a = relationship("Protein", foreign_keys=[interactor_a_id])
    interactor_b = relationship("Protein", foreign_keys=[interactor_b_id])

class Organism(Base):
    """Represent Organism class of ORM model

    Args:
        tax_id (_int_): _tax id of organism that is unique so use as primary key_
        name (_str_): _name of organism_
    """
    __tablename__ = "organisms"  # table name

    tax_id: Mapped[int] = mapped_column (Integer, primary_key=True)  # tax id is unique for organism so it is primary key in its table
    name: Mapped[str] = mapped_column (String, nullable=False)

class Protein(Base):
    """Represent protein class.

    Args:
        uniprot_id (_str_): _uniprot id is unique identifier of protein so, it is primary key_
        symbol (_str_): _represent symbol of protein_
        tax_id (_int_): _tax id of organism that is foreign key of this table and primary key of organism table_
    """
    __tablename__ = "proteins"  # table name 

    uniprot_id: Mapped[str] = mapped_column (String, primary_key=True)  # primary key unique protein identifier (uniprot)
    symbol: Mapped[str] = mapped_column (String, nullable=False)
    tax_id: Mapped[int] = mapped_column (Integer, ForeignKey("organisms.tax_id"))

    # Relationships: Protein links organism
    organism = relationship ("Organism")
