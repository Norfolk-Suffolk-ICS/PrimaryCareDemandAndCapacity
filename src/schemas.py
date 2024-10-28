from typing import Dict, Any, List, Literal, Optional, Union, Annotated
from enum import Enum
from abc import ABC, abstractmethod
from io import BytesIO
from zipfile import ZipFile
import requests
from pydantic import BaseModel, Field
import yaml
import pandas as pd

import constants as const


class DataCatalogEntryType(Enum):
    """Enum for the different types of data sources"""
    CSV_IN_ZIP = "csv_in_zip"
    CSV = "csv"
    JSON = "json"
    SQL = "sql_query"
    API = "api"


class DataCatalogLoadType(str, Enum):
    """Enum for the different ways to load data sources"""
    CATALOG: str = "catalog"
    DF: str = "dataframe"
    PY_NATIVE: str = "python_native"


class DataCatalogBase(BaseModel, ABC):
    """
    Base class for data catalog entries.
    """
    name: str
    description: str
    load_as: DataCatalogLoadType
    read_kwargs: Optional[dict] = None
    website_url: Optional[str] = None
    readme: Optional[str] = None

    @abstractmethod
    def load(self, read_kwargs: dict | None = None) -> Any:
        """converts loads the data source into a python object

        Returns:
            Any: the data source
        """
        if self.load_as == DataCatalogLoadType.CATALOG:
            pass  # do nothing this is overloaded
        elif self.load_as == DataCatalogLoadType.DF:
            return self.to_pandas_dataframe(read_kwargs)
        elif self.load_as == DataCatalogLoadType.PY_NATIVE:
            return self.to_dict(read_kwargs)
        else:
            raise NotImplementedError(f"{self.load_as} load not implemented")


class CSVCatalogEntry(DataCatalogBase):
    source_type: Literal["csv"] = "csv"
    csv_file: str

    def to_pandas_dataframe(self, read_kwargs: dict | None = None) -> pd.DataFrame:
        """Loads the csv file into a pandas dataframe

        Returns:
            pd.DataFrame: the dataframe
        """
        if read_kwargs is None:
            read_csv_kwargs = {}
        else:
            read_csv_kwargs = read_kwargs
        return pd.read_csv(self.csv_file, **read_csv_kwargs)

    def to_dict(self, read_kwargs: dict | None = None) -> dict:
        """Loads the csv file into a dictionary

        Returns:
            dict: the dictionary
        """

        return pd.read_csv(self.csv_file, read_kwargs).to_dict()


class CSVinZIPCatalogEntry(CSVCatalogEntry):
    """
    Catalog entry for a csv file in a zip file.
    """
    source_type: Literal["csv_in_zip"] = "csv_in_zip"
    zip_url: str
    csv_file: str
    zip_file: ZipFile | None = None  # only used for loading, temporary

    def load(self, read_kwargs: dict | None = None) -> Any:
        """Loads the csv file into a python object

        Args:
            read_kwargs (dict | None, optional): passed to pandas.read_csv(). Defaults to None.

        Raises:
            requests.HTTPError: raised if there is an error downloading the zip file
            NotImplementedError: raised when attempting a 

        Returns:
            Any: _description_
        """

        if self.zip_url.startswith("http"):
            zip_file_response = requests.get(self.zip_url, timeout=1000)
            if zip_file_response.status_code != 200:
                raise requests.HTTPError(
                    f"Could not download zip file from {self.zip_url}, \
                        status code {zip_file_response.status_code}"
                )
            zip_bytes = BytesIO(zip_file_response.content)
            zip_bytes.seek(0)
            self.zip_file = ZipFile(zip_bytes)
        else:
            # assume local file object
            self.zip_file = ZipFile(self.zip_url)

        if self.load_as == DataCatalogLoadType.DF:
            return self.to_pandas_dataframe(read_kwargs)
        elif self.load_as == DataCatalogLoadType.PY_NATIVE:
            return self.to_pandas_dataframe(read_kwargs).to_dict()
        elif self.load_as == DataCatalogLoadType.CATALOG:
            raise NotImplementedError(
                f"{self.load_as} load not implemented for zip files")
        self.zip_file = None

    class Config:
        arbitrary_types_allowed = True  # allow zip_file to be set to ZipFile object

    def to_pandas_dataframe(self, read_kwargs: dict | None = None) -> pd.DataFrame:
        # download / extract zip file to buffer and read csv from buffer

        # use pandas to read csv from zip file
        if read_kwargs is None:
            read_csv_kwargs = {}
        else:
            read_csv_kwargs = read_kwargs

        csv_file = self.zip_file.open(self.csv_file, 'r')
        return pd.read_csv(csv_file, **read_csv_kwargs)

    def to_dict(self, read_kwargs: dict | None = None) -> dict:
        return self.to_pandas_dataframe(read_kwargs).to_dict()


