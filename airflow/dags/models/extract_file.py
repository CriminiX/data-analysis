import time
from datetime import date
from typing import Union
from models.aspflow import AspFlow

from models import config_ssp

YEAR_SELECTION_FORMAT="lkAno%-y" # Only works on Unix
MONTH_SELECTION_FORMAT="lkMes%-m"

def extract_file(reference_date: Union[date, str, None] = None, default_filename="downloaded_file.xlsx", crime_type = None):
    url = 'http://www.ssp.sp.gov.br/transparenciassp/Consulta.aspx'
    default_headers = {
        "Host": "www.ssp.sp.gov.br", 
        "Referer": "http://www.ssp.sp.gov.br/transparenciassp/Consulta.aspx",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache"
    }

    flow = AspFlow(url, default_headers, default_filename)
    flow.click(config_ssp.button(crime_type))

    if reference_date is not None:
        reference_date = date.fromisoformat(reference_date) if isinstance(reference_date, str) else reference_date
        year = reference_date.strftime(YEAR_SELECTION_FORMAT)
        month = reference_date.strftime(MONTH_SELECTION_FORMAT)
        flow.click(config_ssp.button(year))
        flow.click(config_ssp.button(month))

    params = {"ctl00$cphBody$filtroDepartamento": "0", "ctl00$cphBody$hdfExport": time.time()}
    flow.click(config_ssp.button("ExportarBOLink"), download_result=True, **params)