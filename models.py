from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str]
    population_2022: Mapped[int]
    population_2023: Mapped[int]
    change_percent: Mapped[str]
    region: Mapped[str]
    subregion: Mapped[str]

    def __repr__(self) -> str:
        return f"<Country(id={self.id}, country={self.country}, population_2022={self.population_2022}, population_2023={self.population_2023}, change_percent={self.change_percent}, region={self.region}, subregion={self.subregion})>"

# database connection
db_url = f"postgresql://postgres:postgres@db:5432/postgres"
engine = create_engine(db_url, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
