import pandas as pd
from datetime import datetime
# convert_dtype/...
from convert_utils.convert_columns_todate import convert_columns_todate
from convert_utils.convert_index_to_country import convert_index_to_country
from convert_utils.convert_columns_to_educationlevel import convert_columns_to_educationlevel
from convert_utils.convert_index_to_continent import convert_index_to_continent
class Graphs:
    def __init__(self):
        self.ID_CENSO = 'ID_CENSO'
        self.LUGAR_DE_NACIMIENTO = 'PERMI01'
        self.ANO_DE_LLEGADA_A_URUGUAY = 'PERMI02'
        self.LUGAR_DE_RESIDENCIA_ANTERIOR = 'PERMI06'
        self.CODIGO_DE_PAIS_PERMI06 = 'PERMI06_4'
        self.CODIGO_DE_PAIS_PERMI04 = 'PERMI01_4'
        self.EDAD = 'PERNA01'
        self.NIVEL_EDUCATIVO_MAS_ALTO = 'PERED03_1'
        self.ESTADO_CONYUGAL = 'PEREC04'
        pass
    
    def create_df_for_graph_1(self):
        dataframe = pd.read_csv('INE-Personas-DB/personas_ext_26_02.csv', usecols=[self.CODIGO_DE_PAIS_PERMI06, self.ANO_DE_LLEGADA_A_URUGUAY, self.LUGAR_DE_NACIMIENTO, self.CODIGO_DE_PAIS_PERMI04 , self.ID_CENSO])
        
        # Que haya nacido en otro país.
        dataframe = dataframe.loc[dataframe[self.LUGAR_DE_NACIMIENTO] == 4]
        
        # Tomamos una tabla pivote que relacione año de llegada al país con país de origen.
        dataframe = dataframe.pivot_table(values=[self.ID_CENSO], columns=[self.ANO_DE_LLEGADA_A_URUGUAY], index=[self.CODIGO_DE_PAIS_PERMI06], aggfunc='count')

        dataframe.fillna(value=0, inplace=True)
        dataframe.columns = convert_columns_todate(dataframe)
        dataframe.index = convert_index_to_country(dataframe)
        
        dataframe.to_excel('Dataframe grafico 1.xlsx')

    def create_df_for_graph_2(self):
        dataframe = pd.read_csv('INE-Personas-DB/personas_ext_26_02.csv', usecols=[self.EDAD, self.LUGAR_DE_NACIMIENTO, self.CODIGO_DE_PAIS_PERMI04 , self.ANO_DE_LLEGADA_A_URUGUAY, self.ID_CENSO])
        
        # Que haya nacido en otro país.
        dataframe = dataframe.loc[dataframe[self.LUGAR_DE_NACIMIENTO] == 4]

        # Que el valor de edad sea menor a 99 para los codigos de error no modifiquen el promedio.
        dataframe = dataframe.loc[dataframe[self.EDAD]<99]

        # Tomamos una tabla pivote que relacione edad con país de nacimiento.
        dataframe = dataframe.pivot_table(values=self.ID_CENSO, columns=self.EDAD, index=self.CODIGO_DE_PAIS_PERMI04, aggfunc='count')
        dataframe.fillna(value=0, inplace=True)
        
        countries = convert_index_to_country(dataframe)
        dataframe.index = countries

        dataframe.to_excel('Dataframe grafico 2.xlsx')

    def create_df_for_graph_3(self):
        dataframe = pd.read_csv('INE-Personas-DB/personas_ext_26_02.csv', usecols=[self.LUGAR_DE_NACIMIENTO, self.CODIGO_DE_PAIS_PERMI04 , self.ANO_DE_LLEGADA_A_URUGUAY, self.NIVEL_EDUCATIVO_MAS_ALTO, self.ID_CENSO])
        
        # Que haya nacido en otro país.
        dataframe = dataframe.loc[dataframe[self.LUGAR_DE_NACIMIENTO] == 4]

        # Que el año de llegada sea mayor al 2003. Sin excluir los códigos genéricos.
        dataframe = dataframe.loc[(dataframe['PERMI02'] >= 2003) | (dataframe['PERMI02'] == 7777) | (dataframe['PERMI02'] == 8888) | (dataframe['PERMI02'] ==9898) | (dataframe['PERMI02'] == 9999)]
        
        # Tomamos una tabla pivote que relacione nivel educativo con país de nacimiento.
        dataframe = dataframe.pivot_table(values=self.ID_CENSO, columns=self.NIVEL_EDUCATIVO_MAS_ALTO, index=self.CODIGO_DE_PAIS_PERMI04, aggfunc='count')
        
        columns = convert_columns_to_educationlevel(dataframe)
        dataframe.columns = columns
        index = convert_index_to_country(dataframe)
        dataframe.index = index

        dataframe.to_excel('Dataframe grafico 3.xlsx')

    def create_df_for_graph_4(self):
        dataframe = pd.read_csv('INE-Personas-DB/personas_ext_26_02.csv', usecols=[self.CODIGO_DE_PAIS_PERMI06, self.ANO_DE_LLEGADA_A_URUGUAY, self.LUGAR_DE_NACIMIENTO, self.CODIGO_DE_PAIS_PERMI04 , self.ID_CENSO, self.ESTADO_CONYUGAL])
        
        # Que haya nacido en otro país.
        dataframe = dataframe.loc[dataframe[self.LUGAR_DE_NACIMIENTO] == 4]
        
        # Tomamos una tabla pivote que relacione año de llegada al país con país de origen.
        dataframe = dataframe.pivot_table(values=[self.ID_CENSO], columns=[self.ESTADO_CONYUGAL], index=[self.CODIGO_DE_PAIS_PERMI06], aggfunc='count')

        # Convertimos los códigos de país en su respectivo continente y los agrupamos.
        dataframe.index = convert_index_to_continent(dataframe)
        dataframe = dataframe.groupby(dataframe.index).sum()

        dataframe.fillna(value=0, inplace=True)        
        dataframe.to_excel('Dataframe grafico 4.xlsx')

graphs = Graphs()
graphs.create_df_for_graph_1()
graphs.create_df_for_graph_2()
graphs.create_df_for_graph_3()
graphs.create_df_for_graph_4()