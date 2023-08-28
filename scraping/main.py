from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import date
import time
import glob
import shutil

class Driver():

    def __init__(self) -> None:
        self.options  = webdriver.ChromeOptions()
        self.URL_BASE = "https://www.carrosnaweb.com.br/fichadetalhe.asp?codigo="

        # options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('disable-infobars')
        self.options.add_argument('--disable-extension')
        self.driver = webdriver.Chrome(service=Service(self.download_webdriver()), options=self.options)
        self.df_vehicles = pd.DataFrame()
        self.today = date.today().strftime('%d%m%Y')


    def download_webdriver(self):
        current_dir = ChromeDriverManager().install()
        destination_dir = r"G:\Meu Drive\workspace\bandtec\projetos_pi\tcc\data-analysis\scraping\web-driver\chromedriver.exe"
        shutil.copy(current_dir, destination_dir)

        return destination_dir

    def get_html(self, code):
        self.driver.get(self.URL_BASE + str(code))
        time.sleep(10)
        return self.driver.page_source
    
    def generate_ids(self):
        return np.arange(1, 20001, 1)
    
    def get_info_vehicles(self):
        ids = self.generate_ids()
        for id in ids:
            html_page =  self.get_html(id)

            soup = BeautifulSoup(html_page, 'html.parser')
            principal_table = soup \
                .find('table', 
                {
                    "cellspacing":"1",
                    "cellpadding":"3",
                    "border":"0",
                    "width":"100%"
                }, recursive=True)
            
            self.transform_informations(principal_table, id)
        
        self.save_file_csv(self.df_vehicles)

    def transform_informations(self, table_on_html: str, id: int):

        if table_on_html is None:
            print('{ Problema ao coletar informações do id: ', id, '}')
        else: 
      
            print('{ Iniciando coleta dos dados para o id: ', id, ' }')
            tbody = table_on_html.find_all('tbody')[0]
            rows = tbody.find_all('tr')

            info_vehicles = []

            for row in rows:
                cells = row.find_all('td')
                for cell in cells:
                    # if not cell.has_attr({"colspan":"6" "align":"center" "bgcolor":"#ffffff"}):
                    info_vehicles.append(cell.text.strip().replace('\n', ''))

            words_to_exclude = \
                [   "Página", 
                    "Compartilhe:", 
                    "As informa", 
                    "Ficha T", 
                    "Avaliação",
                    "SUSPENSÃO",
                    "FREIOS",
                    "DIREÇÃO",
                    "PNEUS",
                    "DIMENSÕES",
                    "AERODINÂMICA",
                    "DESEMPENHO",
                    "CONSUMO",
                    "AUTONOMIA",
                    "MOTOR",
                    "TRANSMISSÃO",
                    "Fotos",
                ]

            # Criar uma nova lista sem elementos que contenham palavras da lista de exclusão
            filtered_list_exclude = [item for item in info_vehicles if not any(word in item for word in words_to_exclude)]
            filtered_removed_empty = list(filter(None, filtered_list_exclude))

            info_veichle = []
            filtered_desc_labels = filtered_removed_empty[1:-1]

            j = -1

            for i in range(len(filtered_desc_labels)):
                # Indice para a informção do veículo
                j = j+2
                if j == 145:
                    break
                info_veichle.append(filtered_desc_labels[j])

            self.df_vehicles = pd.concat([self.df_vehicles, pd.DataFrame([info_veichle])], ignore_index=True)
            print('{ Coleta dos dados para o id: ', id, ' finalizado }')
            
    def save_file_csv(self, df_vehicles):
        df_vehicles.to_csv('./vehicles/anomesdia={}_/vehicles.csv'.format(self.today), index=False, header=False)
        print("Arquivo salvo com sucesso!")

if __name__ == "__main__":
    driver = Driver()

    driver.get_info_vehicles()


