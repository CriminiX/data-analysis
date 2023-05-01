import requests
from bs4 import BeautifulSoup
import time
from enum import Enum
from datetime import date
from typing import Union
import logging
from argparse import ArgumentParser

YEAR_SELECTION_FORMAT = "lkAno%-y"  # Only works on Unix
MONTH_SELECTION_FORMAT = "lkMes%-m"

DEFAULT_BROWSER_HEADERS = {
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
    "Cache-Control": "no-cache",
}

BUTTON_PREFIX = "ctl00${}"


def button(id):
    return BUTTON_PREFIX.format(id)


class CrimeType(Enum):
    CAR_THEFT = button("cphBody$btnRouboVeiculo")


class StatisticType(Enum):
    MONTHLY = button("conteudo$btnMensal")
    POLICY_PRODUCTIVITY = button("conteudo$btnPolicial")
    CRIME_RATE = button("conteudo$btnTaxa")


class AspFlow:
    def __init__(self, url, default_headers, default_filename) -> None:
        self.session = requests.Session()
        response = self.session.get(url, headers=default_headers)
        self.page = BeautifulSoup(response.text, "html.parser")
        self.url = url
        self.default_headers = default_headers
        self.default_filename = default_filename
        self.logger = logging.getLogger("aspflow")

    def click(self, target_id, event_argument=None, download_result=False, **kwargs):
        self.logger.info(f"Clicking {target_id}")
        viewstate = self.page.find("input", {"name": "__VIEWSTATE"})["value"]
        eventvalidation = self.page.find("input", {"name": "__EVENTVALIDATION"})[
            "value"
        ]
        viewstategenerator = self.page.find("input", {"name": "__VIEWSTATEGENERATOR"})[
            "value"
        ]

        data = {
            "__VIEWSTATE": viewstate,
            "__EVENTVALIDATION": eventvalidation,
            "__VIEWSTATEGENERATOR": viewstategenerator,
            "__EVENTARGUMENT": event_argument,
            "__LASTFOCUS": "",
            "__EVENTTARGET": target_id,
            **kwargs,
        }
        response = self.session.post(self.url, data=data, headers=self.default_headers)

        if download_result:
            with open(self.default_filename, "wb") as f:
                f.write(response.content)
        else:
            self.page = BeautifulSoup(response.text, "html.parser")

        return self


def extract_file(
    reference_date: Union[date, str, None] = None,
    default_filename="downloaded_file.xlsx",
    crime_type=CrimeType.CAR_THEFT,
):
    url = "http://www.ssp.sp.gov.br/transparenciassp/Consulta.aspx"
    flow = AspFlow(url, DEFAULT_BROWSER_HEADERS, default_filename)
    flow.click(button("cphBody$btnRouboVeiculo"))

    if reference_date is not None:
        reference_date = (
            date.fromisoformat(reference_date)
            if isinstance(reference_date, str)
            else reference_date
        )
        year = reference_date.strftime(YEAR_SELECTION_FORMAT)
        month = reference_date.strftime(MONTH_SELECTION_FORMAT)
        flow.click(button(f"cphBody${year}"))
        flow.click(button(f"cphBody${month}"))

    params = {
        "ctl00$cphBody$filtroDepartamento": "0",
        "ctl00$cphBody$hdfExport": time.time(),
    }
    flow.click(button("cphBody$ExportarBOLink"), download_result=True, **params)


def extract_statistics(
    reference_date: Union[date, str, None] = None,
    default_filename="downloaded_file.csv",
    stats_type=StatisticType.MONTHLY,
):
    url = "http://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx"
    flow = AspFlow(url, DEFAULT_BROWSER_HEADERS, default_filename)
    params = {
        "ctl00$conteudo$ddlAnos": 0,
        "ctl00$conteudo$ddlRegioes": 0,
        "ctl00$conteudo$ddlMunicipios": 0,
        "ctl00$conteudo$ddlDelegacias": 0,
    }
    flow.click(stats_type.value)
    if reference_date is not None:
        reference_date = (
            date.fromisoformat(reference_date)
            if isinstance(reference_date, str)
            else reference_date
        )
        year = reference_date.strftime("%Y")
        params["ctl00$conteudo$ddlAnos"] = year
        flow.click(button("conteudo$ddlAnos"), **params)
    export_params = {"ctl00$conteudo$btnExcel.x": 15, "ctl00$conteudo$btnExcel.y": 15}
    flow.click("", download_result=True, **params, **export_params)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    some_date = date(2005, 5, 5)
    parser = ArgumentParser()
    parser.add_argument("-type", choices=["theft", "statistics"], default="theft")
    args = parser.parse_args()
    if args.type == "theft":
        extract_file(some_date)
    elif args.type == "statistics":
        extract_statistics(some_date)
