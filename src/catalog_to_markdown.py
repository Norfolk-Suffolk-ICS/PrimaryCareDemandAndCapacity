from string import Template
import datetime as dt
import pandas as pd
from schemas import DataCatalog


OUTPUT_MARKDOWN_FILE  = "PelicanWebsite/content/data-catalogue/data_catalogue.md"

DATASET_COLUMN_MAPPING = {
    "name" : "Name",
    "description" : "Description",
    "website_url" : "Website URL",
    "zip_file" : "Source URL",
    "csv_file" : "Specific Source",
    }

MARKDOWN_TEMPLATE = Template("""Title: Data Catalogue
Date: $current_datetime
Modified: $current_datetime
Category: Data Catalogue
Authors: A.Jarman & I.Khan
Summary: A list of all the Datasets used in the analysis for the SNEE-ICS Demand and Capacity Modelling project.

## NHS England Datasets\n
<!-- START TABLE 1-->\n
$table1
<br>
<!-- END TABLE 1-->\n
## ONS Population Scenarios\n
<!-- START TABLE 2-->\n
$table2
<br><hr><br>
<!-- END TABLE 2-->\n
""")

def create_link(url:str, text:str='Source')->str:
    """Creates html tags for a url 
    with the text provided as the displayed text.

    Parameters
    ----------
    url : str
        url used in link
    text : str, optional
        Text displayed, by default 'Source'

    Returns
    -------
    str
        HTML chunk for a link
    """
    return f"<a href='{url}'>{text}</a>"


if __name__ == '__main__':  
    # note that this should be run from the root directory
    catalog = DataCatalog.load_from_yaml("data_catalog.yaml")

    # create a dataframe for each table and rename the columns
    single_source_df = pd.DataFrame(
        [entry.model_dump() for entry in  catalog.single_data_sources]
        ).loc[:,list(DATASET_COLUMN_MAPPING.keys())].rename(columns=DATASET_COLUMN_MAPPING)
    ons_df = pd.DataFrame(
        [entry.model_dump() for entry in  catalog.scenario_data_sources[0].scenarios]
        ).loc[:,list(DATASET_COLUMN_MAPPING.keys())].rename(columns=DATASET_COLUMN_MAPPING)
    
    # loop through both tables and create links for the source and website columns
    for table in single_source_df, ons_df:
        for column in table.columns:
            if column in ["Source URL", "Website URL"]:
                # table only the first word of the column name as the link text
                link_text = column.split(" ")[0]
                # create the link
                table[column] = table[column].map(lambda x: create_link(x, link_text))

    # create a dictionary of the tables to be inserted into the markdown template
    tables = {
        "table1": single_source_df.to_html(index=False,escape=False),
        "table2": ons_df.to_html(index=False,escape=False)}

    # write to file
    with open(OUTPUT_MARKDOWN_FILE, "w") as md_file:
        file_content = MARKDOWN_TEMPLATE.substitute(current_datetime=dt.datetime.now().isoformat(),**tables) 
        md_file.write(file_content)