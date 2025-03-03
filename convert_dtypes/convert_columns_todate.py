from datetime import date

def convert_columns_todate(dataframe):
    dates = []
    
    for column in dataframe.columns:
        year = int(column[1])
        month = 1
        day = 1
        if year in [7777, 8888, 9898, 9999]:
            code = year
            dates.append(code)
            pass
        else:
            fecha = date(year, month, day)
            dates.append(fecha)
    
    return dates

