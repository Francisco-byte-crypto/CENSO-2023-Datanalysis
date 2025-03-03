import pandas as pd

def convert_columns_to_educationlevel(dataframe):
    education_codes = pd.read_excel('Codigos-variables/Codigo de niveles educativos.xlsx')
    education_codes.index = education_codes['codigo'].values
    del education_codes['codigo']

    education_levels = []
    for column in dataframe.columns:
        if column in education_codes.index:
            education = education_codes.loc[column, 'valor']
            education_levels.append(education)
        else:
            education_levels.append(column)
    return education_levels