import pandas as pd

def convert_index_to_country(dataframe=None):
    country_codes = pd.read_excel("Codigos-variables/Codigos de paises.xlsx")
    country_codes.index = country_codes['codigo'].values
    del country_codes['codigo']

    countries = []
    for index in dataframe.index:
        if index in country_codes.index:
            country = country_codes.loc[index, 'pais']
            countries.append(country)
        else:
            countries.append(index)
    return countries
