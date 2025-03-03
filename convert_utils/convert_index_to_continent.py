import pandas as pd

def convert_index_to_continent(dataframe=None):
    country_codes = pd.read_excel("Codigos-variables/Codigos de paises.xlsx")
    country_codes.index = country_codes['codigo'].values
    del country_codes['codigo']

    continents = []
    for index in dataframe.index:
        if index in country_codes.index:
            continent = country_codes.loc[index, 'continente']
            continents.append(continent)
        else:
            continents.append(index)
    return continents