class SQLQueryCatalogEntry(DataCatalogBase):
    source_type: Literal["sql_query"] = "sql_query"
    query: str
    database_metadata: Optional[Dict[str, Any]] = None

    def to_pandas_dataframe(self, read_kwargs: Optional[dict] = None) -> pd.DataFrame:
        """Loads the sql query into a pandas dataframe

        Returns:
            pd.DataFrame: the dataframe
        """
        if read_kwargs is None:
            read_sql_kwargs = {}
        else:
            read_sql_kwargs = read_kwargs
        return pd.read_sql(self.query, **read_sql_kwargs)

    def load(self, read_kwargs: Optional[dict] = None) -> Any:
        """converts loads the data source into a python object

        Returns:
            Any: the data source
        """
        return self.to_pandas_dataframe(read_kwargs=read_kwargs)


# 'Register' these types with pydantic
DataCatalogEntry = Annotated[Union[CSVCatalogEntry, CSVinZIPCatalogEntry,
                                   SQLQueryCatalogEntry], Field(discriminator='source_type')]


class ScenariosCatalogEntry(DataCatalogBase):
    load_as: DataCatalogLoadType = DataCatalogLoadType.CATALOG  # override load_as
    scenarios: List[DataCatalogEntry]

    def load(self, read_kwargs: dict | None = None) -> Dict[str, Any]:
        """Loads each of the scenarios into a dictionary, keyed by scenario name

        Args:
            load_kwargs (Optional[dict], optional): _description_. Defaults to None.

        Returns:
            Dict[str, Any]: _description_
        """
        scenario_data = {}

        for scenario in self.scenarios:
            if scenario.read_kwargs is not None:
                scenario_kwargs = scenario.read_kwargs.get(
                    scenario.name, {})
            else:
                scenario_kwargs = {}
            scenario_data[scenario.name] = scenario.load(
                **scenario_kwargs)
        return scenario_data


class DataCatalog(BaseModel):
    """Class which documents the data sources used in a model run
    consists of single data sources (catalog entries) and scenario data sources (sub-catalog of entries)
    """

    domain: str
    single_data_sources: List[DataCatalogEntry]
    scenario_data_sources: List[ScenariosCatalogEntry]
    notes: Optional[str] = None

    @classmethod
    def load_from_yaml(cls, catalog_path: str = "data_catalog.yaml") -> "DataCatalog":
        """Loads a data catalog from a yaml file

        Args:
            catalog_path (str, optional): path to data catalog file. Defaults to "data_catalog.yaml".

        Raises:
            FileNotFoundError: When file is not found
            yaml.YAMLError: When yaml file is not valid, or parsing error
            Exception: Any other error

        Returns:
            DataCatalog: an instance of the object
        """

        try:
            yaml_dict: Dict[str, Any] = yaml.safe_load(
                open(catalog_path, 'r', encoding='utf-8'))
        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"Could not find data catalog at {catalog_path}, check filepath.") from error
        except yaml.YAMLError as error:
            raise yaml.YAMLError(
                f"Could not load data catalog at {catalog_path}, check formatting.") from error
        except Exception as error:
            raise Exception(
                f"Could not load data catalog at {catalog_path}, \
                    please check file is valid") from error

        cat_instance = cls.model_validate(yaml_dict)
        return cat_instance

    def get_catalog_entry_by_name(self, name: str) -> DataCatalogEntry:
        """Returns a data catalog entry by name

        Args:
            name (str): name of the data catalog entry

        Raises:
            KeyError: if the name is not found

        Returns:
            DataCatalogEntry: the data catalog entry
        """
        for entry in self.single_data_sources:
            if entry.name == name:
                return entry
        raise KeyError(f"Could not find data catalog entry with name {name}")
    
    def get_top_level_scenario_by_name(self,name:str)->ScenariosCatalogEntry:
        """Returns a top level scenario by name

        Args:
            name (str): name of the scenario

        Raises:
            KeyError: if the name is not found

        Returns:
            ScenariosCatalogEntry: the scenario
        """
        for entry in self.scenario_data_sources:
            if entry.name == name:
                return entry
        raise KeyError(f"Could not find scenario with name {name}")

    def get_scenario_catalog_entry_by_name(self, name: str, scenario_name:str) -> DataCatalogEntry:
        """Returns a data catalog entry by name

        Args:
            name (str): name of the data catalog entry

        Raises:
            KeyError: if the name is not found

        Returns:
            DataCatalogEntry: the data catalog entry
        """
        toplevel_scenario = self.get_top_level_scenario_by_name(name)
        for entry in toplevel_scenario.scenarios:
            if entry.name == scenario_name:
                return entry
        raise KeyError(f"Could not find scenario data catalog entry with name {name}")


# class CommunityReferralRates(BaseModel):
#     area:Literal[tuple(const.CCG_SUB_ICB.keys())]
#     rate: float

# class AcuteReferralRates(BaseModel):
#     area: Literal[tuple(const.CCG_SUB_ICB.keys())]
#     gp: float = Field(..., alias='GP')
#     Other:float = Field(..., alias='Other')

# class ReferralRates(BaseModel):
#     acute: List[AcuteReferralRates]
#     community: List[CommunityReferralRates]


if __name__ == '__main__':
    my_catalog = DataCatalog.load_from_yaml()

    single_sources = {source.name: source.load()
                      for source in my_catalog.single_data_sources}
    
    print(single_sources)

    ons_scenarios = my_catalog.scenario_data_sources[0].load()

    print(ons_scenarios)