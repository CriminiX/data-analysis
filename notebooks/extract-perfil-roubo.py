from re import sub
import numpy as np
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

URL = "https://www.ssp.sp.gov.br/Estatistica/perf_roubo/"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

def map_row_value(value: str):
    try:
        v = value.replace('%', '').replace(',', '.')
        return np.float64(v) / 100
    except:
        return np.nan
    
def map_month_name(value: str):
    try:
        return {
            'Jan': 1, 
            'Fev': 2, 
            'Mar': 3, 
            'Abr': 4, 
            'Mai': 5, 
            'Jun': 6, 
            'Jul': 7, 
            'Ago': 8, 
            'Set': 9, 
            'Out': 10, 
            'Nov': 11, 
            'Dez': 12
        }[value]
    except:
        return int(value)

def map_column_name(column_name: str):
    if not type(column_name) is str:
        return column_name
    temp = column_name.replace("\n", " ")
    temp = temp.replace("\r", " ")
    temp = sub("\s+", " ", temp)
    return temp.upper().strip()

def map_year(year: int):
    request = Request(f"{URL}{year}.htm")
    request.add_header('User-Agent', USER_AGENT)
    response = urlopen(request)
    assert response.status == 200, "RESPONSE NOT OK"

    content = response.read()
    soup = BeautifulSoup(content, 'html.parser')

    df = pd.DataFrame({"ANO": np.repeat(year, 13)})
    trs = soup.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        if not len(tds) > 13:
            continue
        tds_series = pd.Series(tds).map(lambda x: x.text).astype("object").replace("", np.nan)
        if not tds_series.size > 13:
            continue
        indexer = 0
        if '%' not in str(tds_series[1]):
            indexer = 1
        if 'Jan' == str(tds_series[1]):
            df['MES'] = tds_series[1:].reset_index(drop=True)
        else:
            if indexer == 1:
                df[map_column_name(tds_series[1])] = tds_series.iloc[2:].reset_index(drop=True)
            elif indexer == 0:
                df[map_column_name(tds_series[0])] = tds_series.iloc[1:].reset_index(drop=True)

    pd.set_option('display.max_columns', None)
    df = df.drop(columns=["TOTAL"]).dropna(how="all", axis=1).reset_index(drop=True)

    for c in df.columns[2:]:
        df[c] = df[c].map(map_row_value)
    df['MES'] = df['MES'].map(map_month_name)
    df = df.dropna(how="any", axis=1)

    return df

x_base = map_year(2014)
for y in range(2015,2023):
    x = map_year(y)
    x_base = pd.concat([x_base, x])

x_base.reset_index(drop=True).dropna(how="all", axis=1).drop(columns=[""]).to_csv("perfil-roubo.csv", index=False)
